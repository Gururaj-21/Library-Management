# Library Management System

This project is a Django-based library management system that allows users to manage books, borrowers, and borrowing history. 

## Features
 - Manage books and borrowers.
 - Track borrowing history.
 - Api endpoints to do crud operations for borrower, books,borrowing history.
 - Integrated mail to send the password mail to the borrowers.
 - Implemented login_required and admin_only access for the api's.

## Requirement
 - Python 3.x
 - Django 3.x or later
 - Django REST Framework

## Installation
 1. Clone the repository:
    ```shell
    git clone https://github.com/Gururaj-21/Library-Management.git
    cd .\Library_Management_System\
    ```
 2. Create a virtual environment and activate it:
    ```shell
    python -m venv venv
    source venv/bin/activate 
    ```
 3. Install the requirements:
    ```shell
    pip install -r requirements.txt
    ```
 4. Apply Migrations:
    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```
 5. Start the development server:
    ```shell
    python manage.py runserver
    ```

### Using Postman Collections

To easily test the API endpoints, you can use Postman collections. Follow these steps:

1. **Install Postman:**

    Download and install Postman from the [official website](https://www.postman.com/downloads/).

2. **Import the Collection:**

    - Open Postman.
    - Click on the `Import` button.
    - Select the `File` tab.
    - Click `Choose Files` and select the `Library_Management_System.Library Management Api's.postman_collection.json` file provided in this repository.

3. **Using the Requests:**

    - Open the imported collection.
    - Each folder contains requests for CRUD operations for borrowers, books, and borrowing history.
    - Click on any request to open it.
    - Click `Send` to execute the request.

## Admin credentials:
Uses this credential to login as Ads=min
- mail_id:gururaj431@gmail.com
- password:bUlqUe2FtG