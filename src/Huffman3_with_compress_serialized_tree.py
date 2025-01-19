import heapq
import pickle
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def calculate_frequency(text):
    return Counter(text)


def build_priority_queue(frequencies):
    heap = []
    for char, freq in frequencies.items():
        heapq.heappush(heap, Node(char, freq))
    return heap


def build_huffman_tree(heap):
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(root, current_code, codes):
    if root is None:
        return

    if root.char is not None:
        codes[root.char] = current_code

    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)


def get_huffman_codes(root):
    codes = {}
    generate_codes(root, "", codes)
    return codes


def serialize_tree(node):
    if node is None:
        return None
    if node.char is not None:
        return {"char": node.char, "freq": node.freq}
    return {
        "freq": node.freq,
        "left": serialize_tree(node.left),
        "right": serialize_tree(node.right),
    }


def deserialize_tree(tree_dict):
    if tree_dict is None:
        return None
    if "char" in tree_dict:
        return Node(tree_dict["char"], tree_dict["freq"])
    node = Node(None, tree_dict["freq"])
    node.left = deserialize_tree(tree_dict["left"])
    node.right = deserialize_tree(tree_dict["right"])
    return node


def compress(input_text_file, output_data_path="compressed_words.bin", output_tree_path="compressed_words.bin.tree"):
    """Compress the input text file using Huffman coding and save the results."""
    with open(input_text_file, "r") as file:
        text = file.read()

    frequencies = calculate_frequency(text)
    heap = build_priority_queue(frequencies)
    root = build_huffman_tree(heap)
    huffman_codes = get_huffman_codes(root)

    encoded_text = "".join(huffman_codes[char] for char in text)

    if len(encoded_text) % 8 != 0:
        padding_length = 8 - len(encoded_text) % 8
        encoded_text += "0" * padding_length
    else:
        padding_length = 0

    byte_data = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder="big")

    with open(output_data_path, "wb") as data_file:
        data_file.write(byte_data)

    tree_dict = serialize_tree(root)
    with open(output_tree_path, "wb") as tree_file:
        pickle.dump((tree_dict, padding_length), tree_file)


def decompress(
    input_data_path="compressed_words.bin",
    input_tree_path="compressed_words.bin.tree",
    output_text_path="huffman_decompressed.txt",
):
    """Decompress the binary file and save the decompressed text to a file."""
    with open(input_tree_path, "rb") as tree_file:
        tree_dict, padding_length = pickle.load(tree_file)

    root = deserialize_tree(tree_dict)

    with open(input_data_path, "rb") as data_file:
        byte_data = data_file.read()

    bit_string = "".join(f"{byte:08b}" for byte in byte_data)
    if padding_length > 0:
        bit_string = bit_string[:-padding_length]

    decoded_text = []
    current_node = root

    for bit in bit_string:
        current_node = current_node.left if bit == "0" else current_node.right

        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = root

    decompressed_text = "".join(decoded_text)

    # Write the decompressed text to the output file
    with open(output_text_path, "w") as output_file:
        output_file.write(decompressed_text)


if __name__ == "__main__":
    input_text_file = "words.txt"
    compressed_file = "huffman_compressed.bin"
    tree_file = "huffman_tree.bin"
    decompressed_file = "huffman_decompressed.txt"

    # Compress the input file
    compress(input_text_file, compressed_file, tree_file)

    # Decompress to the output file
    decompress(compressed_file, tree_file, decompressed_file)


