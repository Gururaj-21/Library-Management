document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    const addBorrowerButton = document.getElementById('addBorrowerButton');
    const borrowerFormContainer = document.getElementById('borrowerFormContainer');

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

    // Load borrowers on page load
    loadBorrowers();

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

    window.editBorrower = function(id) {
        window.location.href = `/edit_borrower/${id}/`;
    }

    window.deleteBorrower = async function(id) {
        await fetch(`/api/borrowers/${id}/`, {
            method: 'DELETE',
        });
        loadBorrowers();
    }

    function cancelForm() {
        borrowerFormContainer.innerHTML = '';
    }
});
