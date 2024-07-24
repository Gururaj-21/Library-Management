document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    const addBorrowerButton = document.getElementById('addBorrowerButton');
    const addBookButton = document.getElementById('addBookButton');
    const borrowerFormContainer = document.getElementById('borrowerFormContainer');
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


    // Add Borrower Button Event
    addBorrowerButton.addEventListener('click', function() {
        showBorrowerForm();
    });

    // Add Book Button Event
    addBookButton.addEventListener('click', function() {
        showBookForm();
    });

    // Load borrowers and books on page load
    loadBorrowers();
    loadBooks();

    async function loadBorrowers() {
        const response = await fetch('/api/borrowers/');
        const borrowers = await response.json();
        const tbody = document.getElementById('borrowersTable').querySelector('tbody');
        tbody.innerHTML = '';
        borrowers.forEach(borrower => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${borrower.borrower_id_id}</td>
                <td>${borrower.name}</td>
                <td>${borrower.email_id}</td>
                <td>
                    <button onclick="editBorrower(${borrower.borrower_id_id})">Edit</button>
                    <button onclick="deleteBorrower(${borrower.borrower_id_id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

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


    window.showBorrowerForm = function(borrower = {}) {
        borrowerFormContainer.innerHTML = `
            <h3>${borrower.id ? 'Edit' : 'Add'} Borrower</h3>
            <form id="borrowerForm">
                <input type="text" id="borrowerName" placeholder="Name" value="${borrower.name || ''}" required>
                <input type="email" id="borrowerEmail" placeholder="Email" value="${borrower.email_id || ''}" required>
                <label>
                    <input type="checkbox" id="isAdmin" ${borrower.is_admin ? 'checked' : ''}>
                    Is Admin
                </label>
                <button type="submit">${borrower.borrower_id_id ? 'Update' : 'Add'} Borrower</button>
                ${borrower.borrower_id_id ? `<button type="button" onclick="cancelForm()">Cancel</button>` : ''}
            </form>
        `;

        const borrowerForm = document.getElementById('borrowerForm');
        borrowerForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const name = document.getElementById('borrowerName').value;
            const email = document.getElementById('borrowerEmail').value;
            const is_admin = document.getElementById('isAdmin').checked;

            if (borrower.borrower_id_id) {
                // Update Borrower
                await fetch(`/api/borrowers/${borrower.borrower_id_id}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name, email, is_admin }),
                });
            } else {
                // Add Borrower
                await fetch('/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name, email, is_admin }),
                });
            }
            loadBorrowers();
            borrowerFormContainer.innerHTML = '';
        });
    }

    window.showBookForm = function(book = {}) {
        bookFormContainer.innerHTML = `
            <h3>${book.id ? 'Edit' : 'Add'} Book</h3>
            <form id="bookForm">
                <input type="text" id="bookTitle" placeholder="Title" value="${book.title || ''}" required>
                <input type="text" id="bookAuthor" placeholder="Author" value="${book.author || ''}" required>
                <input type="text" id="isbn" placeholder="Isbn" value="${book.isbn || ''}" required>
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

    window.editBorrower = function(id) {
        window.location.href = `/edit_borrower.html?id=${id}`;
    }

    window.deleteBorrower = async function(id) {
        await fetch(`/edit_book/${id}/`, {
            method: 'DELETE',
        });
        loadBorrowers();
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
        borrowerFormContainer.innerHTML = '';
        bookFormContainer.innerHTML = '';
    }
});
