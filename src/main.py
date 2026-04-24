import sys
import os

# Add src to Python path if running directly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ui.main_window import run_ui

def main():
    """
    Entry point cho ứng dụng RoomQS.
    Khởi chạy UI chính.
    """
    run_ui()

if __name__ == "__main__":
    main()
