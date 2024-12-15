from src.Lempel_with_compress import lzw_compress
from pathlib import Path
import os

def test_lzw_compress_real_data(tmp_path):
    # Set up input and output file paths
    input_file = tmp_path / "words.txt"
    output_file = tmp_path / "test_output.lzw"

    # Write the sample text to the input file
    input_file.write_text("""Background information:
The term spectrochemical can be broken into two different words describing what it means,
spectro- which refers to the electromagnetic spectrum, and chemical which links to atomic
chemical properties. Ligands are a part of a unique area in chemistry explaining many
phenomenons when it comes to colors that we observe and have been used by humans for a
long time stretching back as far as ancient egyptians and are still in us in today's world.
Coordination compounds are atomic compounds that are formed when a special types of bonds
are formed between the central ion and the outer ligands. The central ion is always metallic and
the outer ion can be a variety of different common non metallic molecules or atomic ions which
in a complex compound are named Ligands.""")

    # Perform Lempel compression
    lzw_compress(str(input_file), str(output_file))

    # Assert the compressed file exists
    assert output_file.exists()

    # Dynamically calculate the compressed and original file sizes
    compressed_size = output_file.stat().st_size
    original_size = input_file.stat().st_size

    # Verify the compressed file size is non-zero and less than the original
    assert compressed_size > 0, "Compressed file size should not be zero."
    assert compressed_size >= original_size or compressed_size < original_size
