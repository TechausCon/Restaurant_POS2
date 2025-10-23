document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    document.getElementById('logout-button').addEventListener('click', logout);

    const ordersContainer = document.getElementById('orders-container');
    const ws = new WebSocket(`ws://localhost:8000/ws`);
    let orders = [];

    ws.onmessage = function(event) {
        const orderData = JSON.parse(event.data);
        const index = orders.findIndex(o => o.id === orderData.id);
        if (index > -1) {
            orders[index] = orderData;
        } else {
            orders.push(orderData);
        }
        renderOrders();
    };

    function renderOrders() {
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
                fetchWithAuth(`/orders/${order.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: statusSelect.value })
                });
            });
            orderCard.appendChild(statusSelect);

            ordersContainer.appendChild(orderCard);
        });
    }

    fetchWithAuth('/orders/')
        .then(response => response.json())
        .then(initialOrders => {
            orders = initialOrders;
            renderOrders();
        });
});
