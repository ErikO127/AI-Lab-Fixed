from collections import Counter

def analyze_frequency(input_file):
    """Analyze character frequency in the input file."""
    with open(input_file, 'r') as file:
        data = file.read()
    return Counter(data)


def initialize_dictionary_by_frequency(freq_counter):
    """Initialize the dictionary with characters sorted by frequency."""
    sorted_chars = sorted(freq_counter.keys(), key=lambda x: -freq_counter[x])
    dictionary = {char: idx for idx, char in enumerate(sorted_chars)}
    return dictionary, len(dictionary)


def lzw_compress(input_file, output_file):
    """Compress a text file using the enhanced LZW algorithm."""
    freq_counter = analyze_frequency(input_file)
    dictionary, dict_size = initialize_dictionary_by_frequency(freq_counter)

    with open(input_file, 'r') as file:
        data = file.read()

    string = ""
    compressed_data = []

    for symbol in data:
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            dictionary[string_plus_symbol] = dict_size
            dict_size += 1
            string = symbol

    if string:
        compressed_data.append(dictionary[string])

    with open(output_file, 'wb') as file:
        for code in compressed_data:
            file.write(code.to_bytes(2, byteorder='big'))  


if __name__ == "__main__":
    input_text_file = "words.txt" 
    compressed_file = "compressed.lzw"

    lzw_compress(input_text_file, compressed_file)


def compress(text):
    """Compress the input text using the LZW algorithm."""
    freq_counter = Counter(text)
    dictionary, dict_size = initialize_dictionary_by_frequency(freq_counter)
    
    string = ""
    compressed_data = []

    for symbol in text:
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            dictionary[string_plus_symbol] = dict_size
            dict_size += 1
            string = symbol

    if string:
        compressed_data.append(dictionary[string])
    
    return compressed_data
