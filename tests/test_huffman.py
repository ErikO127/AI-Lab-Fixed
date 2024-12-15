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
        """Background information:
The term spectrochemical can be broken into two different words describing what it means,
spectro- which refers to the electromagnetic spectrum, and chemical which links to atomic
chemical properties. Ligands are a part of a unique area in chemistry explaining many
phenomenons when it comes to colors that we observe and have been used by humans for a
long time stretching back as far as ancient egyptians and are still in us in today's world.
Coordination compounds are atomic compounds that are formed when a special types of bonds
are formed between the central ion and the outer ligands. The central ion is always metallic and
the outer ion can be a variety of different common non metallic molecules or atomic ions which
in a complex compound are named Ligands."""
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
