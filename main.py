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
import os

# =========================
# CONFIGURATION
# =========================

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
]

# Database configuration
DB_HOST = 'srv1837.hstgr.io'
DB_PORT = 3306
DB_USER = 'u329947844_ems'
DB_PASSWORD = 'Hifi11@ems'
DB_NAME = 'u329947844_ems'

# Email configuration
EMAIL_SENDER = "ariharasudhanonofficial@gmail.com"
EMAIL_PASSWORD = "tjhw ghst eyma xwlp"
EMAIL_RECEIVER = "ariharasudhanonofficial@gmail.com"

# =========================
# SELENIUM HEADLESS SETUP
# =========================

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# ✅ ChromeDriver path for Linux (GitHub Actions)
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# =========================
# FUNCTIONS
# =========================

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
        print("✅ Database connection established.")
        return connection
    except OperationalError as e:
        print(f"❌ Failed to connect to database: {e}")
        driver.quit()
        exit(1)

def initialize_database_tables(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wallet_records_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    profile_name VARCHAR(255),
                    task_wallet_amount DECIMAL(15,2),
                    intro_commission DECIMAL(15,2),
                    total_amount DECIMAL(15,2)
                        GENERATED ALWAYS AS (COALESCE(task_wallet_amount, 0) + COALESCE(intro_commission, 0)) STORED,
                    record_date DATE NOT NULL,
                    fetched_at DATETIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_user_date (username, record_date)
                )
            """)
        print("✅ Table wallet_records_logs verified.")
    except Exception as e:
        print(f"⚠️ Error initializing tables: {e}")

def login_and_redirect_to_dashboard(username, password):
    try:
        print(f"\n🔐 Logging in as {username}")
        driver.get("https://www.sboportal.org.in/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profileid")))

        driver.find_element(By.ID, "profileid").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "submitbtn").click()
        time.sleep(3)

        if "dashboard" not in driver.current_url.lower():
            driver.get("https://www.sboportal.org.in/dashboard")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "wallet")))
        print("✅ Dashboard loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Login failed for {username}: {e}")
        return False

def get_profile_name():
    try:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".profile_avatar .content_profile h2"))
        )
        return el.text.strip()
    except:
        return "Unknown"

def fetch_wallet_amounts():
    amounts = {"task_earned": 0, "intro_commission": 0}
    try:
        task_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h4[contains(., 'Task Earned')]/following-sibling::h3"))
        )
        intro_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h4[contains(., 'Intro Commission')]/following-sibling::h3"))
        )
        amounts["task_earned"] = float(task_el.text.replace("₹", "").replace(",", ""))
        amounts["intro_commission"] = float(intro_el.text.replace("₹", "").replace(",", ""))
    except Exception as e:
        print(f"⚠️ Error fetching wallet: {e}")
    return amounts

def update_database(connection, username, profile_name, task, intro):
    try:
        date = datetime.now().date()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO wallet_records_logs 
                (username, profile_name, task_wallet_amount, intro_commission, record_date, fetched_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                    profile_name = VALUES(profile_name),
                    task_wallet_amount = VALUES(task_wallet_amount),
                    intro_commission = VALUES(intro_commission),
                    fetched_at = VALUES(fetched_at)
            """, (username, profile_name, task, intro, date))
        print(f"✅ DB updated for {username}")
        return True
    except Exception as e:
        print(f"❌ DB update failed for {username}: {e}")
        return False

def logout():
    try:
        driver.get("https://www.sboportal.org.in/logout")
        time.sleep(2)
    except:
        pass

def send_email_report(summary_html):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"SBO Report {datetime.now().strftime('%d-%m-%Y %H:%M')}"

        msg.attach(MIMEText(summary_html, "html"))
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL_SENDER, EMAIL_PASSWORD)
        s.send_message(msg)
        s.quit()
        print("📧 Email sent successfully")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def main():
    print("🚀 Starting SBO Automation on GitHub Actions (Headless Chrome)...")
    connection = create_database_connection()
    initialize_database_tables(connection)

    html_report = "<h2>SBO Wallet Summary</h2><table border='1' cellpadding='8'><tr><th>Username</th><th>Name</th><th>Task</th><th>Intro</th><th>Status</th></tr>"

    for cred in credentials:
        username, password = cred["username"], cred["password"]
        if login_and_redirect_to_dashboard(username, password):
            name = get_profile_name()
            amounts = fetch_wallet_amounts()
            success = update_database(connection, username, name, amounts["task_earned"], amounts["intro_commission"])
            html_report += f"<tr><td>{username}</td><td>{name}</td><td>{amounts['task_earned']}</td><td>{amounts['intro_commission']}</td><td>{'✅' if success else '❌'}</td></tr>"
            logout()
        else:
            html_report += f"<tr><td>{username}</td><td>-</td><td>-</td><td>-</td><td>❌ Login failed</td></tr>"

    html_report += "</table><p>Automation completed at {}</p>".format(datetime.now().strftime("%d-%m-%Y %H:%M"))
    send_email_report(html_report)

    connection.close()
    driver.quit()
    print("✅ Completed successfully!")

if __name__ == "__main__":
    main()
