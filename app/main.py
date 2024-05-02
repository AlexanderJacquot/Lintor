import subprocess
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QPushButton
from loguru import logger
import sys


logger.remove()
logger.add(sys.stdout)


def lint_path(path, dialect):
    # Check if the path is a directory or a file
    if path.is_dir():
        # Lint all SQL files in the directory
        for sql_file in path.glob('**/*.sql'):
            print(f"Linting {sql_file}")
            result = subprocess.run(['python3 -m sqlfluff', 'lint', str(sql_file)], capture_output=True, text=True)
            print(result.stdout)
    elif path.is_file():
        # Lint the single file
        print(f"Linting {path}")
        result = subprocess.run(['sqlfluff', 'lint', str(path), '--dialect', dialect], capture_output=True, text=True)
        print(result.stderr)
        print(result.stdout)
    else:
        print("The path is neither a file nor a directory")


# def open_file_dialog(self) -> str:
#     excel_file_path = QFileDialog.getOpenFileName(None, "Selectionez le fichier de vente")
#     if excel_file_path:
#         logger.info(f"Fichier selectioné: {excel_file_path}")
#         self.excel_path = excel_file_path[0]
#         return excel_file_path[0]
#             photo_folder_path = QFileDialog.getExistingDirectory(None, "Selectionnez le dossier de Photos")
#         if photo_folder_path:
#             logger.info(f"Dossier Choisis: {photo_folder_path}")
#             self.photo_folder_path = photo_folder_path
#             return photo_folder_path
#             # QApplication.exit()
#     else:
#         logger.error("Pas de fichier de vente sélectioné. Recommence pauvre con")
#         exit(1)

class FileOrFolderDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File or Folder Dialog')

        layout = QVBoxLayout(self)

        # Button for selecting files
        btn_select_file = QPushButton('Select File', self)
        btn_select_file.clicked.connect(self.openFile)
        layout.addWidget(btn_select_file)

        # Button for selecting folders
        btn_select_folder = QPushButton('Select Folder', self)
        btn_select_folder.clicked.connect(self.openFolder)
        layout.addWidget(btn_select_folder)

        self.setLayout(layout)
        self.show()

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a file", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print("Selected file:", fileName)

    def openFolder(self):
        options = QFileDialog.Options()
        folderName = QFileDialog.getExistingDirectory(self, "Select a folder", "", options=options)
        if folderName:
            print("Selected folder:", folderName)

def main():
    app = QApplication(sys.argv)
    ex = FileOrFolderDialog()

    user_input = input("Enter the path of a directory or a file to lint: ")
    path = Path(user_input)

    dialect = 'bigquery'

    if not path.exists():
        print("The path does not exist. Please check the path and try again.")
        return

    lint_path(path, dialect)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
