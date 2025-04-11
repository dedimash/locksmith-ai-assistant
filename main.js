// Main JavaScript for Locksmith AI Assistant

document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function() {
            document.getElementById('sidebar').classList.toggle('active');
        });
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Make call log table rows clickable
    const callTableRows = document.querySelectorAll('.call-table tbody tr');
    callTableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            const url = this.dataset.url;
            if (url) {
                window.location.href = url;
            }
        });
    });
});

// Function to load dashboard statistics via API
function loadDashboardStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateDashboardStats(data.data);
                createServiceChart(data.data.service_types);
                createCallsChart(data.data.calls_by_day);
            }
        })
        .catch(error => console.error('Error loading dashboard stats:', error));
}

// Function to update dashboard statistics
function updateDashboardStats(data) {
    const totalCallsElement = document.getElementById('total-calls');
    if (totalCallsElement) {
        totalCallsElement.textContent = data.total_calls;
    }
}

// Function to create service type chart
function createServiceChart(serviceTypes) {
    const ctx = document.getElementById('serviceChart');
    if (!ctx) return;

    const labels = Object.keys(serviceTypes);
    const data = Object.values(serviceTypes);
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#007bff',
                    '#28a745',
                    '#ffc107',
                    '#dc3545',
                    '#6c757d',
                    '#17a2b8'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Service Types'
                }
            }
        }
    });
}

// Function to create calls by day chart
function createCallsChart(callsByDay) {
    const ctx = document.getElementById('callsChart');
    if (!ctx) return;

    const labels = Object.keys(callsByDay).reverse();
    const data = Object.values(callsByDay).reverse();
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Calls per Day',
                data: data,
                backgroundColor: '#007bff'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Calls by Day'
                }
            }
        }
    });
}
