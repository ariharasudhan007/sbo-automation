import os

def main():
    print("SBO Automation Running")

    # Example of using environment variables for DB & Email
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    gmail_user = os.getenv('GMAIL_USER')
    gmail_pass = os.getenv('GMAIL_PASS')
    to_email = os.getenv('TO_EMAIL')

    print(f"DB Host: {db_host}")
    print(f"Email To: {to_email}")

if __name__ == '__main__':
    main()
