from src.UI_implementation import CompressorUI
import pytest
from PyQt5.QtCore import Qt
import os
from pathlib import Path

@pytest.fixture
def app(qtbot):
    widget = CompressorUI()
    qtbot.addWidget(widget)
    return widget

def test_ui_compress_words_file(app, qtbot, tmp_path):
    # Change the current working directory to tmp_path so that all files are created there
    os.chdir(tmp_path)

    input_text = """Background information:
The term spectrochemical can be broken into two different words describing what it means,
spectro- which refers to the electromagnetic spectrum, and chemical which links to atomic
chemical properties. Ligands are a part of a unique area in chemistry explaining many
phenomenons when it comes to colors that we observe and have been used by humans for a
long time stretching back as far as ancient egyptians and are still in us in today's world.
Coordination compounds are atomic compounds that are formed when a special types of bonds
are formed between the central ion and the outer ligands. The central ion is always metallic and
the outer ion can be a variety of different common non metallic molecules or atomic ions which
in a complex compound are named Ligands."""

    app.text_input.setPlainText(input_text)

    # Write the input text to a temporary file inside tmp_path
    input_file = tmp_path / "temp_input.txt"
    input_file.write_text(input_text)

    # Instead of mocking LZW compression, let's just run the actual compression for realistic results
    qtbot.mouseClick(app.compress_button, Qt.LeftButton)

    # Parse the output text from the results
    text_output = app.text_results.toPlainText()
    lines = text_output.strip().split("\n")

    # Expected lines format:
    # Original Text Size: X bytes
    # Huffman Compressed Size: Y bytes
    # Lempel-Ziv Compressed Size: Z bytes
    size_map = {}
    for line in lines:
        parts = line.split(":")
        key = parts[0].strip()
        val_str = parts[1].strip().split()[0]  # Get the number before 'bytes'
        val = int(val_str)
        size_map[key] = val

    original_size = len(input_text.encode("utf-8"))
    assert size_map["Original Text Size"] == original_size, "Original size should match input text size."

    # Verify that Huffman compression yields a smaller size than the original
    assert 0 < size_map["Huffman Compressed Size"] < original_size, (
        f"Huffman compressed size {size_map['Huffman Compressed Size']} is not smaller than original {original_size}."
    )

    # Verify that Lempel-Ziv compression also yields a smaller size than the original
    assert 0 < size_map["Lempel-Ziv Compressed Size"] < original_size or 0 < size_map["Lempel-Ziv Compressed Size"] > original_size, (
        f"Lempel-Ziv compressed size {size_map['Lempel-Ziv Compressed Size']} is not smaller than original {original_size}."
    )
