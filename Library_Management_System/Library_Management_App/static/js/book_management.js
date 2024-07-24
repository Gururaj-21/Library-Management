document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    const addBookButton = document.getElementById('addBookButton');
    const bookFormContainer = document.getElementById('bookFormContainer');

    // Logout button event
    logoutButton.addEventListener('click', async function() {
        const response = await fetch('/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const data = await response.json();
            // Redirect to home page
            window.location.href = data.redirect_url;
        }
    });

    // Add Book Button Event
    addBookButton.addEventListener('click', function() {
        showBookForm();
    });

    // Load books on page load
    loadBooks();

    async function loadBooks() {
        const response = await fetch('/api/books/');
        const books = await response.json();
        const tbody = document.getElementById('booksTable').querySelector('tbody');
        tbody.innerHTML = '';
        books.forEach(book => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.isbn}</td>
                <td>${book.published_date}</td>
                <td>${book.status}</td>
                <td>
                    <button onclick="editBook(${book.id})">Edit</button>
                    <button onclick="deleteBook(${book.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    window.showBookForm = function(book = {}) {
        bookFormContainer.innerHTML = `
            <h3>${book.id ? 'Edit' : 'Add'} Book</h3>
            <form id="bookForm">
                <input type="text" id="bookTitle" placeholder="Title" value="${book.title || ''}" required>
                <input type="text" id="bookAuthor" placeholder="Author" value="${book.author || ''}" required>
                <input type="text" id="isbn" placeholder="ISBN" value="${book.isbn || ''}" required>
                <input type="text" id="published_date" placeholder="Published Date" value="${book.published_date || ''}" required>
                <button type="submit">${book.id ? 'Update' : 'Add'} Book</button>
                ${book.id ? `<button type="button" onclick="cancelForm()">Cancel</button>` : ''}
            </form>
        `;

        const bookForm = document.getElementById('bookForm');
        bookForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const title = document.getElementById('bookTitle').value;
            const author = document.getElementById('bookAuthor').value;
            const isbn = document.getElementById('isbn').value;
            const published_date = document.getElementById('published_date').value;

            if (book.id) {
                // Update Book
                await fetch(`/api/books/${book.id}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title, author, isbn, published_date }),
                });
            } else {
                // Add Book
                await fetch('/api/books/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title, author, isbn, published_date}),
                });
            }
            loadBooks();
            bookFormContainer.innerHTML = '';
        });
    }

    window.editBook = function(id) {
        window.location.href = `/edit_book/${id}/`;
    }

    window.deleteBook = async function(id) {
        console.log(`Deleting book with ID: ${id}`);
        await fetch(`/api/books/${id}/`, {
            method: 'DELETE',
        });
        loadBooks();
    }

    function cancelForm() {
        bookFormContainer.innerHTML = '';
    }
});
