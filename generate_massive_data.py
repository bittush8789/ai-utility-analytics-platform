import sqlite3
import random
import sys
import os
from datetime import datetime, timedelta

# Default Generation Dimensions (Scaled for instant evaluation, easily adjustable)
TOTAL_CUSTOMERS = 15000
TOTAL_INCIDENTS = 25000
TOTAL_COMPLAINTS = 20000
TOTAL_WORK_ORDERS = 18000
TOTAL_BILLING = 35000
TOTAL_PAYMENTS = 30000
TOTAL_ASSETS = 8000
TOTAL_METER_READINGS = 40000
TOTAL_EMPLOYEES = 2000
TOTAL_WATER_TESTS = 10000
TOTAL_AUDIT_LOGS = 12000
TOTAL_ALERTS_HISTORY = 6000
TOTAL_SUPPLIERS = 1500
TOTAL_INVENTORY = 4000
TOTAL_OUTAGE_EVENTS = 5000
TOTAL_MAINTENANCE = 4000
TOTAL_FEEDBACK = 8000

DB_PATH = "utility_analytics.db"

UK_REGIONS = [
    "Greater London", "South East England", "South West England", "West Midlands",
    "East Midlands", "North West England", "North East England", "Yorkshire",
    "Scotland", "Wales", "Northern Ireland"
]
UK_CITIES = [
    "London", "Manchester", "Birmingham", "Leeds", "Liverpool", "Bristol",
    "Sheffield", "Glasgow", "Edinburgh", "Cardiff", "Belfast", "Reading",
    "Oxford", "Cambridge", "Nottingham", "Leicester", "Coventry", "Luton",
    "Slough", "Southampton"
]
ZONES = [
    "North Zone", "South Zone", "East Zone", "West Zone", "Central Zone",
    "Metro Zone", "Rural Zone", "Industrial Zone", "Coastal Zone"
]

def recreate_db():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass
            
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables exactly matching enterprise schema requirements
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        full_name TEXT,
        email TEXT,
        role TEXT,
        region TEXT,
        is_active INTEGER DEFAULT 1,
        last_login TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        city TEXT,
        region TEXT,
        zone TEXT,
        customer_type TEXT,
        created_date TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_type TEXT,
        severity TEXT,
        city TEXT,
        region TEXT,
        zone TEXT,
        status TEXT,
        sla_hours REAL,
        report_date TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        complaint_type TEXT,
        priority TEXT,
        city TEXT,
        region TEXT,
        status TEXT,
        report_date TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_orders (
        wo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        engineer_name TEXT,
        task_type TEXT,
        status TEXT,
        estimated_hours REAL,
        actual_hours REAL,
        created_date TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS billing (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        region TEXT,
        amount REAL,
        paid_status TEXT,
        due_date TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        amount REAL,
        payment_date TEXT,
        payment_method TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_type TEXT,
        install_year INTEGER,
        health_score INTEGER,
        status TEXT,
        maintenance_cost REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meter_readings (
        reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        reading_value REAL,
        reading_date TEXT,
        anomaly_flag INTEGER DEFAULT 0
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        region TEXT,
        active_status INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS water_quality_tests (
        test_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        turbidity REAL,
        chlorine_level REAL,
        ph_level REAL,
        status TEXT,
        test_date TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kpi_daily (
        report_date TEXT PRIMARY KEY,
        total_incidents INTEGER,
        resolved_incidents INTEGER,
        complaints INTEGER,
        revenue REAL,
        sla_percent REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT,
        page TEXT,
        timestamp TEXT,
        status TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts_history (
        alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT,
        severity TEXT,
        message TEXT,
        alert_date TEXT
    );
    """)

    # NEW TABLES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_name TEXT,
        category TEXT,
        city TEXT,
        contract_value REAL,
        active_status INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_type TEXT,
        warehouse_city TEXT,
        stock_qty INTEGER,
        reorder_level INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS outage_events (
        outage_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        zone TEXT,
        start_time TEXT,
        end_time TEXT,
        affected_customers INTEGER,
        cause TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_schedule (
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id INTEGER,
        next_due_date TEXT,
        priority TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_feedback (
        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_date TEXT
    );
    """)

    conn.commit()
    conn.close()

def generate_bulk_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    start_date = datetime(2019, 1, 1)
    end_date = datetime.now()
    delta_days = (end_date - start_date).days
    
    # 1. Customers
    print("Generating Customers data...")
    customer_types = ["Residential", "Commercial", "Industrial", "Government"]
    c_list = []
    for i in range(1, TOTAL_CUSTOMERS + 1):
        city = random.choice(UK_CITIES)
        region = random.choice(UK_REGIONS)
        if city == "London":
            region = "Greater London"
        elif city in ["Manchester", "Liverpool"]:
            region = "North West England"
        c_list.append((
            f"Enterprise Account {i}",
            f"user_{i}@uk-utilities.com",
            city,
            region,
            random.choice(ZONES),
            random.choice(customer_types),
            (start_date + timedelta(days=random.randint(0, delta_days))).strftime("%Y-%m-%d")
        ))
    cursor.executemany("INSERT INTO customers (name, email, city, region, zone, customer_type, created_date) VALUES (?, ?, ?, ?, ?, ?, ?)", c_list)
    
    # 2. Employees
    print("Generating Employees...")
    emp_roles = ["Field Operations", "Support Rep", "Network Analyst", "Executive Officer"]
    emp_list = []
    for i in range(1, TOTAL_EMPLOYEES + 1):
        emp_list.append((f"Staff Worker {i}", random.choice(emp_roles), random.choice(UK_REGIONS), 1))
    cursor.executemany("INSERT INTO employees (name, role, region, active_status) VALUES (?, ?, ?, ?)", emp_list)

    # 3. Incidents
    print("Generating Incidents...")
    inc_types = ["Burst Pipe", "Pressure Loss", "Billing Anomaly", "Sewerage Overload", "Water Quality Alert"]
    sevs = ["Critical", "High", "Medium", "Low"]
    status_options = ["Resolved", "In Progress", "Pending"]
    inc_list = []
    for i in range(1, TOTAL_INCIDENTS + 1):
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        city = random.choice(UK_CITIES)
        region = random.choice(UK_REGIONS)
        # Seasonal logic
        if dt.month in [12, 1, 2] and random.random() < 0.35:
            inc_type = "Burst Pipe"
            sev = "Critical"
        else:
            inc_type = random.choice(inc_types)
            sev = random.choice(sevs)
            
        inc_list.append((
            inc_type,
            sev,
            city,
            region,
            random.choice(ZONES),
            random.choice(status_options),
            round(random.uniform(2, 72), 1),
            dt.strftime("%Y-%m-%d")
        ))
    cursor.executemany("INSERT INTO incidents (incident_type, severity, city, region, zone, status, sla_hours, report_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", inc_list)

    # 4. Complaints
    print("Generating Complaints...")
    comp_types = ["Interrupted Flow", "Low Water Pressure", "Incorrect Invoice", "Customer Service Issue"]
    comp_list = []
    for i in range(1, TOTAL_COMPLAINTS + 1):
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        comp_list.append((
            random.randint(1, TOTAL_CUSTOMERS),
            random.choice(comp_types),
            random.choice(["High", "Normal", "Low"]),
            random.choice(UK_CITIES),
            random.choice(UK_REGIONS),
            random.choice(["Resolved", "Open"]),
            dt.strftime("%Y-%m-%d")
        ))
    cursor.executemany("INSERT INTO complaints (customer_id, complaint_type, priority, city, region, status, report_date) VALUES (?, ?, ?, ?, ?, ?, ?)", comp_list)

    # 5. Work Orders
    print("Generating Work Orders...")
    wo_list = []
    for i in range(1, TOTAL_WORK_ORDERS + 1):
        est = round(random.uniform(1.5, 12.0), 1)
        # Weekend logic
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        act = est * (1.25 if dt.weekday() >= 5 else 0.95)
        wo_list.append((
            f"Engineer Profile {random.randint(1, 150)}",
            random.choice(["Mainline Repair", "Valve Installation", "Quality Inspection", "Billing Adjustments"]),
            random.choice(["Completed", "Pending", "Cancelled"]),
            est,
            round(act, 1),
            dt.strftime("%Y-%m-%d")
        ))
    cursor.executemany("INSERT INTO work_orders (engineer_name, task_type, status, estimated_hours, actual_hours, created_date) VALUES (?, ?, ?, ?, ?, ?)", wo_list)

    # 6. Billing & Payments
    print("Generating Billing & Payments...")
    bill_list = []
    pay_list = []
    for i in range(1, TOTAL_BILLING + 1):
        region = random.choice(UK_REGIONS)
        # RLS mapping
        amt = round(random.uniform(55, 3400), 2)
        paid = random.choice(["Paid", "Unpaid", "Overdue"])
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        bill_list.append((
            random.randint(1, TOTAL_CUSTOMERS),
            region,
            amt,
            paid,
            dt.strftime("%Y-%m-%d")
        ))
        
        # Immediate payment correlation
        if paid == "Paid" and i <= TOTAL_PAYMENTS:
            pay_list.append((
                i,
                amt,
                (dt + timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d"),
                random.choice(["Direct Debit", "BACS", "Debit Card", "Corporate Cheque"])
            ))
            
    cursor.executemany("INSERT INTO billing (customer_id, region, amount, paid_status, due_date) VALUES (?, ?, ?, ?, ?)", bill_list)
    cursor.executemany("INSERT INTO payments (invoice_id, amount, payment_date, payment_method) VALUES (?, ?, ?, ?)", pay_list)

    # 7. Assets
    print("Generating Assets...")
    a_types = ["Reservoir Tank", "Pressure Valve", "Main Water Pipe", "Pumping Substation"]
    asset_list = []
    for i in range(1, TOTAL_ASSETS + 1):
        year = random.randint(1955, 2024)
        health = random.randint(10, 100)
        # Relationship logic
        if 2026 - year > 25:
            health = max(10, health - random.randint(15, 45))
        
        cost = round((100 - health) * random.uniform(500, 1500), 2)
        asset_list.append((
            random.choice(a_types),
            year,
            health,
            random.choice(["Fully Operational", "Under Maintenance", "Requires Replacement"]),
            cost
        ))
    cursor.executemany("INSERT INTO assets (asset_type, install_year, health_score, status, maintenance_cost) VALUES (?, ?, ?, ?, ?)", asset_list)

    # 8. Meter Readings
    print("Generating Meter Readings...")
    readings = []
    for i in range(1, TOTAL_METER_READINGS + 1):
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        val = round(random.uniform(25, 1200), 2)
        anomaly = 1 if val > 1100 and random.random() < 0.05 else 0
        readings.append((
            random.randint(1, TOTAL_CUSTOMERS),
            val,
            dt.strftime("%Y-%m-%d"),
            anomaly
        ))
    cursor.executemany("INSERT INTO meter_readings (customer_id, reading_value, reading_date, anomaly_flag) VALUES (?, ?, ?, ?)", readings)

    # 9. KPI Daily
    print("Generating Daily KPI records...")
    kpi_list = []
    curr = start_date
    while curr <= end_date:
        kpi_list.append((
            curr.strftime("%Y-%m-%d"),
            random.randint(15, 65),
            random.randint(10, 55),
            random.randint(5, 35),
            round(random.uniform(12000, 95000), 2),
            round(random.uniform(85.5, 99.5), 2)
        ))
        curr += timedelta(days=1)
    cursor.executemany("INSERT INTO kpi_daily (report_date, total_incidents, resolved_incidents, complaints, revenue, sla_percent) VALUES (?, ?, ?, ?, ?, ?)", kpi_list)

    # 10. Audit Logs
    print("Generating Audit Logs...")
    audit_list = []
    actions = ["Login", "Query SQL", "Data Refresh", "Upload File", "Generate Report"]
    pages = ["Executive Dashboard", "AI SQL Copilot", "Forecasting", "Admin Panel"]
    users_options = ["admin", "ceo", "analyst", "ops_manager"]
    for i in range(1, TOTAL_AUDIT_LOGS + 1):
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        audit_list.append((
            random.choice(users_options),
            random.choice(actions),
            random.choice(pages),
            dt.strftime("%Y-%m-%d %H:%M:%S"),
            random.choice(["Success", "Denied"])
        ))
    cursor.executemany("INSERT INTO audit_logs (username, action, page, timestamp, status) VALUES (?, ?, ?, ?, ?)", audit_list)

    # 11. Alerts History
    print("Generating Alerts History...")
    alert_list = []
    for i in range(1, TOTAL_ALERTS_HISTORY + 1):
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        alert_list.append((
            random.choice(["System Breach", "Network Failure", "Pipeline Burst", "SLA Deviation"]),
            random.choice(["Critical", "High", "Warning"]),
            f"Alert registered for sector region zone {random.choice(ZONES)} on event volume.",
            dt.strftime("%Y-%m-%d")
        ))
    cursor.executemany("INSERT INTO alerts_history (alert_type, severity, message, alert_date) VALUES (?, ?, ?, ?)", alert_list)

    # 12. Suppliers
    print("Generating Suppliers data...")
    supp_list = []
    for i in range(1, TOTAL_SUPPLIERS + 1):
        supp_list.append((
            f"Corporate Supplier Group {i}",
            random.choice(["Pipelines & Engineering", "Logistics & Fleet", "Software & IT Services", "Water Treatment Chemicals"]),
            random.choice(UK_CITIES),
            round(random.uniform(50000, 2500000), 2),
            1 if random.random() > 0.1 else 0
        ))
    cursor.executemany("INSERT INTO suppliers (supplier_name, category, city, contract_value, active_status) VALUES (?, ?, ?, ?, ?)", supp_list)

    # 13. Inventory
    print("Generating Inventory data...")
    inv_list = []
    for i in range(1, TOTAL_INVENTORY + 1):
        inv_list.append((
            random.choice(a_types),
            random.choice(UK_CITIES),
            random.randint(50, 1500),
            random.randint(40, 450)
        ))
    cursor.executemany("INSERT INTO inventory (asset_type, warehouse_city, stock_qty, reorder_level) VALUES (?, ?, ?, ?)", inv_list)

    # 14. Outage Events
    print("Generating Outages data...")
    out_list = []
    for i in range(1, TOTAL_OUTAGE_EVENTS + 1):
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        out_list.append((
            random.choice(UK_CITIES),
            random.choice(ZONES),
            dt.strftime("%Y-%m-%d 08:00:00"),
            (dt + timedelta(hours=random.randint(1, 24))).strftime("%Y-%m-%d 18:00:00"),
            random.randint(15, 12000),
            random.choice(["Infrastructure Damage", "Scheduled Maintenance", "Extreme Weather", "Power Outage"])
        ))
    cursor.executemany("INSERT INTO outage_events (city, zone, start_time, end_time, affected_customers, cause) VALUES (?, ?, ?, ?, ?, ?)", out_list)

    # 15. Maintenance Schedule
    print("Generating Maintenance Schedule...")
    maint_list = []
    for i in range(1, TOTAL_MAINTENANCE + 1):
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        maint_list.append((
            random.randint(1, TOTAL_ASSETS),
            dt.strftime("%Y-%m-%d"),
            random.choice(["Critical", "High", "Normal"])
        ))
    cursor.executemany("INSERT INTO maintenance_schedule (asset_id, next_due_date, priority) VALUES (?, ?, ?)", maint_list)

    # 16. Customer Feedback
    print("Generating Customer Feedback...")
    feed_list = []
    feed_comments = [
        "Prompt service, the leak was repaired within hours.",
        "Billing was slightly confusing this quarter.",
        "Customer representative was incredibly polite.",
        "Experiencing slightly reduced water pressure during peak hours."
    ]
    for i in range(1, TOTAL_FEEDBACK + 1):
        dt = start_date + timedelta(days=random.randint(0, delta_days))
        feed_list.append((
            random.randint(1, TOTAL_CUSTOMERS),
            random.randint(1, 5),
            random.choice(feed_comments),
            dt.strftime("%Y-%m-%d")
        ))
    cursor.executemany("INSERT INTO customer_feedback (customer_id, rating, comment, created_date) VALUES (?, ?, ?, ?)", feed_list)

    # Adding default corporate users back!
    print("Enriching default clearance user profiles...")
    cursor.execute("""
    INSERT INTO users (username, password, full_name, email, role, region) VALUES 
    ('admin', 'admin123', 'System Administrator', 'admin@utility.com', 'Admin', 'All'),
    ('ceo', 'ceo123', 'Chief Executive Officer', 'ceo@utility.com', 'CEO', 'All'),
    ('ops_manager', 'ops123', 'Operations Manager', 'ops@utility.com', 'Operations Manager', 'London'),
    ('analyst', 'analyst123', 'Principal Data Analyst', 'analyst@utility.com', 'Data Analyst', 'All'),
    ('finance', 'fin123', 'Finance Manager', 'finance@utility.com', 'Finance Manager', 'London'),
    ('engineer', 'eng123', 'Field Operations Engineer', 'engineer@utility.com', 'Field Engineer', 'London'),
    ('support', 'sup123', 'Customer Support Lead', 'support@utility.com', 'Customer Support Lead', 'All'),
    ('viewer', 'view123', 'Viewer Guest', 'viewer@utility.com', 'Viewer / Guest', 'All');
    """)

    # Index optimization
    print("Indexing core operational query vectors...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_customers_region ON customers(region);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_customers_city ON customers(city);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_incidents_report_date ON incidents(report_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_incidents_region ON incidents(region);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_complaints_customer_id ON complaints(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_billing_region ON billing(region);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_billing_paid ON billing(paid_status);")

    conn.commit()
    conn.close()
    print("Database fully compiled, populated, and indexed perfectly!")

if __name__ == "__main__":
    recreate_db()
    generate_bulk_data()
