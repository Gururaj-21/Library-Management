from django.urls import path
from .views import *

urlpatterns = [
    path('', login_page),
    path('login/',login_page),
    path('login_user/', login_user, name='login'),
    path('admin_home/', Admin_home_page, name='admin_home'),
    path('employer_home/', Borrower_home_page, name='Borrower_home_page'),
    path('available-books/', available_books_page, name='available_books_page'),
    path('borrowed-books/', borrowed_books_page, name='borrowed_books_page'),
    path('borrower-management/', borrower_management_page, name='borrower_management_page'),
    path('book-management/', book_management_page, name='book_management_page'),
    path('register/', register_borrower, name='register'),
    # path('book_management/', book_management, name='book_management'),
    path('borrowing_history/', borrowing_history, name="borrowing_management"),
    path('books_checkout/<int:book_id>/',book_check_out),
    path('books_return/<int:book_id>/', return_book, name='return_book'),
    path('list_status_books/', list_status_books, name="list_status_books"),
    # path('borrower_view/', view_borrower),
    # path('delete_borrower/<int:borrower_id>/', delete_borrower),
    # path('view_user/', get_user),
    path('api/borrowers/', manage_borrowers, name='manage_borrowers'),
    path('api/borrowers/<int:borrower_id>/', delete_borrower, name='modify_borrower'),
    path('api/books/', manage_books, name='manage_books'),
    path('api/books/<int:id>/', modify_book, name='modify_book'),
    path('edit_book/<int:id>/', edit_book, name='edit_book'),
    path('edit_borrower/<int:id>/', edit_borrower, name='edit_borrower'),
    path('logout/', logout_user, name='logout'),


]
