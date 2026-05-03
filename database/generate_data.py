import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

def random_dates(start, end, n=10):
    start_u = start.value // 10**9
    end_u = end.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

def generate_all_data(db_path):
    print(f"Connecting to DB at {db_path}...")
    # Remove existing db to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    
    # Settings
    N_CUSTOMERS = 250000
    N_INCIDENTS = 700000
    N_COMPLAINTS = 600000
    N_WORK_ORDERS = 500000
    N_BILLING = 1200000
    N_PAYMENTS = 1000000
    N_ASSETS = 120000
    N_METER_READINGS = 2500000
    N_EMPLOYEES = 25000
    N_WATER_TESTS = 200000
    N_KPI_DAILY = 1825 # 5 years
    
    COUNTRIES = ['United Kingdom']
    REGIONS = ['Greater London', 'South East England', 'West Midlands', 'North West England', 'Scotland', 'Wales', 'Northern Ireland', 'Yorkshire', 'East Midlands', 'South West England']
    CITIES = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Liverpool', 'Bristol', 'Oxford', 'Reading', 'Cambridge', 'Sheffield', 'Glasgow', 'Edinburgh', 'Cardiff', 'Belfast', 'Nottingham', 'Leicester']
    ZONES = ['North Zone', 'South Zone', 'East Zone', 'West Zone', 'Central Zone', 'Metro Zone', 'Rural Zone', 'Industrial Zone']
    
    start_date = pd.to_datetime('2019-01-01')
    end_date = pd.to_datetime('2023-12-31')
    
    print("1. Generating Customers...")
    customers = pd.DataFrame({
        'customer_id': np.arange(1, N_CUSTOMERS + 1),
        'customer_name': [f"Customer_{i}" for i in range(1, N_CUSTOMERS + 1)],
        'country': np.random.choice(COUNTRIES, N_CUSTOMERS),
        'region': np.random.choice(REGIONS, N_CUSTOMERS),
        'city': np.random.choice(CITIES, N_CUSTOMERS),
        'zone': np.random.choice(ZONES, N_CUSTOMERS),
        'account_type': np.random.choice(['Residential', 'Commercial', 'Industrial'], N_CUSTOMERS, p=[0.8, 0.15, 0.05]),
        'join_date': random_dates(start_date, end_date, N_CUSTOMERS).strftime('%Y-%m-%d'),
        'status': np.random.choice(['Active', 'Inactive'], N_CUSTOMERS, p=[0.95, 0.05])
    })
    customers.to_sql('customers', conn, index=False, if_exists='replace')
    
    print("2. Generating Incidents...")
    incident_types = ['Leak', 'Burst Pipe', 'Low Pressure', 'No Water', 'Contamination']
    incidents = pd.DataFrame({
        'incident_id': np.arange(1, N_INCIDENTS + 1),
        'incident_type': np.random.choice(incident_types, N_INCIDENTS, p=[0.4, 0.2, 0.2, 0.15, 0.05]),
        'severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'], N_INCIDENTS),
        'country': np.random.choice(COUNTRIES, N_INCIDENTS),
        'region': np.random.choice(REGIONS, N_INCIDENTS),
        'city': np.random.choice(CITIES, N_INCIDENTS),
        'zone': np.random.choice(ZONES, N_INCIDENTS),
        'status': np.random.choice(['Resolved', 'Open', 'In Progress'], N_INCIDENTS, p=[0.9, 0.05, 0.05]),
        'created_date': random_dates(start_date, end_date, N_INCIDENTS).strftime('%Y-%m-%d %H:%M:%S'),
        'affected_customers': np.random.randint(1, 1000, N_INCIDENTS),
        'sla_hours': np.random.randint(2, 48, N_INCIDENTS)
    })
    # Add resolved date based on status
    incidents['resolved_date'] = np.where(incidents['status'] == 'Resolved', 
                                          (pd.to_datetime(incidents['created_date']) + pd.to_timedelta(np.random.randint(1, 72, N_INCIDENTS), unit='h')).dt.strftime('%Y-%m-%d %H:%M:%S'),
                                          None)
    incidents.to_sql('incidents', conn, index=False, if_exists='replace')
    
    print("3. Generating Complaints...")
    complaints = pd.DataFrame({
        'complaint_id': np.arange(1, N_COMPLAINTS + 1),
        'customer_id': np.random.randint(1, N_CUSTOMERS + 1, N_COMPLAINTS),
        'complaint_type': np.random.choice(['Billing', 'Pressure', 'Quality', 'Service', 'Other'], N_COMPLAINTS),
        'priority': np.random.choice(['Low', 'Medium', 'High'], N_COMPLAINTS),
        'country': np.random.choice(COUNTRIES, N_COMPLAINTS),
        'region': np.random.choice(REGIONS, N_COMPLAINTS),
        'city': np.random.choice(CITIES, N_COMPLAINTS),
        'zone': np.random.choice(ZONES, N_COMPLAINTS),
        'status': np.random.choice(['Closed', 'Open'], N_COMPLAINTS, p=[0.95, 0.05]),
        'created_date': random_dates(start_date, end_date, N_COMPLAINTS).strftime('%Y-%m-%d %H:%M:%S')
    })
    complaints['closed_date'] = np.where(complaints['status'] == 'Closed',
                                         (pd.to_datetime(complaints['created_date']) + pd.to_timedelta(np.random.randint(1, 14, N_COMPLAINTS), unit='D')).dt.strftime('%Y-%m-%d %H:%M:%S'),
                                         None)
    complaints.to_sql('complaints', conn, index=False, if_exists='replace')
    
    print("4. Generating Work Orders...")
    work_orders = pd.DataFrame({
        'work_id': np.arange(1, N_WORK_ORDERS + 1),
        'engineer_id': np.random.randint(1, N_EMPLOYEES + 1, N_WORK_ORDERS),
        'engineer_name': [f"Engineer_{np.random.randint(1, 1000)}" for _ in range(N_WORK_ORDERS)],
        'task_type': np.random.choice(['Repair', 'Inspection', 'Installation', 'Maintenance'], N_WORK_ORDERS),
        'priority': np.random.choice(['Low', 'Medium', 'High', 'Urgent'], N_WORK_ORDERS),
        'country': np.random.choice(COUNTRIES, N_WORK_ORDERS),
        'region': np.random.choice(REGIONS, N_WORK_ORDERS),
        'city': np.random.choice(CITIES, N_WORK_ORDERS),
        'zone': np.random.choice(ZONES, N_WORK_ORDERS),
        'status': np.random.choice(['Completed', 'Pending', 'In Progress'], N_WORK_ORDERS, p=[0.9, 0.05, 0.05]),
        'assigned_date': random_dates(start_date, end_date, N_WORK_ORDERS).strftime('%Y-%m-%d %H:%M:%S'),
        'estimated_hours': np.random.randint(1, 24, N_WORK_ORDERS),
        'actual_hours': np.random.randint(1, 30, N_WORK_ORDERS)
    })
    work_orders['completed_date'] = np.where(work_orders['status'] == 'Completed',
                                            (pd.to_datetime(work_orders['assigned_date']) + pd.to_timedelta(work_orders['actual_hours'], unit='h')).dt.strftime('%Y-%m-%d %H:%M:%S'),
                                            None)
    work_orders.to_sql('work_orders', conn, index=False, if_exists='replace')

    print("5. Generating Billing...")
    billing = pd.DataFrame({
        'invoice_id': np.arange(1, N_BILLING + 1),
        'customer_id': np.random.randint(1, N_CUSTOMERS + 1, N_BILLING),
        'country': np.random.choice(COUNTRIES, N_BILLING),
        'region': np.random.choice(REGIONS, N_BILLING),
        'city': np.random.choice(CITIES, N_BILLING),
        'zone': np.random.choice(ZONES, N_BILLING),
        'amount': np.round(np.random.uniform(20.0, 500.0, N_BILLING), 2),
        'due_date': random_dates(start_date, end_date, N_BILLING).strftime('%Y-%m-%d'),
        'paid_status': np.random.choice(['Paid', 'Unpaid', 'Overdue'], N_BILLING, p=[0.8, 0.1, 0.1])
    })
    billing['payment_date'] = np.where(billing['paid_status'] == 'Paid',
                                      (pd.to_datetime(billing['due_date']) - pd.to_timedelta(np.random.randint(1, 15, N_BILLING), unit='D')).dt.strftime('%Y-%m-%d'),
                                      None)
    billing.to_sql('billing', conn, index=False, if_exists='replace')
    
    print("6. Generating Payments...")
    payments = pd.DataFrame({
        'payment_id': np.arange(1, N_PAYMENTS + 1),
        'invoice_id': np.random.randint(1, N_BILLING + 1, N_PAYMENTS),
        'customer_id': np.random.randint(1, N_CUSTOMERS + 1, N_PAYMENTS),
        'amount': np.round(np.random.uniform(20.0, 500.0, N_PAYMENTS), 2),
        'payment_mode': np.random.choice(['Credit Card', 'Bank Transfer', 'Direct Debit', 'Cash'], N_PAYMENTS),
        'payment_date': random_dates(start_date, end_date, N_PAYMENTS).strftime('%Y-%m-%d'),
        'status': np.random.choice(['Success', 'Failed', 'Pending'], N_PAYMENTS, p=[0.9, 0.08, 0.02])
    })
    payments.to_sql('payments', conn, index=False, if_exists='replace')

    print("7. Generating Assets...")
    assets = pd.DataFrame({
        'asset_id': np.arange(1, N_ASSETS + 1),
        'asset_type': np.random.choice(['Pipe', 'Pump', 'Valve', 'Meter', 'Treatment Plant'], N_ASSETS),
        'country': np.random.choice(COUNTRIES, N_ASSETS),
        'region': np.random.choice(REGIONS, N_ASSETS),
        'city': np.random.choice(CITIES, N_ASSETS),
        'zone': np.random.choice(ZONES, N_ASSETS),
        'install_year': np.random.randint(1970, 2023, N_ASSETS),
        'health_score': np.random.randint(10, 100, N_ASSETS),
        'maintenance_cost': np.round(np.random.uniform(100.0, 10000.0, N_ASSETS), 2),
        'status': np.random.choice(['Active', 'Under Repair', 'Decommissioned'], N_ASSETS, p=[0.9, 0.08, 0.02])
    })
    assets.to_sql('assets', conn, index=False, if_exists='replace')
    
    print("8. Generating Meter Readings...")
    meter_readings = pd.DataFrame({
        'reading_id': np.arange(1, N_METER_READINGS + 1),
        'customer_id': np.random.randint(1, N_CUSTOMERS + 1, N_METER_READINGS),
        'reading_date': random_dates(start_date, end_date, N_METER_READINGS).strftime('%Y-%m-%d'),
        'usage_liters': np.round(np.random.uniform(1000.0, 50000.0, N_METER_READINGS), 2),
        'anomaly_flag': np.random.choice([0, 1], N_METER_READINGS, p=[0.98, 0.02])
    })
    meter_readings.to_sql('meter_readings', conn, index=False, if_exists='replace')

    print("9. Generating Employees...")
    employees = pd.DataFrame({
        'employee_id': np.arange(1, N_EMPLOYEES + 1),
        'employee_name': [f"Employee_{i}" for i in range(1, N_EMPLOYEES + 1)],
        'role': np.random.choice(['Engineer', 'Manager', 'Analyst', 'Support', 'Technician'], N_EMPLOYEES),
        'department': np.random.choice(['Operations', 'Maintenance', 'Customer Service', 'IT', 'Finance'], N_EMPLOYEES),
        'region': np.random.choice(REGIONS, N_EMPLOYEES),
        'city': np.random.choice(CITIES, N_EMPLOYEES),
        'zone': np.random.choice(ZONES, N_EMPLOYEES),
        'join_date': random_dates(pd.to_datetime('2010-01-01'), end_date, N_EMPLOYEES).strftime('%Y-%m-%d'),
        'status': np.random.choice(['Active', 'On Leave', 'Terminated'], N_EMPLOYEES, p=[0.9, 0.05, 0.05])
    })
    employees.to_sql('employees', conn, index=False, if_exists='replace')
    
    print("10. Generating Water Quality Tests...")
    water_tests = pd.DataFrame({
        'test_id': np.arange(1, N_WATER_TESTS + 1),
        'zone': np.random.choice(ZONES, N_WATER_TESTS),
        'city': np.random.choice(CITIES, N_WATER_TESTS),
        'sample_date': random_dates(start_date, end_date, N_WATER_TESTS).strftime('%Y-%m-%d'),
        'ph_level': np.round(np.random.normal(7.2, 0.5, N_WATER_TESTS), 2),
        'chlorine_level': np.round(np.random.normal(1.0, 0.3, N_WATER_TESTS), 2),
        'contamination_flag': np.random.choice([0, 1], N_WATER_TESTS, p=[0.99, 0.01])
    })
    water_tests.to_sql('water_quality_tests', conn, index=False, if_exists='replace')

    print("11. Generating KPI Daily...")
    dates = pd.date_range(start=start_date, periods=N_KPI_DAILY, freq='D')
    kpi_daily = pd.DataFrame({
        'report_date': dates.strftime('%Y-%m-%d'),
        'total_incidents': np.random.randint(50, 500, N_KPI_DAILY),
        'resolved_incidents': np.random.randint(40, 480, N_KPI_DAILY),
        'complaints': np.random.randint(100, 800, N_KPI_DAILY),
        'revenue': np.round(np.random.uniform(50000.0, 500000.0, N_KPI_DAILY), 2),
        'sla_percent': np.round(np.random.uniform(85.0, 99.9, N_KPI_DAILY), 2)
    })
    kpi_daily.to_sql('kpi_daily', conn, index=False, if_exists='replace')

    # Create Indexes for performance
    print("12. Creating Indexes...")
    conn.execute("CREATE INDEX idx_customers_city ON customers(city);")
    conn.execute("CREATE INDEX idx_incidents_date ON incidents(created_date);")
    conn.execute("CREATE INDEX idx_incidents_status ON incidents(status);")
    conn.execute("CREATE INDEX idx_complaints_date ON complaints(created_date);")
    conn.execute("CREATE INDEX idx_billing_status ON billing(paid_status);")
    
    conn.commit()
    conn.close()
    print("Database Generation Complete!")

if __name__ == "__main__":
    generate_all_data("utility_analytics.db")
