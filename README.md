# SBO Automation GitHub Project

This project runs a headless Selenium automation with MySQL connection and Gmail reporting using GitHub Actions.

## Setup

1. Upload your actual `main.py` code replacing the placeholder.
2. Add the following GitHub Secrets:
   - DB_HOST
   - DB_USER
   - DB_PASS
   - DB_NAME
   - GMAIL_USER
   - GMAIL_PASS
   - TO_EMAIL
3. Push to GitHub and the action will run daily at 6 PM IST.
