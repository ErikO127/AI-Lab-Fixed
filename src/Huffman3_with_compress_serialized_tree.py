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
    """Calculate frequency of each character in the text."""
    return Counter(text)


def build_priority_queue(frequencies):
    """Build a priority queue from character frequencies."""
    heap = []
    for char, freq in frequencies.items():
        heapq.heappush(heap, Node(char, freq))
    return heap


def build_huffman_tree(heap):
    """Build Huffman Tree from the priority queue."""
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(root, current_code, codes):
    """Recursively traverse the tree to generate Huffman codes."""
    if root is None:
        return

    if root.char is not None:
        codes[root.char] = current_code

    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)


def get_huffman_codes(root):
    """Get Huffman codes for each character."""
    codes = {}
    generate_codes(root, "", codes)
    return codes


def serialize_tree(node):
    """Serialize the Huffman tree into a nested dictionary."""
    if node is None:
        return None
    if node.char is not None:
        return {"char": node.char, "freq": node.freq}
    return {
        "freq": node.freq,
        "left": serialize_tree(node.left),
        "right": serialize_tree(node.right),
    }


def compress(text, output_data_path='compressed_words.bin', output_tree_path='compressed_words.bin.tree'):

    """Compress the input text using Huffman coding and store the results in binary files."""
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

    byte_data = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder='big')

    with open(output_data_path, 'wb') as data_file:
        data_file.write(byte_data)

    tree_dict = serialize_tree(root)
    with open(output_tree_path, 'wb') as tree_file:
        pickle.dump((tree_dict, padding_length), tree_file)

    return byte_data, len(byte_data)
