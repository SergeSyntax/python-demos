import unittest
from main import do_stuff


class TestMain(unittest.TestCase):
    """check do_stuff function"""

    def setUp(self) -> None:
        print("\n setup before each")
        return super().setUp()

    def test_do_stuff(self):
        """it return the correct calculation"""
        test_param = 10
        result = do_stuff(test_param)
        self.assertEqual(15, result)

    def test_value_err(self):
        """it return error on wrong type"""
        with self.assertRaises(ValueError):
            do_stuff("test")

    def tearDown(self) -> None:
        print("\n teardown before each")
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
