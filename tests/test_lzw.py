import os
from pathlib import Path
import pytest

from src.Lempel_with_compress import lzw_compress, lzw_decompress

@pytest.fixture
def protein_text():
    """
    Reads the protein_word.txt file from the src folder
    and returns its contents.
    """
    src_dir = Path(__file__).parent.parent / "src"
    text_path = src_dir / "protein_word.txt"
    return text_path.read_text(encoding="utf-8")


def test_lzw_compress_decompress(tmp_path, protein_text):
    # 1) Write text to a temp file
    input_file = tmp_path / "test_input_lzw.txt"
    input_file.write_text(protein_text, encoding="utf-8")

    # Output files
    compressed_file = tmp_path / "test_output.lzw"
    decompressed_file = tmp_path / "test_lzw_decompressed.txt"

    # 2) Compress
    lzw_compress(str(input_file), str(compressed_file))
    assert compressed_file.exists(), "LZW compressed file not created."

    # 3) Decompress
    lzw_decompress(str(compressed_file), str(decompressed_file))
    assert decompressed_file.exists(), "LZW decompressed file not created."

    # 4) Verify round-trip
    decompressed_text = decompressed_file.read_text(encoding="utf-8")
    assert decompressed_text == protein_text, "LZW decompressed text does not match the original."

    # 5) Check size difference
    original_size = input_file.stat().st_size
    compressed_size = compressed_file.stat().st_size
    assert compressed_size < original_size, (
        f"Expected LZW compressed size {compressed_size} to be less than original {original_size}."
    )
