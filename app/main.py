import sys
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QPushButton, QTextEdit
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", filter="my_module", level="INFO")


def lint_path(path, dialect):
    output = []
    # Check if the path is a directory or a file
    if path.is_dir():
        # Lint all SQL files in the directory
        for sql_file in path.glob('**/*.sql'):
            result = subprocess.run(['python3', '-m', 'sqlfluff', 'lint', str(sql_file), '--dialect', dialect],
                                    capture_output=True, text=True)
            output.append(f"Linting {sql_file}\n{result.stderr}{result.stdout}\n")
    elif path.is_file():
        # Lint the single file
        result = subprocess.run(['python3', '-m', 'sqlfluff', 'lint', str(path), '--dialect', dialect],
                                capture_output=True, text=True)
        output.append(f"Linting {path}\n{result.stderr}{result.stdout}\n")
    else:
        output.append("The path is neither a file nor a directory")

    return "\n".join(output)


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

        # Text Edit for displaying results
        self.results_text = QTextEdit(self)
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        self.setLayout(layout)
        self.show()

    def openFile(self):
        self.results_text.clear()  # Clear previous results
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a file", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.selected_path = fileName
            self.displayResults()

    def openFolder(self):
        self.results_text.clear()  # Clear previous results
        options = QFileDialog.Options()
        folderName = QFileDialog.getExistingDirectory(self, "Select a folder", "", options=options)
        if folderName:
            self.selected_path = folderName
            self.displayResults()

    def displayResults(self):
        path = Path(self.selected_path)
        if path.exists():
            dialect = 'bigquery'
            results = lint_path(path, dialect)
            
            # Begin HTML formatting
            formatted_text = "<p><b>Linting " + str(path) + "</b></p>"
            
            # Parse each line and apply HTML formatting based on content
            for line in results.split('\n'):
                if "FAIL" in line:
                    # Red color for FAIL messages
                    formatted_text += f"<p style='color: red;'>{line}</p>"
                elif line.startswith("L:") and "ERROR" in line or "WARN" in line:
                    # Orange color for warnings, red for errors
                    color = 'orange' if "WARN" in line else 'red'
                    formatted_text += f"<p style='color: {color};'>{line}</p>"
                elif line.strip():
                    # Default styling for other lines
                    formatted_text += f"<p>{line}</p>"
            
            self.results_text.setHtml(formatted_text)
        else:
            self.results_text.setPlainText("The path does not exist. Please check the path and try again.")



def main():
    app = QApplication(sys.argv)
    ex = FileOrFolderDialog()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
