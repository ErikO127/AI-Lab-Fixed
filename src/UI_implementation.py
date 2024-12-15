from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QMainWindow
)
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
import importlib.util
import os
import sys

# Load the Huffman and Lempel modules dynamically
def load_module_from_file(file_name, module_name):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, file_name)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


huffman_module = load_module_from_file('Huffman3_with_compress_serialized_tree.py', 'huffman')
lempel_module = load_module_from_file('Lempel_with_compress.py', 'lempel')


class CompressorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lempel_module = lempel_module
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.label_input = QLabel("Paste text below or drag a .txt file:")
        layout.addWidget(self.label_input)

        self.text_input = QTextEdit()
        self.text_input.setAcceptDrops(True)
        self.text_input.dragEnterEvent = self.drag_enter_event
        self.text_input.dropEvent = self.drop_event
        layout.addWidget(self.text_input)

        self.compress_button = QPushButton("Compress and Compare")
        self.compress_button.clicked.connect(self.compress_text)
        layout.addWidget(self.compress_button)

        self.label_results = QLabel("Results:")
        layout.addWidget(self.label_results)

        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        layout.addWidget(self.text_results)

        self.setWindowTitle("Text Compression Comparison")
        self.resize(600, 400)

        self.central_widget.setLayout(layout)

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.txt'):
                with open(file_path, 'r') as file:
                    self.text_input.setPlainText(file.read())
            else:
                QMessageBox.warning(self, "Invalid File", "Please drop a valid .txt file.")

    def compress_text(self):
        input_text = self.text_input.toPlainText().strip()
        if not input_text:
            QMessageBox.critical(self, "Error", "Please provide some text to compress.")
            return

        try:
            # Perform Huffman compression
            huffman_compressed_data, huffman_compressed_size = huffman_module.compress(input_text)

            # Save input text to a temporary file for Lempel compression
            input_file = "temp_input.txt"
            lempel_output_file = "compressed.lzw"
            with open(input_file, 'w') as file:
                file.write(input_text)

            # Perform Lempel compression and get file size
            lempel_module.lzw_compress(input_file, lempel_output_file)
            lempel_compressed_size = os.path.getsize(lempel_output_file)

            # Display results
            original_size = len(input_text.encode('utf-8'))  # Get size of original text in bytes
            self.text_results.setText(
                f"Original Text Size: {original_size} bytes\n"
                f"Huffman Compressed Size: {huffman_compressed_size} bytes\n"
                f"Lempel-Ziv Compressed Size: {lempel_compressed_size} bytes\n"
            )

            # Visualize results
            self.show_compression_graph(original_size, huffman_compressed_size, lempel_compressed_size)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Compression failed: {e}")


    def show_compression_graph(self, original_size, huffman_size, lempel_size):
        data = {
            "Algorithm": ["Original", "Huffman", "Lempel"],
            "Size (bytes)": [original_size, huffman_size, lempel_size],
        }
        df = pd.DataFrame(data)

        # Bar Graph
        df.plot(kind="bar", x="Algorithm", y="Size (bytes)", legend=False, title="Compression Comparison")
        plt.ylabel("Size (bytes)")
        plt.show()

        # Pie Chart
        df.set_index("Algorithm").plot.pie(y="Size (bytes)", autopct='%1.1f%%', legend=False, title="Compression Distribution")
        plt.ylabel("")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CompressorUI()
    main_window.show()
    sys.exit(app.exec_())
