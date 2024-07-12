from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'


class BorrowingHistorySerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='book.title')
    borrower = serializers.CharField(source='borrower.name')

    class Meta:
        model = BorrowingHistory
        fields = ['book', 'borrower', 'borrowed_date', 'returned_date']


class BorrowingHistoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingHistory
        fields = ['returned_date']
