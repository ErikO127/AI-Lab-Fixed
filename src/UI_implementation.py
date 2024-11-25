from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
)
import importlib.util
import os


def load_module_from_file(file_name, module_name):
    base_path = os.path.dirname(os.path.abspath(__file__))  # Path to this script
    file_path = os.path.join(base_path, file_name)          # Full path to the module
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load the Huffman and Lempel modules
huffman_module = load_module_from_file('Huffman3_with_compress_serialized_tree.py', 'huffman')
lempel_module = load_module_from_file('Lempel_with_compress.py', 'lempel')


class CompressorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Input label and text box
        self.label_input = QLabel("Paste text below:")
        layout.addWidget(self.label_input)

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        # Compress button
        self.compress_button = QPushButton("Compress and Compare")
        self.compress_button.clicked.connect(self.compress_text)
        layout.addWidget(self.compress_button)

        # Results label and text box
        self.label_results = QLabel("Results:")
        layout.addWidget(self.label_results)

        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        layout.addWidget(self.text_results)

        # Set layout
        self.setLayout(layout)
        self.setWindowTitle("Text Compression Comparison")
        self.resize(600, 400)

    def compress_text(self):
        input_text = self.text_input.toPlainText().strip()
        if not input_text:
            QMessageBox.critical(self, "Error", "Please paste some text to compress.")
            return

        try:
            # Compress using Huffman
            huffman_compressed_data, huffman_compressed_size = huffman_module.compress(input_text)

            # Compress using Lempel-Ziv
            lempel_compressed_data = lempel_module.compress(input_text)
            lempel_compressed_size = len(lempel_compressed_data)

            # Display results
            results = (
                f"Original Text Size: {len(input_text)} bytes\n"
                f"Huffman Compressed Size: {huffman_compressed_size} bytes\n"
                f"Lempel-Ziv Compressed Size: {lempel_compressed_size} bytes\n"
            )
            self.text_results.setPlainText(results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")


# Run the PyQt5 application
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = CompressorUI()
    window.show()
    sys.exit(app.exec_())
