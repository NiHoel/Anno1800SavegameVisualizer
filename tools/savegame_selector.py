import sys
from PyQt5.QtWidgets import QFileDialog, QApplication

if __name__ == "__main__":
     directory = sys.argv[1]
     description = sys.argv[2]
     filter = sys.argv[3]
     app = QApplication([directory])
     fname = QFileDialog.getOpenFileName(None, description,
             directory, filter=filter)
     print(fname[0])