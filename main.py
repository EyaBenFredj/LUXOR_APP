import sys
import logging
from PyQt5.QtWidgets import QApplication
from login import Login
from database import create_tables, populate_listefour
import os

# Configure logging to write to a directory that doesn't require elevated permissions
log_file_path = os.path.join(os.path.expanduser("~"), 'app.log')  # Writes log file to the user's home directory
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    logging.info('Application started')
    try:
        db_path = resource_path("cost_calculation.db")
        create_tables(db_path)  # Pass the correct database path
        populate_listefour(db_path)  # Populate initial data
        logging.info('Database tables created successfully')

        app = QApplication(sys.argv)
        logging.info('QApplication created')

        login_window = Login()
        logging.info('Login window created')

        login_window.show()
        logging.info('Login window shown')

        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        sys.exit(1)  # Ensure the application exits with a non-zero status on error

if __name__ == '__main__':
    main()
