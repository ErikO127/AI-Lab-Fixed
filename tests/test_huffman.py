import os
from pathlib import Path
import pytest

from src.Huffman3_with_compress_serialized_tree import (
    compress as huffman_compress,
    decompress as huffman_decompress,
)

@pytest.fixture
def protein_text():
    """
    Reads the protein_word.txt file from the src folder
    and returns its contents.
    """
    # Path to this test file: tests/test_huffman.py
    # We want to go up one directory -> parent, then into src folder
    src_dir = Path(__file__).parent.parent / "src"
    text_path = src_dir / "protein_word.txt"
    return text_path.read_text(encoding="utf-8")


def test_huffman_compress_decompress(tmp_path, protein_text):
    # 1) Write text to a temp file
    input_file = tmp_path / "test_input_huffman.txt"
    input_file.write_text(protein_text, encoding="utf-8")

    # Output files
    compressed_file = tmp_path / "test_huffman_compressed.bin"
    tree_file = tmp_path / "test_huffman_tree.bin"
    decompressed_file = tmp_path / "test_huffman_decompressed.txt"

    # 2) Compress
    huffman_compress(str(input_file), str(compressed_file), str(tree_file))
    assert compressed_file.exists(), "Huffman compressed file was not created."
    assert tree_file.exists(), "Huffman tree file was not created."

    # 3) Decompress
    huffman_decompress(str(compressed_file), str(tree_file), str(decompressed_file))
    assert decompressed_file.exists(), "Huffman decompressed file was not created."

    # 4) Check round-trip
    decompressed_text = decompressed_file.read_text(encoding="utf-8")
    assert decompressed_text == protein_text, "Huffman decompressed text does not match the original."

    # 5) Check size difference
    original_size = len(protein_text.encode("utf-8"))
    compressed_size = compressed_file.stat().st_size
    assert compressed_size < original_size, (
        f"Expected Huffman-compressed size {compressed_size} to be less than original {original_size}."
    )
