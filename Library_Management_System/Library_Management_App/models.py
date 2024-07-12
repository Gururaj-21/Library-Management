from django.db import models


# Create your models here.
class Book(models.Model):
    AVAILABLE = 'available'
    CHECKEDOUT ='checked_out'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (CHECKEDOUT, 'Checked Out'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.title} by {self.author}"


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class Borrower(models.Model):
    borrower_id = models.ForeignKey(User,related_name='Borrower_history',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email_id = models.EmailField(unique=True)

    def __str__(self):
        return self.borrower_id


class BorrowingHistory(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, related_name='book_history', on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, related_name='borrower_history', on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower} borrowed {self.book}"
