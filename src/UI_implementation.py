from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox, QMainWindow
)
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
import importlib.util
import os
import sys


# Load the Huffman and Lempel modules dynamically
def load_module_from_file(file_name, module_name):
    file_path = os.path.abspath(file_name)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


huffman_module = load_module_from_file("src/Huffman3_with_compress_serialized_tree.py", "huffman")
lempel_module = load_module_from_file("src/Lempel_with_compress.py", "lempel")


class CompressorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.label_input = QLabel("Drag and drop multiple .txt files or use the 'Select Files' button below:")
        layout.addWidget(self.label_input)

        self.text_results = QTextEdit()
        self.text_results.setReadOnly(True)
        layout.addWidget(self.text_results)

        self.select_files_button = QPushButton("Select Files")
        self.select_files_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_files_button)

        self.compress_button = QPushButton("Compress, Decompress, Compare, and Visualize")
        self.compress_button.clicked.connect(self.process_files)
        layout.addWidget(self.compress_button)

        self.setWindowTitle("Text Compression Comparison")
        self.resize(800, 600)

        self.central_widget.setLayout(layout)

    def select_files(self):
        """Open a file dialog to select multiple text files."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Text Files", "", "Text Files (*.txt)", options=options)
        if files:
            self.selected_files = files
            self.text_results.setText(f"Selected Files:\n" + "\n".join(files))
        else:
            self.selected_files = []
            self.text_results.setText("No files selected.")

    def process_files(self):
        """Compress, decompress, compare, and visualize for multiple files."""
        if not hasattr(self, "selected_files") or not self.selected_files:
            QMessageBox.critical(self, "Error", "Please select at least one .txt file.")
            return

        try:
            results = []
            overall_data = {"Algorithm": [], "Size (bytes)": [], "File": []}

            for file_path in self.selected_files:
                # File-specific paths
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                huffman_compressed_file = f"{base_name}_huffman_compressed.bin"
                huffman_tree_file = f"{base_name}_huffman_tree.bin"
                huffman_decompressed_file = f"{base_name}_huffman_decompressed.txt"

                lempel_compressed_file = f"{base_name}_lempel_compressed.lzw"
                lempel_decompressed_file = f"{base_name}_lempel_decompressed.txt"

                # Read the original file size
                original_size = os.path.getsize(file_path)

                # Huffman compression and decompression
                huffman_module.compress(file_path, huffman_compressed_file, huffman_tree_file)
                huffman_module.decompress(huffman_compressed_file, huffman_tree_file, huffman_decompressed_file)

                huffman_compressed_size = os.path.getsize(huffman_compressed_file)
                huffman_decompressed_size = os.path.getsize(huffman_decompressed_file)

                # Lempel-Ziv compression and decompression
                lempel_module.lzw_compress(file_path, lempel_compressed_file)
                lempel_module.lzw_decompress(lempel_compressed_file, lempel_decompressed_file)

                lempel_compressed_size = os.path.getsize(lempel_compressed_file)
                lempel_decompressed_size = os.path.getsize(lempel_decompressed_file)

                # Collect results for display
                results.append(
                    f"File: {file_path}\n"
                    f"Original Size: {original_size} bytes\n"
                    f"Huffman Compressed Size: {huffman_compressed_size} bytes\n"
                    f"Huffman Decompressed Size: {huffman_decompressed_size} bytes\n"
                    f"Lempel-Ziv Compressed Size: {lempel_compressed_size} bytes\n"
                    f"Lempel-Ziv Decompressed Size: {lempel_decompressed_size} bytes\n"
                )

                # Collect data for visualization
                overall_data["Algorithm"].extend(["Original", "Huffman", "Lempel"])
                overall_data["Size (bytes)"].extend([original_size, huffman_compressed_size, lempel_compressed_size])
                overall_data["File"].extend([base_name] * 3)

            # Display results in the UI
            self.text_results.setText("\n\n".join(results))

            # Visualize results
            self.visualize_results(overall_data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Processing failed: {e}")

    def visualize_results(self, data):
        """Create bar charts for each file and an aggregate chart."""
        df = pd.DataFrame(data)

        # Individual file visualizations
        for file_name in df["File"].unique():
            file_data = df[df["File"] == file_name]
            file_data.plot(
                kind="bar", x="Algorithm", y="Size (bytes)", legend=False,
                title=f"Compression Comparison for {file_name}"
            )
            plt.ylabel("Size (bytes)")
            plt.show()

        # Aggregate visualization
        aggregate_data = df.groupby("Algorithm")["Size (bytes)"].mean().reset_index()
        aggregate_data.plot(
            kind="bar", x="Algorithm", y="Size (bytes)", legend=False,
            title="Average Compression Comparison"
        )
        plt.ylabel("Size (bytes)")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CompressorUI()
    main_window.show()
    sys.exit(app.exec_())
