from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
import json

from .models import Borrower, BorrowingHistory, Book


class RegisterBorrowerTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_borrower_registration(self):
        data = {
            "name": "raj",
            "email": "gururajkt21@gmail.com",
            "isAdmin": "false",
        }
        response = self.client.post("/register/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "User registered successfully"})

    def test_borrower_registration_as_admin(self):
        data = {"name": "Test Admin", "email": "test@admin.com", "isAdmin": "true"}
        response = self.client.post("/register/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "User registered successfully"})


class BookManagementTest(TestCase):
    # def setUp(self):
    #     self.client = Client()
    #     self.user = User.objects.create_user(username="test_user", password="test_password")
    #     self.client.login(username="test_user", password="test_password")  # Simulate login

    def test_create_book_success(self):
        data = {
            "title": "Data Structure",
            "author": "john",
            "isbn": "54653121",
            "published_date": "2017-05-10"
        }
        response = self.client.post("/book_management/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Book created successfully!")
        self.assertIn("data", response.json())

    def test_update_book_success(self):
        # Create a book first
        book_data = {
            "title": "Data Structure",
            "author": "john",
            "isbn": "54653121",
            "published_date": "2017-05-10"
        }
        book_response = self.client.post("/book_management/", json.dumps(book_data), content_type="application/json")
        book_id = book_response.json()["data"][0]["id"]

        # Update data
        update_data = {"id": book_id, "title": "DSA"}
        response = self.client.put(f"/book_management/", json.dumps(update_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Book updated successfully!")
        self.assertIn("data", response.json())

    def test_update_book_invalid_data(self):
        # Create a book first
        book_data = {
            "title": "Data Structure",
            "author": "john",
            "isbn": "54653121",
            "published_date": "2017-05-10"
        }
        book_response = self.client.post("/book_management/", json.dumps(book_data), content_type="application/json")
        book_id = book_response.json()["data"][0]["id"]

        # Update with invalid data
        update_data = {"id": book_id, "name": "invalid_value"}
        response = self.client.put(f"/book_management/", json.dumps(update_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_book_success(self):
        book_data = {
            "title": "Data Structure",
            "author": "john",
            "isbn": "54653121",
            "published_date": "2017-05-10"
        }
        book_response = self.client.post("/book_management/", json.dumps(book_data), content_type="application/json")
        book_id = book_response.json()["data"][0]["id"]
        delete_data = {"id": book_id}
        response = self.client.delete(f"/book_management/", json.dumps(delete_data),
                                      content_type="application/json")
        self.assertEqual(response.status_code, 200)

