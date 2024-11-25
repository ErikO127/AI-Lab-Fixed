from src.ai_labs_project.Lempel_with_compress import lzw_compress
from pathlib import Path
import os

def test_lzw_compress_real_data(tmp_path):
    # Copy the words.txt file into the temp directory
    input_file = tmp_path / "words.txt"
    output_file = tmp_path / "test_output.lzw"

    # Write sample text from words.txt to the temporary file
    input_file.write_text(
        "ABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABAB"
    )

    lzw_compress(str(input_file), str(output_file))

    # Assert output file is created
    assert os.path.exists(output_file)

    # Assert the compressed file is not empty
    assert os.path.getsize(output_file) > 0

    # Optional: Compare sizes for compressible input
    assert os.path.getsize(output_file) <= os.path.getsize(input_file)

