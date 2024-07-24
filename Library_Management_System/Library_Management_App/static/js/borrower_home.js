document.addEventListener('DOMContentLoaded', function() {
    loadAvailableBooks();
    loadBorrowedBooks();
    async function loadAvailableBooks() {
        const response = await fetch('/list_status_books/');
        const books = await response.json();
        const tbody = document.getElementById('availableBooksTable');
        tbody.innerHTML = '';
        books.forEach(book => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.published_date}</td>
                <td><button onclick="checkoutBook(${book.id})">Checkout</button></td>
            `;
            tbody.appendChild(row);
        });
    }

    async function loadBorrowedBooks() {
        const response = await fetch('/borrowing_history/');
        const books = await response.json();
        const tbody = document.getElementById('borrowedBooksTable');
        tbody.innerHTML = '';
        books.forEach(book => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.borrowed_date}</td>
                <td><button onclick="returnBook(${book.id})">Return</button></td>
            `;
            tbody.appendChild(row);
        });
    }


    window.checkoutBook = async function(bookId) {
        await fetch(`/books_checkout/${bookId}/`, {
            method: 'POST',
        });
        loadAvailableBooks();
    }

    window.returnBook = async function(bookId) {
        await fetch(`/books_return/${bookId}/`, {
            method: 'POST',
        });
        loadBorrowedBooks();
    }
});
