import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # Replace with your MySQL username
    'password': '',    # Replace with your MySQL password
    'database': 'inventory_db_python'
}

# Secret key for session management and security
# For production, use an environment variable to set this
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')  # Replace 'default_secret_key' with a secure value or use environment variables
