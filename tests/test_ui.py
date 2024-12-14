from src.UI_implementation import CompressorUI
from unittest.mock import MagicMock
import pytest
from PyQt5.QtCore import Qt

@pytest.fixture
def app(qtbot):
    widget = CompressorUI()
    qtbot.addWidget(widget)
    return widget

def test_ui_compress_words_file(app, qtbot, tmp_path):
    # Simulate user input with content from words.txt
    app.text_input.setPlainText(
        """A spectrometric investigation of the correlation between complex ions and their ligands"""
    )

    # Click the compress button
    qtbot.mouseClick(app.compress_button, Qt.LeftButton)

    # Verify the results are displayed correctly
    expected_output = (
        "Original Text Size: 87 bytes\n"
        "Huffman Compressed Size: 45 bytes\n"
        "Lempel-Ziv Compressed Size: 74 bytes\n"
    )
    assert app.text_results.toPlainText() == expected_output

