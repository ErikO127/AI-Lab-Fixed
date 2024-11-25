from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
)
import importlib.util
import os


def load_module_from_file(file_name, module_name):
    base_path = os.path.dirname(os.path.abspath(__file__))  
    file_path = os.path.join(base_path, file_name)         
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


huffman_module = load_module_from_file('Huffman3_with_compress_serialized_tree.py', 'huffman')
lempel_module = load_module_from_file('Lempel_with_compress.py', 'lempel')


class CompressorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_input = QLabel("Paste text below:")
        layout.addWidget(self.label_input)

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        self.compress_button = QPushButton("Compress and Compare")
        self.compress_button.clicked.connect(self.compress_text)
        layout.addWidget(self.compress_button)

        self.label_results = QLabel("Results:")
        layout.addWidget(self.label_results)

        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        layout.addWidget(self.text_results)

        self.setLayout(layout)
        self.setWindowTitle("Text Compression Comparison")
        self.resize(600, 400)

    def compress_text(self):
        input_text = self.text_input.toPlainText().strip()
        if not input_text:
            QMessageBox.critical(self, "Error", "Please paste some text to compress.")
            return

        try:
            huffman_compressed_data, huffman_compressed_size = huffman_module.compress(input_text)

            lempel_compressed_data = lempel_module.compress(input_text)
            lempel_compressed_size = len(lempel_compressed_data)

            results = (
                f"Original Text Size: {len(input_text)} bytes\n"
                f"Huffman Compressed Size: {huffman_compressed_size} bytes\n"
                f"Lempel-Ziv Compressed Size: {lempel_compressed_size} bytes\n"
            )
            self.text_results.setPlainText(results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = CompressorUI()
    window.show()
    sys.exit(app.exec_())
