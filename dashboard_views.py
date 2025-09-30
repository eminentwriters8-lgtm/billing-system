# Create the enhanced admin_dashboard.html template
python -c "
content = '''
{% extends \"base.html\" %}

{% block content %}
<div class=\"row mb-4\">
    <div class=\"col-12\">
        <h1>📊 Dashboard Overview</h1>
        <p class=\"text-muted\">Africa Online Networks - Administrator Dashboard</p>
    </div>
</div>

<!-- Alert Panels -->
{% if expiring_soon or overdue_clients %}
<div class=\"row mb-4\">
    {% if overdue_clients %}
    <div class=\"col-md-6 mb-3\">
        <div class=\"card border-danger\">
            <div class=\"card-header bg-danger text-white\">
                <h5 class=\"mb-0\">⚠️ Overdue Clients: {{ overdue_clients|length }}</h5>
            </div>
            <div class=\"card-body\">
                {% for client in overdue_clients %}
                <div class=\"d-flex justify-content-between align-items-center mb-2\">
                    <div>
                        <strong>{{ client.user.get_full_name|default:client.user.username }}</strong>
                        <small class=\"d-block text-muted\">Due: {{ client.next_billing_date }}</small>
                    </div>
                    <span class=\"badge bg-danger\">OVERDUE</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    {% endif %}
    
    {% if expiring_soon %}
    <div class=\"col-md-6 mb-3\">
        <div class=\"card border-warning\">
            <div class=\"card-header bg-warning text-white\">
                <h5 class=\"mb-0\">🔔 Expiring Soon: {{ expiring_soon|length }}</h5>
            </div>
            <div class=\"card-body\">
                {% for client in expiring_soon %}
                <div class=\"d-flex justify-content-between align-items-center mb-2\">
                    <div>
                        <strong>{{ client.user.get_full_name|default:client.user.username }}</strong>
                        <small class=\"d-block text-muted\">Expires: {{ client.next_billing_date }}</small>
                    </div>
                    <span class=\"badge bg-warning\">Due soon</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    {% endif %}
</div>
{% endif %}

<!-- Statistics Cards -->
<div class=\"row mb-4\">
    <div class=\"col-md-2 mb-3\">
        <div class=\"card bg-primary text-white\">
            <div class=\"card-body text-center\">
                <h2>{{ total_clients }}</h2>
                <p class=\"mb-0\">Total Clients</p>
            </div>
        </div>
    </div>
    <div class=\"col-md-2 mb-3\">
        <div class=\"card bg-success text-white\">
            <div class=\"card-body text-center\">
                <h2>{{ active_clients }}</h2>
                <p class=\"mb-0\">Active</p>
            </div>
        </div>
    </div>
    <div class=\"col-md-2 mb-3\">
        <div class=\"card bg-warning text-white\">
            <div class=\"card-body text-center\">
                <h2>{{ suspended_clients }}</h2>
                <p class=\"mb-0\">Suspended</p>
            </div>
        </div>
    </div>
    <div class=\"col-md-3 mb-3\">
        <div class=\"card bg-info text-white\">
            <div class=\"card-body text-center\">
                <h2>KSH {{ monthly_revenue }}</h2>
                <p class=\"mb-0\">Monthly Revenue</p>
            </div>
        </div>
    </div>
    <div class=\"col-md-3 mb-3\">
        <div class=\"card bg-dark text-white\">
            <div class=\"card-body text-center\">
                <h2>KSH {{ yearly_revenue.total|default:0 }}</h2>
                <p class=\"mb-0\">Yearly Revenue</p>
            </div>
        </div>
    </div>
</div>

<div class=\"row\">
    <!-- Service Analytics & Revenue Section -->
    <div class=\"col-md-8 mb-4\">
        <!-- Yearly Revenue with Quarterly Breakdown -->
        <div class=\"card mb-4\">
            <div class=\"card-header\">
                <h5 class=\"mb-0\">💰 Yearly Revenue Analysis ({{ current_year }})</h5>
            </div>
            <div class=\"card-body\">
                <div class=\"row mb-4\">
                    <div class=\"col-md-3 text-center\">
                        <div class=\"border rounded p-3\">
                            <h6 class=\"text-primary\">Q1</h6>
                            <h4>KSH {{ yearly_revenue.q1|default:0 }}</h4>
                            <small class=\"text-muted\">Jan - Mar</small>
                        </div>
                    </div>
                    <div class=\"col-md-3 text-center\">
                        <div class=\"border rounded p-3\">
                            <h6 class=\"text-success\">Q2</h6>
                            <h4>KSH {{ yearly_revenue.q2|default:0 }}</h4>
                            <small class=\"text-muted\">Apr - Jun</small>
                        </div>
                    </div>
                    <div class=\"col-md-3 text-center\">
                        <div class=\"border rounded p-3\">
                            <h6 class=\"text-warning\">Q3</h6>
                            <h4>KSH {{ yearly_revenue.q3|default:0 }}</h4>
                            <small class=\"text-muted\">Jul - Sep</small>
                        </div>
                    </div>
                    <div class=\"col-md-3 text-center\">
                        <div class=\"border rounded p-3\">
                            <h6 class=\"text-danger\">Q4</h6>
                            <h4>KSH {{ yearly_revenue.q4|default:0 }}</h4>
                            <small class=\"text-muted\">Oct - Dec</small>
                        </div>
                    </div>
                </div>
                
                <!-- Quarter-over-Quarter Growth -->
                <div class=\"row\">
                    <div class=\"col-12\">
                        <h6>📈 Quarter-over-Quarter Growth</h6>
                        <div class=\"table-responsive\">
                            <table class=\"table table-sm table-bordered\">
                                <thead class=\"table-light\">
                                    <tr>
                                        <th>Quarter</th>
                                        <th>Revenue</th>
                                        <th>Growth</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for growth in quarterly_growth %}
                                    <tr>
                                        <td><strong>{{ growth.quarter }}</strong></td>
                                        <td>KSH {{ growth.revenue }}</td>
                                        <td>
                                            <span class=\"{% if growth.growth >= 0 %}text-success{% else %}text-danger{% endif %}\">
                                                {{ growth.growth }}%
                                            </span>
                                        </td>
                                        <td>
                                            <span class=\"badge bg-{% if growth.growth >= 0 %}success{% else %}danger{% endif %}\">
                                                {% if growth.growth >= 0 %}↑ Growth{% else %}↓ Decline{% endif %}
                                            </span>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Service Analytics -->
        <div class=\"card mb-4\">
            <div class=\"card-header\">
                <h5 class=\"mb-0\">📈 Service Analytics</h5>
            </div>
            <div class=\"card-body\">
                <div class=\"row\">
                    {% for stat in service_stats %}
                    <div class=\"col-md-6 mb-3\">
                        <div class=\"card\">
                            <div class=\"card-body\">
                                <h6>{{ stat.service_type }}</h6>
                                <div class=\"d-flex justify-content-between\">
                                    <span class=\"text-muted\">Clients</span>
                                    <strong>{{ stat.count }}</strong>
                                </div>
                                <div class=\"d-flex justify-content-between\">
                                    <span class=\"text-muted\">Revenue</span>
                                    <strong>KSH {{ stat.revenue }}</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <!-- Simple Revenue Chart -->
                <div class=\"mt-4\">
                    <h6>Revenue Trend (Last 6 Months)</h6>
                    <div class=\"chart-container\" style=\"height: 200px;\">
                        <div class=\"d-flex align-items-end\" style=\"height: 150px; gap: 10px;\">
                            {% for month in monthly_trend %}
                            <div class=\"d-flex flex-column align-items-center\" style=\"flex: 1;\">
                                <div class=\"bg-primary rounded\" style=\"width: 30px; height: {{ month.revenue|floatformat:0|default:50 }}px; max-height: 100px;\"></div>
                                <small class=\"mt-1\">{{ month.month }}</small>
                                <small class=\"text-muted\">KSH {{ month.revenue|floatformat:0 }}</small>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Data Usage & Bandwidth Monitoring -->
        <div class=\"card\">
            <div class=\"card-header\">
                <h5 class=\"mb-0\">🌐 Data Usage & Bandwidth Monitoring</h5>
            </div>
            <div class=\"card-body\">
                <!-- Overall Bandwidth Usage -->
                <div class=\"row mb-4\">
                    <div class=\"col-md-6\">
                        <h6>Total Bandwidth Usage</h6>
                        <div class=\"progress\" style=\"height: 25px;\">
                            <div class=\"progress-bar bg-success\" role=\"progressbar\" 
                                 style=\"width: {{ bandwidth_stats.usage_percentage }}%\"
                                 aria-valuenow=\"{{ bandwidth_stats.usage_percentage }}\" 
                                 aria-valuemin=\"0\" 
                                 aria-valuemax=\"100\">
                                {{ bandwidth_stats.usage_percentage }}%
                            </div>
                        </div>
                        <small class=\"text-muted\">
                            {{ bandwidth_stats.used|default:\"0\" }} GB / {{ bandwidth_stats.total|default:\"0\" }} GB
                        </small>
                    </div>
                    <div class=\"col-md-6\">
                        <h6>Peak Usage Times</h6>
                        <div class=\"list-group list-group-flush\">
                            <div class=\"list-group-item px-0 d-flex justify-content-between\">
                                <span>Morning (6AM-12PM)</span>
                                <span class=\"badge bg-info\">{{ bandwidth_stats.peak_morning|default:\"0\" }}%</span>
                            </div>
                            <div class=\"list-group-item px-0 d-flex justify-content-between\">
                                <span>Afternoon (12PM-6PM)</span>
                                <span class=\"badge bg-warning\">{{ bandwidth_stats.peak_afternoon|default:\"0\" }}%</span>
                            </div>
                            <div class=\"list-group-item px-0 d-flex justify-content-between\">
                                <span>Evening (6PM-12AM)</span>
                                <span class=\"badge bg-danger\">{{ bandwidth_stats.peak_evening|default:\"0\" }}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Top Data Users -->
                <h6>📊 Top Data Users (This Month)</h6>
                <div class=\"table-responsive\">
                    <table class=\"table table-sm table-striped\">
                        <thead class=\"table-light\">
                            <tr>
                                <th>Client</th>
                                <th>Service</th>
                                <th>Data Used</th>
                                <th>Limit</th>
                                <th>Usage %</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for user in top_data_users %}
                            <tr>
                                <td>
                                    <strong>{{ user.client_name|truncatechars:15 }}</strong>
                                </td>
                                <td>{{ user.service_type }}</td>
                                <td>{{ user.data_used }} GB</td>
                                <td>{{ user.data_limit }} GB</td>
                                <td>
                                    <div class=\"progress\" style=\"height: 15px;\">
                                        <div class=\"progress-bar {% if user.usage_percentage > 90 %}bg-danger{% elif user.usage_percentage > 75 %}bg-warning{% else %}bg-success{% endif %}\" 
                                             role=\"progressbar\" 
                                             style=\"width: {{ user.usage_percentage }}%\"
                                             aria-valuenow=\"{{ user.usage_percentage }}\" 
                                             aria-valuemin=\"0\" 
                                             aria-valuemax=\"100\">
                                        </div>
                                    </div>
                                    <small>{{ user.usage_percentage }}%</small>
                                </td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan=\"5\" class=\"text-center text-muted\">No data usage records found</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Quick Actions & Recent Activity -->
    <div class=\"col-md-4 mb-4\">
        <!-- Quick Actions -->
        <div class=\"card mb-4\">
            <div class=\"card-header\">
                <h5 class=\"mb-0\">⚡ Quick Actions</h5>
            </div>
            <div class=\"card-body\">
                <div class=\"d-grid gap-2\">
                    <a href=\"/admin/clients/client/add/\" class=\"btn btn-success btn-sm\">➕ Add New Client</a>
                    <a href=\"/admin/clients/serviceplan/add/\" class=\"btn btn-primary btn-sm\">📋 Manage Plans</a>
                    <a href=\"/clients/\" class=\"btn btn-info btn-sm\">👥 View All Clients</a>
                    <a href=\"/clients/sms/compose/\" class=\"btn btn-warning btn-sm\">📱 Send SMS</a>
                    <a href=\"/admin/\" class=\"btn btn-secondary btn-sm\">⚙️ Admin Panel</a>
                </div>
            </div>
        </div>

        <!-- Recent Payments -->
        <div class=\"card mb-4\">
            <div class=\"card-header\">
                <h5 class=\"mb-0\">💰 Recent Payments</h5>
            </div>
            <div class=\"card-body\">
                {% if recent_payments %}
                <div class=\"list-group list-group-flush\">
                    {% for payment in recent_payments %}
                    <div class=\"list-group-item px-0\">
                        <div class=\"d-flex w-100 justify-content-between\">
                            <h6 class=\"mb-1\">{{ payment.client.user.username|truncatechars:12 }}</h6>
                            <small>KSH {{ payment.amount }}</small>
                        </div>
                        <small class=\"text-muted\">{{ payment.payment_date|date:\"M d\" }} • 
                            <span class=\"badge bg-{% if payment.status == 'Completed' %}success{% else %}warning{% endif %}\">
                                {{ payment.status }}
                            </span>
                        </small>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <p class=\"text-muted text-center\">No recent payments</p>
                {% endif %}
            </div>
        </div>

        <!-- Bandwidth Alerts -->
        <div class=\"card\">
            <div class=\"card-header\">
                <h5 class=\"mb-0\">🚨 Bandwidth Alerts</h5>
            </div>
            <div class=\"card-body\">
                {% if bandwidth_alerts %}
                <div class=\"list-group list-group-flush\">
                    {% for alert in bandwidth_alerts %}
                    <div class=\"list-group-item px-0\">
                        <div class=\"d-flex w-100 justify-content-between align-items-start\">
                            <div>
                                <h6 class=\"mb-1\">{{ alert.client_name }}</h6>
                                <small class=\"text-muted\">{{ alert.service_type }}</small>
                            </div>
                            <span class=\"badge bg-{% if alert.alert_type == 'high_usage' %}warning{% else %}danger{% endif %}\">
                                {{ alert.usage_percentage }}%
                            </span>
                        </div>
                        <div class=\"progress mt-2\" style=\"height: 8px;\">
                            <div class=\"progress-bar {% if alert.usage_percentage > 90 %}bg-danger{% else %}bg-warning{% endif %}\" 
                                 style=\"width: {{ alert.usage_percentage }}%\">
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <p class=\"text-muted text-center\">No bandwidth alerts</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<!-- Support Information -->
<div class=\"row mt-4\">
    <div class=\"col-12\">
        <div class=\"card border-info\">
            <div class=\"card-header bg-info text-white\">
                <h5 class=\"mb-0\">🛠️ Technical Support</h5>
            </div>
            <div class=\"card-body\">
                <div class=\"row text-center\">
                    <div class=\"col-md-4 mb-3\">
                        <div class=\"border rounded p-3\">
                            <h4>📞</h4>
                            <h5>Call Support</h5>
                            <p class=\"mb-1\">
                                <a href=\"tel:0706315742\" class=\"btn btn-outline-primary btn-sm\">
                                    0706315742
                                </a>
                            </p>
                            <small class=\"text-muted\">Martin Mutinda</small>
                        </div>
                    </div>
                    <div class=\"col-md-4 mb-3\">
                        <div class=\"border rounded p-3\">
                            <h4>✉️</h4>
                            <h5>Email Support</h5>
                            <p class=\"mb-1\">
                                <a href=\"mailto:martinmutinda095@gmail.com\" class=\"btn btn-outline-success btn-sm\">
                                    Send Email
                                </a>
                            </p>
                            <small class=\"text-muted\">Quick Response</small>
                        </div>
                    </div>
                    <div class=\"col-md-4 mb-3\">
                        <div class=\"border rounded p-3\">
                            <h4>🌐</h4>
                            <h5>System Info</h5>
                            <p class=\"mb-1\">
                                <strong>Version:</strong> 2.0
                            </p>
                            <small class=\"text-muted\">&copy; 2025 Martin Mutinda</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# Create the templates directory if it doesn't exist
import os
os.makedirs('templates/dashboard', exist_ok=True)

# Write the template file
with open('templates/dashboard/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Created enhanced admin dashboard template')
"