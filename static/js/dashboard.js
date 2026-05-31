function renderStudentDashboard() {
    const container = document.getElementById('appContent');
    container.innerHTML = `
        <div class="row">
        <div class="col-md-4">
            <h5>Новая заявка</h5>
            <form id="newOrderForm">
            <div class="mb-3">
                <label for="certType" class="form-label">Тип справки</label>
                <select class="form-select" id="certType">
                <option value="справка об обучении">Справка об обучении</option>
                <option value="справка для военкомата">Справка для военкомата</option>
                <option value="справка для соцзащиты">Справка для соцзащиты</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="reason" class="form-label">Примечание</label>
                <textarea class="form-control" id="reason" rows="2"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Отправить заявку</button>
            </form>
        </div>
        <div class="col-md-8">
            <h5>Мои заявки</h5>
            <div id="ordersTableContainer"></div>
        </div>
        </div>
    `;

    document.getElementById('newOrderForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const certificate_type = document.getElementById('certType').value;
        const reason = document.getElementById('reason').value;
        try {
        await apiRequest('/orders/', 'POST', { certificate_type, reason });
        alert('Заявка создана!');
        document.getElementById('newOrderForm').reset();
        loadOrders('student');
        } catch (err) {
        alert('Ошибка: ' + err.message);
        }
    });
    }

    function renderStaffDashboard() {
    const container = document.getElementById('appContent');
    container.innerHTML = `
        <h5>Все заявки студентов</h5>
        <div id="ordersTableContainer"></div>
    `;
    }

    async function loadOrders(role) {
    const endpoint = '/orders/';
    try {
        const orders = await apiRequest(endpoint, 'GET');
        const container = document.getElementById('ordersTableContainer');
        if (!orders.length) {
        container.innerHTML = '<p>Заявок пока нет.</p>';
        return;
        }
        let html = `
        <table class="table table-bordered table-striped">
            <thead>
            <tr>
                <th>ID</th>
                ${role === 'staff' ? '<th>Студент</th>' : ''}
                <th>Тип справки</th>
                <th>Примечание</th>
                <th>Статус</th>
                <th>Создана</th>
                ${role === 'staff' ? '<th>Действие</th>' : ''}
            </tr>
            </thead>
            <tbody>
        `;
        orders.forEach(order => {
        html += `<tr>
            <td>${order.id}</td>
            ${role === 'staff' ? `<td>${order.user.full_name}</td>` : ''}
            <td>${order.certificate_type}</td>
            <td>${order.reason || '-'}</td>
            <td><span class="badge bg-${order.status === 'готово' ? 'success' : order.status === 'выполняется' ? 'warning' : 'secondary'}">${order.status}</span></td>
            <td>${new Date(order.created_at).toLocaleString()}</td>
            ${role === 'staff' ? `<td>
            <select class="form-select form-select-sm change-status" data-order-id="${order.id}">
                <option value="принято" ${order.status === 'принято' ? 'selected' : ''}>Принято</option>
                <option value="выполняется" ${order.status === 'выполняется' ? 'selected' : ''}>Выполняется</option>
                <option value="готово" ${order.status === 'готово' ? 'selected' : ''}>Готово</option>
            </select>
            </td>` : ''}
        </tr>`;
        });
        html += '</tbody></table>';
        container.innerHTML = html;

        if (role === 'staff') {
        document.querySelectorAll('.change-status').forEach(select => {
            select.addEventListener('change', async (e) => {
            const orderId = e.target.dataset.orderId;
            const newStatus = e.target.value;
            try {
                await apiRequest(`/orders/${orderId}/status?new_status=${newStatus}`, 'PATCH');
                alert('Статус обновлён');
            } catch (err) {
                alert('Ошибка: ' + err.message);
            }
            });
        });
        }
    } catch (err) {
        console.error(err);
    }
}