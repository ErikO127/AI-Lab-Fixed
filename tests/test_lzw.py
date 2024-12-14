from src.Lempel_with_compress import lzw_compress
from pathlib import Path
import os

def test_lzw_compress_real_data(tmp_path):
    # Copy the words.txt file into the temp directory
    input_file = tmp_path / "words.txt"
    output_file = tmp_path / "test_output.lzw"

    # Write the sample text to the input file
    input_file.write_text("A spectrometric investigation of the correlation between complex ions and their ligands")

    # Compress the input file using the actual LZW function
    lzw_compress(str(input_file), str(output_file))

    # Assert the compressed file is created
    assert os.path.exists(output_file)

    # Calculate the compressed file size dynamically
    compressed_size = os.path.getsize(output_file)

    # Assert the compressed size is what we expect it to be
    original_size = os.path.getsize(input_file)
    assert compressed_size > 0  # Compressed file should not be empty
    assert compressed_size < original_size  # Compression should reduce file size

