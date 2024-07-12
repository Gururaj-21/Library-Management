from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions
from .serializers import *
from .models import Borrower, User, Book, BorrowingHistory
from .password_generator import *
from .mail import *


# import logging

# logger = logging.getLogger(__name__)

def login_required(function):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return JsonResponse({'message': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
        return function(request, *args, **kwargs)

    return wrapper


def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_admin'):
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'message': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

    return wrapper


@csrf_exempt
@api_view(['POST'])
@admin_only
@login_required
def register_borrower(request):
    try:
        # logger.info("Registering the user")
        if request.method == 'POST':
            name = request.data.get('name')
            email_id = request.data.get('email')
            is_admin = request.data.get('isAdmin')
            if is_admin == "true":
                is_admin = True
            else:
                is_admin = False
            password_string = generate_random_string()
            hash_password = encode_string(password_string)
            user_details = User.objects.create(email_id=email_id, password=hash_password, is_admin=is_admin)
            if not is_admin:
                Borrower.objects.create(borrower_id=user_details, name=name, email_id=email_id)
            send_email(password_string, email_id)
            print(request.data)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        # logger.error(f"Error in register_borrower: {e}")
        return JsonResponse({'message': 'User registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_user(request):
    try:
        if request.method == 'POST':
            mail_id = request.data.get('mail_id')
            password = request.data.get('password')
            hash_password = encode_string(password)
            # Authenticate user
            user = User.objects.get(email_id=mail_id, password=hash_password)

            if user is not None:
                # Set session variables
                request.session['user_id'] = user.id
                request.session['is_admin'] = user.is_admin

                return JsonResponse({'message': 'Login successful'})
            else:
                # Login failed
                return JsonResponse({'message': 'Login failed. Invalid credentials'},
                                    status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # logger.error(f"Error in login_user: {e}")
        return JsonResponse({'message': 'An error occurred during login'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@admin_only
@login_required
def book_management(request):
    try:
        if request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = BookSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                books = Book.objects.all()
                all_books_serializer = BookSerializer(books, many=True)
                return JsonResponse({"message": "Book created successfully!", "data": all_books_serializer.data},
                                    status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            book = Book.objects.get(id=data["id"])
            serializer = BookSerializer(book, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                books = Book.objects.all()
                all_books_serializer = BookSerializer(books, many=True)
                return JsonResponse({"message": "Book updated successfully!", "data": all_books_serializer.data},
                                    status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            book = Book.objects.get(id=request.data.get('id'))
            book.delete()
            books = Book.objects.all()
            all_books_serializer = BookSerializer(books, many=True)
            return JsonResponse({"message": "Book deleted successfully!", "data": all_books_serializer.data},
                                status=status.HTTP_200_OK)
        elif request.method == 'GET':
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@login_required
@api_view(['GET'])
def list_status_books(request):
    try:
        if request.method == 'GET':
            books = Book.objects.filter(status=request.data.get('status'))
            serializer = BookSerializer(books, many=True)
            return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        # logger.error(f"Error in list_status_books: {e}")
        return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@login_required
@api_view(['GET'])
def list_books(request):
    try:
        if request.method == 'GET':
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        # logger.error(f"Error in list_books: {e}")
        return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@login_required
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def borrowing_history(request):
    try:
        if request.method == 'POST':
            book_name = request.data.get('book')
            borrower_id = request.data.get('borrower')
            borrowed_date = request.data.get('borrowed_date')

            try:
                book = Book.objects.get(title=book_name)
            except Book.DoesNotExist:
                return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

            if book.status == Book.AVAILABLE:
                try:
                    borrower = Borrower.objects.get(borrower_id=borrower_id)
                except Borrower.DoesNotExist:
                    return Response({"message": "Borrower not found"}, status=status.HTTP_404_NOT_FOUND)

                BorrowingHistory.objects.create(book=book, borrower=borrower, borrowed_date=borrowed_date)
                book.status = Book.CHECKEDOUT
                book.save()

                borrow_history = BorrowingHistory.objects.filter(borrower=borrower)
                serializer = BorrowingHistorySerializer(borrow_history, many=True)

                return Response({"message": "Book successfully checked out", "data": serializer.data})

            else:
                borrow_history = BorrowingHistory.objects.filter(borrower__borrower_id=borrower_id)
                serializer = BorrowingHistorySerializer(borrow_history, many=True)

                return Response(
                    {"message": "Book already checked out", "data": serializer.data},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        elif request.method == 'GET':
            borrower_id = request.data.get('borrower_id')
            if borrower_id:
                try:
                    borrower = Borrower.objects.get(borrower_id=borrower_id)
                except Borrower.DoesNotExist:
                    return Response({"message": "Borrower not found"}, status=status.HTTP_404_NOT_FOUND)

                history = BorrowingHistory.objects.filter(borrower=borrower)
            else:
                history = BorrowingHistory.objects.all()

            serializer = BorrowingHistorySerializer(history, many=True)
            return Response({"data": serializer.data})

        elif request.method == "PUT":
            book_name = request.data.get('book_name')
            borrower_id = request.data.get('borrower_id')

            if not book_name:
                return Response({"message": "Book name is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                book = Book.objects.get(title=book_name)
            except Book.DoesNotExist:
                return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                borrowing_history = BorrowingHistory.objects.get(book=book, borrower__borrower_id=borrower_id,
                                                                 returned_date__isnull=True)
            except BorrowingHistory.DoesNotExist:
                return Response({"message": "No active borrowing history found for this book"},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = BorrowingHistoryUpdateSerializer(borrowing_history, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # Update the book status to available if the returned date is provided
                if 'returned_date' in serializer.validated_data:
                    book.status = Book.AVAILABLE
                    book.save()

                return Response({"message": "Borrowing history updated successfully", "data": serializer.data})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # logger.error(f"Error in Borrowing history: {e}")
        return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@login_required
@admin_only
@api_view(['GET'])
def view_borrower(request):
    try:
        if request.method == 'GET':
            borrowers = Borrower.objects.all()
            serializer = BorrowerSerializer(borrowers, many=True)
            return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        # logger.error(f"Error in list_books: {e}")
        return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@login_required
@admin_only
@api_view(['DELETE'])
def delete_borrower(request,borrower_id):
    try:
        borrower = Borrower.objects.get(borrower_id=borrower_id)
        user = User.objects.get(id = borrower_id)
        borrow_history = BorrowingHistory.objects.filter(returned_date__isnull=True).exists()
        if not borrow_history:
            borrower.delete()
            user.delete()
            return JsonResponse({"message": "Borrower deleted successfully!"},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "Return all the books before deleting"},
                                status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def get_user(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
@api_view(['POST'])
@login_required
def logout_user(request):
    try:
        if request.method == 'POST':
            return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        # logger.error(f"Error in logout_user: {e}")
        return JsonResponse({'message': 'An error occurred during logout'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
