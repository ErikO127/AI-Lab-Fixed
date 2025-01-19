import pickle

def lzw_compress(input_file, compressed_file):
    """Compress the file with LZW and store just the codes + the set of unique chars."""

    # 1. Read the entire input
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    if not text:
        # Edge case: empty file
        with open(compressed_file, 'wb') as f:
            pickle.dump([], f)
        return

    # 2. Create the initial dictionary from unique characters
    unique_chars = sorted(set(text))
    # Map each unique char to its code
    dictionary = {ch: i for i, ch in enumerate(unique_chars)}
    dict_size = len(dictionary)

    # 3. LZW compression
    string = ""
    compressed_data = []

    for symbol in text:
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary:
            # Keep extending the string
            string = string_plus_symbol
        else:
            # Output the code for string
            compressed_data.append(dictionary[string])
            # Add new sequence (string+symbol) to the dictionary
            dictionary[string_plus_symbol] = dict_size
            dict_size += 1
            # Reset the current string to the current symbol
            string = symbol

    # If there's something left in 'string' at the end, output its code
    if string:
        compressed_data.append(dictionary[string])

    # 4. Store in a pickle:
    #    - the list of unique_chars so decompression can rebuild the initial dictionary
    #    - the compressed list of codes
    with open(compressed_file, 'wb') as f:
        pickle.dump((unique_chars, compressed_data), f)


def lzw_decompress(compressed_file, output_file):
    """Decompress an LZW file that stores only the codes + initial alphabet."""
    with open(compressed_file, 'rb') as f:
        data = pickle.load(f)

    # If the compressed file was empty or had no data
    if not data:
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write("")
        return

    unique_chars, compressed_data = data

    # 1. Build the initial reverse dictionary
    #    Map code -> character
    reverse_dict = {i: ch for i, ch in enumerate(unique_chars)}
    dict_size = len(reverse_dict)

    # 2. Standard LZW decompression logic
    #    Grab the first code and decode it
    old_code = compressed_data[0]
    decompressed = [reverse_dict[old_code]]  # List of strings, to join at the end

    for new_code in compressed_data[1:]:
        if new_code in reverse_dict:
            current_string = reverse_dict[new_code]
        else:
            # Special LZW 'K W K' case
            current_string = reverse_dict[old_code] + reverse_dict[old_code][0]

        # Append to output
        decompressed.append(current_string)

        # Add new sequence to the dictionary: old_string + first_char_of_current_string
        reverse_dict[dict_size] = reverse_dict[old_code] + current_string[0]
        dict_size += 1

        old_code = new_code

    # 3. Write out the decompressed text
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("".join(decompressed))


if __name__ == "__main__":
    # Example usage
    in_file = "words.txt"
    comp_file = "compressed.lzw"
    decomp_file = "decompressed.txt"

    lzw_compress(in_file, comp_file)
    lzw_decompress(comp_file, decomp_file)
