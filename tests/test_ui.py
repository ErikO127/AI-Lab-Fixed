import os
import pytest
from pathlib import Path
from PyQt5.QtCore import Qt

from src.UI_implementation import CompressorUI

@pytest.fixture
def app(qtbot):
    widget = CompressorUI()
    qtbot.addWidget(widget)
    return widget

@pytest.fixture
def protein_file_in_tmp(tmp_path):
    """
    Copy protein_word.txt from src to the tmp_path and return its Path.
    """
    src_dir = Path(__file__).parent.parent / "src"
    source_file = src_dir / "protein_word.txt"
    target_file = tmp_path / "protein_word.txt"
    target_file.write_text(source_file.read_text(encoding="utf-8"), encoding="utf-8")
    return target_file

def test_ui_compress_protein_file(app, qtbot, protein_file_in_tmp):
    # 1) Simulate user selecting that file
    app.selected_files = [str(protein_file_in_tmp)]

    # 2) Click the "Compress..." button
    qtbot.mouseClick(app.compress_button, Qt.LeftButton)

    # 3) Parse the output text
    text_output = app.text_results.toPlainText()
    lines = text_output.strip().split("\n")

    parsed = {}
    for line in lines:
        if "Original Size:" in line:
            parsed["original"] = int(line.split(":")[1].strip().split()[0])
        elif "Huffman Compressed Size:" in line:
            parsed["huffman_compressed"] = int(line.split(":")[1].strip().split()[0])
        elif "Huffman Decompressed Size:" in line:
            parsed["huffman_decompressed"] = int(line.split(":")[1].strip().split()[0])
        elif "Lempel-Ziv Compressed Size:" in line:
            parsed["lzw_compressed"] = int(line.split(":")[1].strip().split()[0])
        elif "Lempel-Ziv Decompressed Size:" in line:
            parsed["lzw_decompressed"] = int(line.split(":")[1].strip().split()[0])

    # 4) Basic checks
    original_size = protein_file_in_tmp.stat().st_size

    assert parsed.get("original") == original_size, (
        f"UI reported original size {parsed.get('original')} "
        f"does not match actual file size {original_size}."
    )
    # Round-trip checks
    assert parsed.get("huffman_decompressed") == original_size, (
        "Huffman decompressed size should match the original file size."
    )
    assert parsed.get("lzw_decompressed") == original_size, (
        "LZW decompressed size should match the original file size."
    )
    # Compressed size checks
    assert parsed.get("huffman_compressed", 0) > 0, "Huffman compressed size should not be 0."
    assert parsed.get("lzw_compressed", 0) > 0, "LZW compressed size should not be 0."

    # Typically, these should be smaller for a decent sized text
    assert parsed["huffman_compressed"] < original_size, (
        f"Huffman compressed size {parsed['huffman_compressed']} is not smaller than original {original_size}."
    )
    assert parsed["lzw_compressed"] < original_size, (
        f"LZW compressed size {parsed['lzw_compressed']} is not smaller than original {original_size}."
    )
