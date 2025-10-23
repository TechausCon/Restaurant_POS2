document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://localhost:8000';
    let selectedTable = null;
    let currentOrder = [];

    const tableGrid = document.getElementById('table-grid');
    const categoryButtons = document.getElementById('category-buttons');
    const menuItems = document.getElementById('menu-items');
    const orderItems = document.getElementById('order-items');
    const selectedTableSpan = document.getElementById('selected-table');
    const placeOrderButton = document.getElementById('place-order');

    // Fetch tables
    fetch(`${apiUrl}/tables/`)
        .then(response => response.json())
        .then(tables => {
            tables.forEach(table => {
                const div = document.createElement('div');
                div.classList.add('table');
                div.textContent = `Table ${table.number}`;
                div.addEventListener('click', () => {
                    selectedTable = table.id;
                    selectedTableSpan.textContent = table.number;
                    document.querySelectorAll('.table').forEach(t => t.classList.remove('selected'));
                    div.classList.add('selected');
                });
                tableGrid.appendChild(div);
            });
        });

    // Fetch categories and menu items
    fetch(`${apiUrl}/categories/`)
        .then(response => response.json())
        .then(categories => {
            categories.forEach(category => {
                const button = document.createElement('button');
                button.textContent = category.name;
                button.addEventListener('click', () => {
                    menuItems.innerHTML = '';
                    category.items.forEach(item => {
                        const div = document.createElement('div');
                        div.classList.add('menu-item');
                        div.textContent = `${item.name} - ${item.price}€`;
                        div.addEventListener('click', () => {
                            const orderItem = currentOrder.find(i => i.menu_item_id === item.id);
                            if (orderItem) {
                                orderItem.quantity++;
                            } else {
                                currentOrder.push({ menu_item_id: item.id, quantity: 1, name: item.name });
                            }
                            renderOrder();
                        });
                        menuItems.appendChild(div);
                    });
                });
                categoryButtons.appendChild(button);
            });
        });

    function renderOrder() {
        orderItems.innerHTML = '';
        currentOrder.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.name} x${item.quantity}`;
            orderItems.appendChild(li);
        });
    }

    placeOrderButton.addEventListener('click', () => {
        if (selectedTable && currentOrder.length > 0) {
            fetch(`${apiUrl}/orders/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ table_id: selectedTable, items: currentOrder })
            }).then(() => {
                currentOrder = [];
                renderOrder();
                alert('Order placed!');
            });
        } else {
            alert('Please select a table and add items to the order.');
        }
    });
});
