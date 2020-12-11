import unittest

from bot.commandListener import _parse_date

# commandListener = __import__("commandListener.py")


class TestCmdListener(unittest.TestCase):
    def test_date_parse(self):
        """
        Test that date parsing works properly
        """
        from datetime import datetime, date

        # '%Y-%m-%d', '%Y%m%d', '%y-%m-%d', '%y%m%d', '%m-%d', '%m%d'
        dates = {
            '2020-10-21': datetime(year=2020, month=10, day=21),
            '20201021': datetime(year=2020, month=10, day=21),
            '20-10-21': datetime(year=2020, month=10, day=21),
            '201021': datetime(year=2020, month=10, day=21),
            '10-21': datetime(year=2020, month=10, day=21),
            '1021': datetime(year=2020, month=10, day=21),
        }

        for format, date in dates.items():
            self.assertEqual(_parse_date(format), date)

if __name__ == "__main__":
    unittest.main()
