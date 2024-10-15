import sys
from PyQt5.QtWidgets import QApplication
from InTheBag.gui import DiscLookupApp  # Import the DiscLookupApp from gui.py

def main():
    app = QApplication(sys.argv)
    window = DiscLookupApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
