import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions
from .serializers import *
from .models import Borrower, User, Book, BorrowingHistory
from .password_generator import *
from .mail import *

import logging

logger = logging.getLogger('django')


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


def login_page(request):
    logger.info("Rendering Logging Page")
    return render(request, 'login.html')


@api_view(['POST'])
def login_user(request):
    try:
        logger.info("Logging in to Library management System")
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            mail_id = data.get('email')
            password = data.get('password')
            hash_password = encode_string(password)
            # Authenticate user
            user = User.objects.get(email_id=mail_id, password=hash_password)

            if user is not None:
                # Set session variables
                request.session['user_id'] = user.id
                request.session['is_admin'] = user.is_admin
                # if user.is_admin:
                if user.is_admin:
                    redirect_url = '/admin_home/'
                else:
                    redirect_url = '/employer_home/'

                # Return success response with redirect URL
                return JsonResponse({'message': 'Login successful', 'redirect_url': redirect_url})
            else:
                # Login failed
                return JsonResponse({'message': 'Login failed. Invalid credentials'},
                                    status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in login_user: {e}")
        return JsonResponse({'message': 'An error occurred during login'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@admin_only
@login_required
def Admin_home_page(request):
    return render(request, 'book_management.html')


@login_required
@admin_only
def borrower_management_page(request):
    return render(request, 'borrower_management.html')


@login_required
@csrf_exempt
@admin_only
def book_management_page(request):
    return render(request, 'book_management.html')


@csrf_exempt
@login_required
def Borrower_home_page(request):
    return render(request, 'available_books.html')


@login_required
def available_books_page(request):
    return render(request, 'available_books.html')


@login_required
def borrowed_books_page(request):
    return render(request, 'borrowed_books.html')


@csrf_exempt
@api_view(['POST'])
@admin_only
@login_required
def register_borrower(request):
    try:
        logger.info("Registering the user")
        if request.method == 'POST':
            name = request.data.get('name')
            email_id = request.data.get('email')
            is_admin = request.data.get("is_admin")
            password_string = generate_random_string()
            hash_password = encode_string(password_string)
            user_details = User.objects.create(email_id=email_id, password=hash_password, is_admin=is_admin)
            if not is_admin:
                Borrower.objects.create(borrower_id=user_details, name=name, email_id=email_id)
            send_email(password_string, email_id)
            print(request.data)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error in register_borrower: {e}")
        return JsonResponse({'message': 'User registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@login_required
@admin_only
@api_view(['GET'])
def view_borrower(request):
    try:
        logger.info("List Book View")
        if request.method == 'GET':
            borrowers = Borrower.objects.all()
            serializer = BorrowerSerializer(borrowers, many=True)
            return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        logger.error(f"Error in list_books: {e}")
        return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@login_required
@admin_only
@api_view(['PUT', 'DELETE'])
def delete_borrower(request, borrower_id):
    try:
        borrower = Borrower.objects.get(borrower_id=borrower_id)
        if request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            borrower.name = data['name']
            borrower.email = data['email']
            borrower.save()
            return JsonResponse({'message': 'Borrower updated successfully'})

        if request.method == 'DELETE':
            user = User.objects.get(id=borrower_id)
            borrow_history = BorrowingHistory.objects.filter(borrower_id=borrower_id,
                                                             returned_date__isnull=True).exists()
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
@admin_only
@login_required
@api_view(['GET', 'POST'])
def manage_borrowers(request):
    if request.method == 'GET':
        borrowers = Borrower.objects.all().values()
        return JsonResponse(list(borrowers), safe=False)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        Borrower.objects.create(name=data['name'], email=data['email'])
        return JsonResponse({'message': 'Borrower added successfully'}, status=status.HTTP_201_CREATED)


@csrf_exempt
@admin_only
@login_required
@api_view(['PUT', 'DELETE'])
def modify_borrower(request, id):
    try:
        borrower = Borrower.objects.get(id=id)
    except Borrower.DoesNotExist:
        return JsonResponse({'message': 'Borrower not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        borrower.name = data['name']
        borrower.email = data['email']
        borrower.save()
        return JsonResponse({'message': 'Borrower updated successfully'})

    if request.method == 'DELETE':
        user = User.objects.get(id=id)
        borrow_history = BorrowingHistory.objects.filter(borrower_id=borrower.id,
                                                         returned_date__isnull=True).exists()
        if not borrow_history:
            borrower.delete()
            user.delete()
        return JsonResponse({'message': 'Borrower deleted successfully'})


@csrf_exempt
@admin_only
@login_required
@api_view(['GET', 'POST'])
def manage_books(request):
    if request.method == 'GET':
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({'message': 'Book added successfully'}, status=status.HTTP_201_CREATED)


@csrf_exempt
@admin_only
@login_required
@api_view(['GET'])
def get_borrower_name(request, id):
    borrower_name = ""
    borrowed_date = ""
    books = Book.objects.get(id = id)
    borrowing_history = BorrowingHistory.objects.filter(book=books, returned_date__isnull=True)
    if borrowing_history:
        borrower = Borrower.objects.filter(id=borrowing_history.values()[0]['borrower_id']).first()
        if borrower:
            borrower_name = borrower.name
            borrowed_date = borrowing_history.values()[0]['borrowed_date']
    return JsonResponse({"name": borrower_name,"borrowed_date":borrowed_date}, safe=False)

@csrf_exempt
@admin_only
@login_required
@api_view(['PUT', 'DELETE'])
def modify_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        # book = Book.objects.get(id=data["id"])
        date_str = data['published_date']
        date_str = date_str.replace('Sept.', 'Sep')
        date_obj = datetime.strptime(date_str, '%b %d, %Y')
        # Format the datetime object into the desired string format
        formatted_date = date_obj.strftime('%Y-%m-%d')
        data['published_date'] = formatted_date
        data["id"] = id
        serializer = BookSerializer(book, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({'message': 'Book updated successfully'})

    if request.method == 'DELETE':
        book.delete()
        return JsonResponse({'message': 'Book deleted successfully'})


@csrf_exempt
@login_required
@admin_only
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'edit_book.html', {'book': book})


@csrf_exempt
@login_required
@admin_only
def edit_borrower(request, id):
    borrower = get_object_or_404(Borrower, borrower_id=id)
    return render(request, 'edit_borrower.html', {'borrower': borrower})


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
        logger.info("Borrower View books")
        if request.method == 'GET':
            books = Book.objects.filter(status="available")
            data = list(books.values('id', 'title', 'author', 'published_date'))
            return JsonResponse(data, safe=False)
    except Exception as e:
        logger.error(f"Error in list_status_books: {e}")
        return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @csrf_exempt
# @login_required
# @api_view(['GET'])
# def list_books(request):
#     try:
#         if request.method == 'GET':
#             books = Book.objects.all()
#             serializer = BookSerializer(books, many=True)
#             return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK, safe=False)
#     except Exception as e:
#         # logger.error(f"Error in list_books: {e}")
#         return JsonResponse({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@login_required
@api_view(['POST'])
def book_check_out(request, book_id):
    try:
        if request.method == 'POST':
            # book_name = request.data.get('book')
            borrower_id = request.session.get("user_id")

            # borrowed_date = request.data.get('borrowed_date')

            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

            if book.status == Book.AVAILABLE:
                try:
                    borrower = Borrower.objects.get(borrower_id=borrower_id)
                except Borrower.DoesNotExist:
                    return Response({"message": "Borrower not found"}, status=status.HTTP_404_NOT_FOUND)

                BorrowingHistory.objects.create(book=book, borrower=borrower,
                                                borrowed_date=datetime.now().strftime("%Y-%m-%d"))
                book.status = Book.CHECKEDOUT
                book.save()

                # borrow_history = BorrowingHistory.objects.filter(borrower=borrower)
                # serializer = BorrowingHistorySerializer(borrow_history, many=True)

                return JsonResponse({'success': True})
    except Exception as ex:
        print(ex)


@csrf_exempt
@login_required
@api_view(['POST'])
def return_book(request, book_id):
    if request.method == "POST":
        borrower_id = request.session.get("user_id")
        borrow_history = BorrowingHistory.objects.get(id=book_id)
        book = Book.objects.get(id=borrow_history.book.id)
        # borrow_history = BorrowingHistory.objects.get(book=book, borrower__borrower_id=borrower_id)
        borrow_history.returned_date = datetime.now().strftime("%Y-%m-%d")
        borrow_history.save()
        book.status = Book.AVAILABLE
        book.save()
        return JsonResponse({'success': True})


@csrf_exempt
@login_required
@api_view(['GET'])
def borrowing_history(request):
    try:
        if request.method == 'GET':
            borrower_id = request.session.get("user_id")
            if borrower_id:
                try:
                    borrower = Borrower.objects.get(borrower_id=borrower_id)
                except Borrower.DoesNotExist:
                    return Response({"message": "Borrower not found"}, status=status.HTTP_404_NOT_FOUND)

                history = BorrowingHistory.objects.filter(borrower=borrower, returned_date__isnull=True)
            else:
                history = BorrowingHistory.objects.all()
            data = [
                {
                    'id': entry.id,
                    'title': entry.book.title,
                    'author': entry.book.author,
                    'borrowed_date': entry.borrowed_date,
                } for entry in history
            ]
            return JsonResponse(data, safe=False)


    except Exception as e:
        logger.error(f"Error in Borrowing history: {e}")
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
        del request.session['user_id']
        del request.session['is_admin']
        # if request.method == 'POST':
        return JsonResponse({'redirect_url': '/login/'}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error in logout_user: {e}")
        return JsonResponse({'message': 'An error occurred during logout'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User.objects.filter(is_admin=False).delete()

# def delete