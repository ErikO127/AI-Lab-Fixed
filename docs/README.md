This is the current documentation for the project that is being created. This project seeks to find the difference in effectiveness between two different compression algorithms. Currently the code is able to take file inputs and text strings and present a detailed and concise representation of their sizes. It presents pie chart size ratios of the text compressions to the original text, bar graphs that compare the sizes as well, and the initial text input place with raw numbers. As mentioned before the app can both take copy and paste texts and accept txt files that are drag and dropped into the app.

## Installation for getting the repositorty set up and tests run
1. Clone the repository: git clone https://github.com/ErikO127/AI-Lab-Fixed.git
2. Download all the dependincies that are needed for the project: poetry install
3. Make sure the virtual environment is set up: poetry shell
4. Run the following command in order to run the tests: poetry run pytest

## Explenations of the code structures

## Core compression models
**Huffman:**
- Implements the Huffman compression algorithm.
- Includes serialization of the Huffman tree for reconstruction.
- Provides methods for compressing and decompressing text.

**Lempel (LZW):**
- Implements the LZW compression algorithm.
- Efficient for repetitive patterns in text data.
- Includes compression and decompression functionality.

**User interface:**
- Handles the graphical interface for user interaction.
- Provides input fields for text and drag-and-drop file functionality.
- Displays visualizations like pie charts and bar graphs.

## Test files
**Test_Huffman:**
- Unit tests for Huffman compression and decompression functions.
- Verifies correctness of size reduction and tree serialization.

**Test_Lempel:**
- Unit tests for the LZW algorithm.
- Ensures the dictionary-based compression operates correctly.

**Test_ui:**
- Tests the user interface functionality.
- Validates input handling, visualization rendering, and integration with compression modules.

## How to Use

**Run the Application:**
Use the UI interface by running:
poetry run python UI_implementation.py

**Input Data:**
Enter text directly into the input field or drag-and-drop a .txt file.

**View Results:**
The app will display:
- Compression ratios as a pie chart.
- Comparison of original and compressed sizes as a bar graph.
- Raw size metrics for detailed analysis.

## Acknowledgements

**Huffman Encoding:** Claude Shannon and Robert Fano's foundational work on data compression.

**LZW Compression:** Terry Welch's adaptation of the original Lempel-Ziv algorithm.