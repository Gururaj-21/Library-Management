from django.urls import path
from .views import *

urlpatterns = [
    path('login_user/', login_user, name='login'),
    path('register/', register_borrower, name='register'),
    path('book_management/',book_management,name='book_management'),
    path('borrowing_history/',borrowing_history,name="borrowing_management"),
    path('list_status_books/',list_status_books,name="list_status_books"),
    path('logout/',logout_user,name='logout')
]