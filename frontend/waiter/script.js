document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    document.getElementById('logout-button').addEventListener('click', logout);

    let selectedTable = null;
    let currentOrder = [];

    const tableGrid = document.getElementById('table-grid');
    const categoryButtons = document.getElementById('category-buttons');
    const menuItems = document.getElementById('menu-items');
    const orderItems = document.getElementById('order-items');
    const selectedTableSpan = document.getElementById('selected-table');
    const placeOrderButton = document.getElementById('place-order');

    // Fetch tables
    fetchWithAuth('/tables/')
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
    fetchWithAuth('/categories/')
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
            fetchWithAuth('/orders/', {
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

    const generateBillButton = document.getElementById('generate-bill');
    generateBillButton.addEventListener('click', () => {
        if (selectedTable) {
            fetchWithAuth(`/orders/table/${selectedTable}`)
                .then(response => response.json())
                .then(orders => {
                    const unbilledOrders = orders.filter(order => !order.bill_id);
                    if (unbilledOrders.length === 0) {
                        alert("No unbilled orders for this table.");
                        return;
                    }
                    const total = unbilledOrders.reduce((acc, order) => {
                        return acc + order.items.reduce((acc, item) => {
                            return acc + (item.menu_item.price * item.quantity);
                        }, 0);
                    }, 0);
                    const order_ids = unbilledOrders.map(order => order.id);

                    fetchWithAuth('/bills/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ total: total, order_ids: order_ids })
                    }).then(() => {
                        alert('Bill generated!');
                        renderBills();
                    });
                });
        } else {
            alert('Please select a table.');
        }
    });

    function renderBills() {
        if (selectedTable) {
            fetchWithAuth(`/bills/table/${selectedTable}`)
                .then(response => response.json())
                .then(bills => {
                    const tableBillsDiv = document.getElementById('table-bills');
                    tableBillsDiv.innerHTML = '';
                    bills.forEach(bill => {
                        const div = document.createElement('div');
                        div.textContent = `Bill #${bill.id}: ${bill.total}€ - ${bill.is_paid ? `Paid (${bill.payment_method})` : 'Unpaid'}`;

                        if (!bill.is_paid) {
                            const payCashButton = document.createElement('button');
                            payCashButton.textContent = 'Pay with Cash';
                            payCashButton.addEventListener('click', () => {
                                fetchWithAuth(`/bills/${bill.id}`, {
                                    method: 'PUT',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ is_paid: 1, payment_method: 'cash' })
                                }).then(() => renderBills());
                            });
                            div.appendChild(payCashButton);

                            const payCardButton = document.createElement('button');
                            payCardButton.textContent = 'Pay with Card';
                            payCardButton.addEventListener('click', () => {
                                fetchWithAuth(`/bills/${bill.id}`, {
                                    method: 'PUT',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ is_paid: 1, payment_method: 'card' })
                                }).then(() => renderBills());
                            });
                            div.appendChild(payCardButton);
                        }

                        tableBillsDiv.appendChild(div);
                    });
                });
        }
    }
});
