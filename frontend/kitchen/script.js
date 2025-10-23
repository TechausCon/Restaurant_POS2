document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://localhost:8000';
    const ordersContainer = document.getElementById('orders-container');

    function fetchOrders() {
        fetch(`${apiUrl}/orders/`)
            .then(response => response.json())
            .then(orders => {
                ordersContainer.innerHTML = '';
                orders.forEach(order => {
                    const orderCard = document.createElement('div');
                    orderCard.classList.add('order-card');

                    const title = document.createElement('h2');
                    title.textContent = `Table ${order.table_id} - ${order.status}`;
                    orderCard.appendChild(title);

                    const itemList = document.createElement('ul');
                    order.items.forEach(item => {
                        const li = document.createElement('li');
                        li.textContent = `${item.menu_item.name} x${item.quantity}`;
                        itemList.appendChild(li);
                    });
                    orderCard.appendChild(itemList);

                    const statusSelect = document.createElement('select');
                    statusSelect.innerHTML = `
                        <option value="pending" ${order.status === 'pending' ? 'selected' : ''}>Pending</option>
                        <option value="in_progress" ${order.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                        <option value="completed" ${order.status === 'completed' ? 'selected' : ''}>Completed</option>
                    `;
                    statusSelect.addEventListener('change', () => {
                        fetch(`${apiUrl}/orders/${order.id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ status: statusSelect.value })
                        }).then(() => fetchOrders());
                    });
                    orderCard.appendChild(statusSelect);

                    ordersContainer.appendChild(orderCard);
                });
            });
    }

    fetchOrders();
    setInterval(fetchOrders, 5000); // Refresh every 5 seconds
});
