import sys
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel, QHBoxLayout
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", filter="my_module", level="INFO")

def lint_path(path, dialect, language):
    output = []
    config_file = './app/.sqlfluff'  # Define the path to your config file
    if language.lower() == "sql":
        command = ['python3', '-m', 'sqlfluff', 'lint', str(path), '--dialect', dialect, '--config', config_file]
    elif language.lower() == "python":
        command = ['python3', '-m', 'flake8', str(path)]
    else:
        return "Unsupported language"

    if path.is_dir():
        for file in path.glob('**/*.sql' if language.lower() == "sql" else '**/*.py'):
            result = subprocess.run(command[:-1] + [str(file)], capture_output=True, text=True) # This needs to be corrected for the -1
            output.append(f"Linting {file}\n{result.stderr}{result.stdout}\n")
    elif path.is_file():
        result = subprocess.run(command, capture_output=True, text=True)
        output.append(f"Linting {path}\n{result.stderr}{result.stdout}\n")
    else:
        output.append("The path is neither a file nor a directory")

    return "\n".join(output)

class FileOrFolderDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('File or Folder Dialog')
        layout = QVBoxLayout(self)

        # Button for selecting files
        btn_run = QPushButton('Lint', self)
        btn_run.clicked.connect(self.run)
        layout.addWidget(btn_run)

        # Button for selecting files
        btn_select_file = QPushButton('Select File', self)
        btn_select_file.clicked.connect(self.openFile)
        layout.addWidget(btn_select_file)

        # Button for selecting folders
        btn_select_folder = QPushButton('Select Folder', self)
        btn_select_folder.clicked.connect(self.openFolder)
        layout.addWidget(btn_select_folder)

        # Dropdown for choosing language
        hbox = QHBoxLayout()
        lbl_language = QLabel("Choose Language:", self)
        hbox.addWidget(lbl_language)
        self.language_dropdown = QComboBox(self)
        self.language_dropdown.addItems(["SQL", "Python"])
        self.language_dropdown.currentIndexChanged.connect(self.updateDialectVisibility)  # Connect to update function
        hbox.addWidget(self.language_dropdown)
        layout.addLayout(hbox)

        # Dropdown for choosing SQL dialect
        self.dialect_hbox = QHBoxLayout()
        self.lbl_dialect = QLabel("Choose SQL Dialect:", self)
        self.dialect_hbox.addWidget(self.lbl_dialect)
        self.dialect_dropdown = QComboBox(self)
        self.dialect_dropdown.addItems(["bigquery", "mysql", "postgres"])
        self.dialect_hbox.addWidget(self.dialect_dropdown)
        layout.addLayout(self.dialect_hbox)

        # Initially hide the SQL dialect widgets
        self.lbl_dialect.setVisible(True)
        self.dialect_dropdown.setVisible(True)

        # Text Edit for displaying results
        self.results_text = QTextEdit(self)
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        self.setLayout(layout)
        self.show()

    def run(self):
        self.displayResults()

    def openFile(self):
        self.results_text.clear()
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*);;SQL Files (*.sql);;Python Files (*.py)", options=options)
        if fileName:
            self.selected_path = fileName
            self.displayResults()

    def openFolder(self):
        self.results_text.clear()
        options = QFileDialog.Options()
        folderName = QFileDialog.getExistingDirectory(self, "Select a folder", "", options=options)
        if folderName:
            self.selected_path = folderName
            self.displayResults()

    def updateDialectVisibility(self):
        # Show or hide the SQL dialect widgets based on the language selection
        if self.language_dropdown.currentText() == "SQL":
            self.lbl_dialect.setVisible(True)
            self.dialect_dropdown.setVisible(True)
        else:
            self.lbl_dialect.setVisible(False)
            self.dialect_dropdown.setVisible(False)

    def displayResults(self):
        try:
            path = Path(self.selected_path)
            if path.exists():
                selected_language = self.language_dropdown.currentText()
                selected_dialect = self.dialect_dropdown.currentText() if selected_language == "SQL" else ''
                results = lint_path(path, selected_dialect, selected_language)

                formatted_text = f"<p><b>Linting {path}</b></p>"

                for line in results.split('\n'):
                    if "FAIL" in line:
                        formatted_text += f"<p style='color: red;'>{line}</p>"
                    elif line.startswith("L:") and ("ERROR" in line or "WARN" in line):
                        color = 'orange' if "WARN" in line else 'red'
                        formatted_text += f"<p style='color: {color};'>{line}</p>"
                    elif line.strip():
                        formatted_text += f"<p>{line}</p>"

                self.results_text.setHtml(formatted_text)
            else:
                self.results_text.setPlainText("The path does not exist. Please check the path and try again.")
        except Exception as e:
            self.results_text.setPlainText("No file or path selected, please select either one and try again.")

def main():
    app = QApplication(sys.argv)
    ex = FileOrFolderDialog()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
