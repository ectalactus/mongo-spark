from unittest import TestCase, main
import datetime

from ColumnTest import ColumnTest
from RetailScrapper import RetailScrapper
from errors.FileFormatError import FileFormatError
from utils.FileUtils import FileUtils
from utils.ObjectUtils import ObjectUtils


class TestScrapper(TestCase):

    def test_value_column_parser(self):
        self.assertEqual(ObjectUtils.to_string("test"), "test")
        self.assertEqual(ObjectUtils.to_integer("42"), 42)
        self.assertEqual(ObjectUtils.to_number("42.21"), 42.21)
        self.assertEqual(ObjectUtils.to_datetime("2010-12-01 08:34:00"), datetime.datetime(2010, 12, 1, 8, 34))

        self.assertRaises(ValueError, ObjectUtils.to_integer, "42D")
        self.assertRaises(ValueError, ObjectUtils.to_datetime, "2010-14-01 08:34:00")

    def test_file_type(self):
        try:
            FileUtils.check_file_type("test_file.xlsx", ".xlsx")
        except:
            self.assertTrue(False)

        self.assertRaises(FileFormatError, FileUtils.check_file_type, "test_file.doc", ".xlsx")

    def test_parsing_row(self):
        scrapper = RetailScrapper(None, None)
        retail = scrapper.parse_row([
            ColumnTest("536365"),
            ColumnTest("84029"),
            ColumnTest("KNITTED UNION FLAG HOT WATER BOTTLE"),
            ColumnTest("6"),
            ColumnTest("2010-12-01 08:34:00"),
            ColumnTest("2.75"),
            ColumnTest("17850"),
            ColumnTest("United Kingdom"),
        ], "Test Sheet")

        self.assertEqual(retail['invoice_id'], 536365)
        self.assertEqual(retail['stock_code'], "84029")
        self.assertEqual(retail['description'], "KNITTED UNION FLAG HOT WATER BOTTLE")
        self.assertEqual(retail['quantity'], 6)
        self.assertEqual(retail['invoice_date'], datetime.datetime(2010, 12, 1, 8, 34))
        self.assertEqual(retail['price'], 2.75)
        self.assertEqual(retail['customer_id'], 17850)
        self.assertEqual(retail['country'], "United Kingdom")


if __name__ == '__main__':
    main()
