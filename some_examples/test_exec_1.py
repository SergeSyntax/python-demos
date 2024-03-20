from unittest import TestCase, main
from unittest.mock import patch
from exec_1 import translate_to_chines


class TestTranslateToChines(TestCase):
    @patch("exec_1.GoogleTranslator.translate")
    def test_translation(self, mock_translate):
        translate_to_chines("hello")
        mock_translate.assert_called_once_with("hello")


if __name__ == "__main__":
    main()
