from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pymysql
from pymysql.err import OperationalError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# List of usernames and passwords
credentials = [
    {"username": "SBOVDBN5591476", "password": "Nithish@123"},
    {"username": "SBOVDBN55205229", "password": "Ramya@2023"},
    {"username": "SBOVDBN5575582", "password": "Kathiravan@1682"},
    {"username": "SBOVDBN5593148", "password": "Kavin@123"},
    {"username": "SBOVDBN55221334", "password": "Ramani@2003"},
    {"username": "SBOVDBN55278247", "password": "Sarathi@2003"},
    {"username": "SBOVDBN55285206", "password": "Ramya@2003"},
    {"username": "SBOVDBN55271922", "password": "Abi@2005"},
    {"username": "SBOVDBN55272194", "password": "Anushya@2004"},
    {"username": "SBOVDBN5573944", "password": "Vinoth@3"},
    {"username": "SBOVDBN5573975", "password": "Sakthi@123"},
    {"username": "SBOVDBN55285076", "password": "Poorna@123"},
    {"username": "SBOVDBN55150323", "password": "Nethaji@2003"},
    {"username": "SBOVDBN55161881", "password": "Ganesh@2003"},
    {"username": "SBOVDBN55194012", "password": "Ganesh@007"},
    {"username": "SBOVDBN55272764", "password": "Abi@2003"},
    {"username": "SBOVDBN55204739", "password": "Thirumalai4627@@"},
    {"username": "SBOVDBN55280040", "password": "Deepi@2003"},
    {"username": "SBOVDBN55214521", "password": "Nagaraju@2003"},
    {"username": "SBOVDBN55284900", "password": "Nag@1234"},
    {"username": "SBOVDBN55278180", "password": "Sarika@2003"},
    {"username": "SBOVDBN55278204", "password": "Raja@2003"},
    {"username": "SBOMA4119", "password": "Rakesh@2025"},
    {"username": "SBOVDBN5573975", "password": "Sakthi@123"},
    {"username": "SBOVDPN5570549", "password": "Jivanya@7200"},
    {"username": "SBOVDPN5578047", "password": "Selvi@123"},
    {"username": "SBOVDPN55243342", "password": "Ari@2003"},
    {"username": "SBOVDPN5557087", "password": "Adhi@0007"},
    {"username": "SBOVDPN5588462", "password": "Chanapapa@123"},
    {"username": "SBOVDPN5570413", "password": "Murugan@123"},
    {"username": "SBOVDPN5570503", "password": "Pachamuthu@123"},
    {"username": "SBOVDPN5574726", "password": "Eduman@123"},
    {"username": "SBOVDPN5586729", "password": "Lakshmi@123"},
    {"username": "SBOVDBN55101273", "password": "Kabir@2003"},
    {"username": "SBOVDBN55164533", "password": "Pavanrr@27"},
    {"username": "SBOVDBN55212428", "password": "Ramana@2002"},
    {"username": "SBOVDBN55279990", "password": "Prabhu@2002"},
    {"username": "SBOVDBN5592352", "password": "Vasa@917170"},
    {"username": "SBOVDPN55176844", "password": "Dinesh@208212"},
    {"username": "SBOVDPN55284877", "password": "Ari@2004"},
    {"username": "SBOVDBN55214743", "password": "Arthi@2003"},
    {"username": "SBOVDBN55286683", "password": "Sarathi@123"},
    {"username": "SBOVDPN55143840", "password": "@Naveen444"},
]

# Database connection details
DB_HOST = 'srv1837.hstgr.io'
DB_PORT = 3306
DB_USER = 'u329947844_ems'
DB_PASSWORD = 'Hifi11@ems'
DB_NAME = 'u329947844_ems'

# Email configuration
EMAIL_SENDER = "ariharasudhanonofficial@gmail.com"
EMAIL_PASSWORD = "tjhw ghst eyma xwlp"
EMAIL_RECEIVER = "ariharasudhanonofficial@gmail.com"

# Configure Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Enable headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# Additional options for better headless performance
options.add_argument('--disable-extensions')
options.add_argument('--disable-images')  # Optional: disable images for faster loading
options.add_argument('--blink-settings=imagesEnabled=false')  # Optional: disable images

# Path to ChromeDriver
service = Service(r"D:\Sbo New\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Store results for email report
processing_results = []

def create_database_connection():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        print("Database connection established.")
        return connection
    except OperationalError as e:
        print(f"Failed to connect to the database: {e}")
        driver.quit()
        exit(1)

def initialize_database_tables(connection):
    """Initialize wallet logs table if it doesn't exist"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wallet_records_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    profile_name VARCHAR(255),
                    task_wallet_amount DECIMAL(15,2),
                    intro_commission DECIMAL(15,2),
                    total_amount DECIMAL(15,2) GENERATED ALWAYS AS (COALESCE(task_wallet_amount, 0) + COALESCE(intro_commission, 0)) STORED,
                    record_date DATE NOT NULL,
                    fetched_at DATETIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_user_date (username, record_date)
                )
            """)
            print("Wallet records logs table initialized/verified.")
    except Exception as e:
        print(f"Error initializing database tables: {e}")

def login_and_redirect_to_dashboard(username, password):
    try:
        print(f"\nProcessing {username}")
        
        driver.get("https://www.sboportal.org.in/login")
        time.sleep(2)  # Slightly longer wait for headless
        
        # Clear and enter credentials
        username_field = driver.find_element(By.ID, "profileid")
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        
        driver.find_element(By.ID, "submitbtn").click()
        time.sleep(3)
        
        # Check if login was successful
        if "dashboard" not in driver.current_url.lower():
            print("Redirecting to dashboard...")
            driver.get("https://www.sboportal.org.in/dashboard")
            time.sleep(2)
            
        # Wait for wallet element to appear
        WebDriverWait(driver, 20).until(  # Increased timeout for headless
            EC.presence_of_element_located((By.CLASS_NAME, "wallet"))
        )
        print("Dashboard loaded successfully")
        return True
        
    except Exception as e:
        print(f"Login/redirect failed for {username}: {e}")
        return False

def get_profile_name():
    try:
        profile_element = WebDriverWait(driver, 15).until(  # Increased timeout
            EC.presence_of_element_located((By.CSS_SELECTOR, ".profile_avatar .content_profile h2"))
        )
        return profile_element.text.strip()
    except Exception as e:
        print(f"Error getting profile name: {e}")
        return None

def fetch_wallet_amounts():
    amounts = {'task_earned': None, 'intro_commission': None}
    
    try:
        task_element = WebDriverWait(driver, 15).until(  # Increased timeout
            EC.presence_of_element_located((By.XPATH, "//h4[contains(., 'Task Earned')]/following-sibling::h3"))
        )
        amounts['task_earned'] = float(task_element.text.strip().replace(',', '').replace('₹', ''))
        
        intro_element = WebDriverWait(driver, 15).until(  # Increased timeout
            EC.presence_of_element_located((By.XPATH, "//h4[contains(., 'Intro Commission')]/following-sibling::h3"))
        )
        amounts['intro_commission'] = float(intro_element.text.strip().replace(',', '').replace('₹', ''))
        
    except Exception as e:
        print(f"Error fetching wallet amounts: {e}")
    
    return amounts

def update_database(connection, username, profile_name, task_amount, intro_amount):
    """Update both main tables and wallet logs"""
    current_date = datetime.now().date()
    current_datetime = datetime.now()
    
    try:
        with connection.cursor() as cursor:
            # Update task_wallet_records table
            if task_amount is not None:
                cursor.execute("""
                    UPDATE task_wallet_records
                    SET task_wallet_amount = %s,
                        fetched_at = CURRENT_TIMESTAMP
                    WHERE username = %s
                """, (task_amount, username))
                print(f"Updated Task Wallet for {username}: ₹{task_amount}")
            
            # Update intro_commission_records table
            if intro_amount is not None:
                cursor.execute("""
                    UPDATE intro_commission_records
                    SET intro_commission = %s,
                        profile_name = %s,
                        fetched_at = CURRENT_TIMESTAMP
                    WHERE username = %s
                """, (intro_amount, profile_name, username))
                print(f"Updated Intro Commission for {username}: ₹{intro_amount}")
            
            # Update or insert into wallet_records_logs table
            cursor.execute("""
                INSERT INTO wallet_records_logs 
                (username, profile_name, task_wallet_amount, intro_commission, record_date, fetched_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                profile_name = VALUES(profile_name),
                task_wallet_amount = VALUES(task_wallet_amount),
                intro_commission = VALUES(intro_commission),
                fetched_at = VALUES(fetched_at)
            """, (username, profile_name, task_amount, intro_amount, current_date, current_datetime))
            
            print(f"Updated wallet logs for {username} on date {current_date}")
                
        return True
    except Exception as e:
        print(f"Database update error for {username}: {e}")
        return False

def get_wallet_logs_summary(connection, username=None):
    """Get summary of wallet logs for reporting"""
    try:
        with connection.cursor() as cursor:
            if username:
                cursor.execute("""
                    SELECT record_date, 
                           COUNT(*) as records_count,
                           SUM(task_wallet_amount) as total_task,
                           SUM(intro_commission) as total_intro,
                           SUM(COALESCE(task_wallet_amount, 0) + COALESCE(intro_commission, 0)) as total_combined
                    FROM wallet_records_logs
                    WHERE username = %s
                    GROUP BY record_date
                    ORDER BY record_date DESC
                    LIMIT 10
                """, (username,))
            else:
                cursor.execute("""
                    SELECT record_date, 
                           COUNT(*) as records_count,
                           SUM(task_wallet_amount) as total_task,
                           SUM(intro_commission) as total_intro,
                           SUM(COALESCE(task_wallet_amount, 0) + COALESCE(intro_commission, 0)) as total_combined
                    FROM wallet_records_logs
                    GROUP BY record_date
                    ORDER BY record_date DESC
                    LIMIT 10
                """)
            
            return cursor.fetchall()
    except Exception as e:
        print(f"Error getting wallet logs summary: {e}")
        return []

def logout():
    try:
        driver.get("https://www.sboportal.org.in/logout")
        time.sleep(2)
        print("Logged out successfully")
        return True
    except Exception as e:
        print(f"Logout failed: {e}")
        return False

def process_user(connection, username, password):
    result = {
        'username': username,
        'status': 'Failed',
        'profile_name': None,
        'task_earned': None,
        'intro_commission': None,
        'error': None
    }
    
    if not login_and_redirect_to_dashboard(username, password):
        result['error'] = 'Login failed'
        processing_results.append(result)
        return
        
    try:
        profile_name = get_profile_name()
        result['profile_name'] = profile_name
        print(f"Profile Name: {profile_name}")
        
        amounts = fetch_wallet_amounts()
        result['task_earned'] = amounts['task_earned']
        result['intro_commission'] = amounts['intro_commission']
        print(f"Fetched Amounts - Task: {amounts['task_earned']}, Intro: {amounts['intro_commission']}")
        
        db_success = update_database(connection, username, profile_name, 
                                   amounts['task_earned'], amounts['intro_commission'])
        
        if db_success:
            result['status'] = 'Success'
        else:
            result['status'] = 'Database Update Failed'
        
    except Exception as e:
        result['error'] = str(e)
        print(f"Error during processing for {username}: {e}")
    finally:
        logout_success = logout()
        if not logout_success:
            result['error'] = 'Logout failed' if not result['error'] else result['error'] + ', Logout failed'
    
    processing_results.append(result)

def calculate_totals():
    total_task = 0
    total_intro = 0
    successful_count = 0
    
    for result in processing_results:
        if result['status'] == 'Success':
            if result['task_earned'] is not None:
                total_task += result['task_earned']
            if result['intro_commission'] is not None:
                total_intro += result['intro_commission']
            successful_count += 1
    
    total_combined = total_task + total_intro
    deduction_35_percent = total_combined * 0.35
    amount_after_deduction = total_combined - deduction_35_percent
    
    return {
        'total_task': total_task,
        'total_intro': total_intro,
        'total_combined': total_combined,
        'deduction_35_percent': deduction_35_percent,
        'amount_after_deduction': amount_after_deduction,
        'successful_count': successful_count
    }

def send_email_report(connection):
    try:
        totals = calculate_totals()
        logs_summary = get_wallet_logs_summary(connection)
        
        subject = f"SBO Portal Report - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                th {{ background-color: #f5f5f5; }}
                .total-row {{ font-weight: bold; background-color: #f0f0f0; }}
                .amount {{ text-align: right; }}
                .success {{ color: green; }}
                .failed {{ color: red; }}
                h2 {{ color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                h3 {{ color: #555; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h2>SBO Portal Automation Report</h2>
            
            <p><strong>Report Date:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p><strong>Total Profiles:</strong> {len(processing_results)}</p>
            <p><strong class="success">Successful:</strong> {totals['successful_count']}</p>
            <p><strong class="failed">Failed:</strong> {len(processing_results) - totals['successful_count']}</p>

            <h3>Financial Summary</h3>
            <table>
                <tr>
                    <th>Description</th>
                    <th>Amount (₹)</th>
                </tr>
                <tr>
                    <td>Total Task Earned</td>
                    <td class="amount">₹{totals['total_task']:,.2f}</td>
                </tr>
                <tr>
                    <td>Total Intro Commission</td>
                    <td class="amount">₹{totals['total_intro']:,.2f}</td>
                </tr>
                <tr class="total-row">
                    <td><strong>Combined Total</strong></td>
                    <td class="amount"><strong>₹{totals['total_combined']:,.2f}</strong></td>
                </tr>
            </table>

            <h3>Deduction Calculation (35%)</h3>
            <table>
                <tr>
                    <th>Description</th>
                    <th>Amount (₹)</th>
                </tr>
                <tr>
                    <td>Total Combined Amount</td>
                    <td class="amount">₹{totals['total_combined']:,.2f}</td>
                </tr>
                <tr>
                    <td>35% Deduction</td>
                    <td class="amount">-₹{totals['deduction_35_percent']:,.2f}</td>
                </tr>
                <tr class="total-row">
                    <td><strong>Final Amount After Deduction</strong></td>
                    <td class="amount"><strong>₹{totals['amount_after_deduction']:,.2f}</strong></td>
                </tr>
            </table>

            <h3>Historical Records Summary (Last 10 Days)</h3>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Records</th>
                    <th>Total Task (₹)</th>
                    <th>Total Intro (₹)</th>
                    <th>Total Combined (₹)</th>
                </tr>
        """
        
        for log in logs_summary:
            html_content += f"""
                <tr>
                    <td>{log['record_date'].strftime('%d/%m/%Y')}</td>
                    <td>{log['records_count']}</td>
                    <td class="amount">₹{log['total_task'] or 0:,.2f}</td>
                    <td class="amount">₹{log['total_intro'] or 0:,.2f}</td>
                    <td class="amount">₹{log['total_combined'] or 0:,.2f}</td>
                </tr>
            """
        
        html_content += """
            </table>

            <h3>Individual Profile Results</h3>
            <table>
                <tr>
                    <th>Username</th>
                    <th>Status</th>
                    <th>Profile Name</th>
                    <th>Task Earned (₹)</th>
                    <th>Intro Commission (₹)</th>
                </tr>
        """
        
        for result in processing_results:
            task_display = f"₹{result['task_earned']:,.2f}" if result['task_earned'] is not None else 'N/A'
            intro_display = f"₹{result['intro_commission']:,.2f}" if result['intro_commission'] is not None else 'N/A'
            status_class = 'success' if result['status'] == 'Success' else 'failed'
            
            html_content += f"""
                <tr>
                    <td>{result['username']}</td>
                    <td class="{status_class}">{result['status']}</td>
                    <td>{result['profile_name'] or 'N/A'}</td>
                    <td class="amount">{task_display}</td>
                    <td class="amount">{intro_display}</td>
                </tr>
            """
        
        html_content += """
            </table>
            
            <br>
            <p><em>Automated report generated by SBO Portal system</em></p>
            <p><em>Complete wallet records are logged in the database with daily tracking</em></p>
            <p><strong>Mode:</strong> Headless Chrome Automation</p>
        </body>
        </html>
        """
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"\nEmail report sent successfully to {EMAIL_RECEIVER}")
        print(f"Total Task Amount: ₹{totals['total_task']:,.2f}")
        print(f"Total Intro Commission: ₹{totals['total_intro']:,.2f}")
        print(f"Combined Total: ₹{totals['total_combined']:,.2f}")
        print(f"35% Deduction: ₹{totals['deduction_35_percent']:,.2f}")
        print(f"Final Amount After Deduction: ₹{totals['amount_after_deduction']:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"Failed to send email report: {e}")
        return False

def main():
    print("Starting SBO Portal Automation in HEADLESS mode...")
    connection = create_database_connection()
    
    try:
        # Initialize database tables
        initialize_database_tables(connection)
        
        for credential in credentials:
            process_user(connection, credential['username'], credential['password'])
        
        print("\nSending email report...")
        send_email_report(connection)
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
        try:
            error_result = {
                'username': 'SYSTEM',
                'status': 'Error',
                'profile_name': None,
                'task_earned': None,
                'intro_commission': None,
                'error': f"Script error: {str(e)}"
            }
            processing_results.append(error_result)
            send_email_report(connection)
        except:
            print("Failed to send error report")
            
    finally:
        try:
            connection.close()
            print("\nDatabase connection closed.")
        except Exception as e:
            print(f"Error closing database connection: {e}")
        
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
