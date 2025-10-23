document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    document.getElementById('logout-button').addEventListener('click', logout);

    // Fetch and display users
    const userList = document.getElementById('user-list');
    fetchWithAuth('/users/')
        .then(response => response.json())
        .then(users => {
            users.forEach(user => {
                const li = document.createElement('li');
                li.textContent = `${user.username} (${user.role})`;
                userList.appendChild(li);
            });
        });

    // Fetch and display tables
    const tableList = document.getElementById('table-list');
    fetchWithAuth('/tables/')
        .then(response => response.json())
        .then(tables => {
            tables.forEach(table => {
                const li = document.createElement('li');
                li.textContent = `Table ${table.number} (${table.seats} seats)`;
                tableList.appendChild(li);
            });
        });

    // Fetch and display categories
    const categoryList = document.getElementById('category-list');
    const itemCategory = document.getElementById('item-category');
    fetchWithAuth('/categories/')
        .then(response => response.json())
        .then(categories => {
            categories.forEach(category => {
                const li = document.createElement('li');
                li.textContent = category.name;
                categoryList.appendChild(li);

                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                itemCategory.appendChild(option);
            });
        });

    // Fetch and display menu items
    const menuItemList = document.getElementById('menu-item-list');
    fetchWithAuth('/menu-items/')
        .then(response => response.json())
        .then(items => {
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.name} - ${item.price}€`;
                menuItemList.appendChild(li);
            });
        });

    // Handle form submissions
    document.getElementById('user-form').addEventListener('submit', event => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('user-role').value;
        fetchWithAuth('/users/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, role })
        }).then(() => location.reload());
    });

    document.getElementById('table-form').addEventListener('submit', event => {
        event.preventDefault();
        const number = document.getElementById('table-number').value;
        const seats = document.getElementById('table-seats').value;
        fetchWithAuth('/tables/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ number, seats })
        }).then(() => location.reload());
    });

    document.getElementById('category-form').addEventListener('submit', event => {
        event.preventDefault();
        const name = document.getElementById('category-name').value;
        fetchWithAuth('/categories/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        }).then(() => location.reload());
    });

    document.getElementById('menu-item-form').addEventListener('submit', event => {
        event.preventDefault();
        const name = document.getElementById('item-name').value;
        const description = document.getElementById('item-description').value;
        const price = document.getElementById('item-price').value;
        const category_id = document.getElementById('item-category').value;
        fetchWithAuth('/menu-items/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description, price, category_id })
        }).then(() => location.reload());
    });

    // Fetch and display sales report
    const salesReport = document.getElementById('sales-report');
    fetchWithAuth('/analytics/sales/')
        .then(response => response.json())
        .then(data => {
            salesReport.innerHTML = `
                <p>Total Sales: ${data.total_sales.toFixed(2)}€</p>
                <p>Total Bills: ${data.total_bills}</p>
            `;
        });
});
