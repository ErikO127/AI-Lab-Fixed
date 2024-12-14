from src.Huffman3_with_compress_serialized_tree import compress
from pathlib import Path
import os

def test_huffman_compress_real_data(tmp_path):
    # Copy the words.txt file into the temp directory
    input_file = tmp_path / "words.txt"
    output_data_path = tmp_path / "compressed.bin"
    output_tree_path = tmp_path / "tree.pkl"

    # Write sample text from words.txt to the temporary file
    input_file.write_text(
        """A spectrometric investigation of the correlation between complex ions and their ligands"""
    )

    with open(input_file, "r") as f:
        text = f.read()

    compressed_data, compressed_size = compress(
        text, str(output_data_path), str(output_tree_path)
    )

    # Assert output files are created
    assert os.path.exists(output_data_path)
    assert os.path.exists(output_tree_path)

    # Assert compressed size is smaller than original
    assert compressed_size < len(text)
