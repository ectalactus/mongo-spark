import logging

import openpyxl
import os
import argparse
import sys
import time

from connectors.MongoConnector import MongoConnector
from errors.FileFormatError import FileFormatError
from utils.BaseLogger import init_base_logger
from utils.FileUtils import FileUtils
from utils.ObjectUtils import ObjectUtils

my_logger = logging.getLogger('my_logger')


class RetailScrapper:

    def __init__(self, mongo_host, mongo_port):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port

        self.__parser_dic_func = [
            ["invoice_id", ObjectUtils.to_integer],
            ["stock_code", ObjectUtils.to_string],
            ["description", ObjectUtils.to_string],
            ["quantity", ObjectUtils.to_integer],
            ["invoice_date", ObjectUtils.to_datetime],
            ["price", ObjectUtils.to_number],
            ["customer_id", ObjectUtils.to_integer],
            ["country", ObjectUtils.to_string]
        ]
        self.min_column_length = len(self.__parser_dic_func)

    def parse_file(self, file_path):
        wb_obj = self.__check_and_load_input_file(file_path)

        row_idx = 1
        is_header = True
        retails = []
        mongo_connector = None
        start = time.time()

        try:
            mongo_connector = MongoConnector(self.mongo_host, self.mongo_port)
            mongo_connector.connect()

            for sheet in wb_obj.worksheets:
                sheet_name = sheet.title
                for row in sheet.rows:
                    if is_header:
                        is_header = False
                        continue
                    if len(row) < self.min_column_length:
                        raise FileFormatError(
                            "Invalid column lengths at line {} in sheet {}".format(row_idx, sheet_name))
                    try:
                        retails.append(self.parse_row(row, sheet_name))
                    except Exception as e:
                        my_logger.error(e)

                    self.__insert_retails(mongo_connector, retails)
                    row_idx += 1

            self.__insert_retails(mongo_connector, retails, True)

        except Exception as e:
            my_logger.error(e)
        finally:
            if mongo_connector:
                mongo_connector.disconnect()
            my_logger.info("Parse file in {} sec".format(time.time() - start))

    def __insert_retails(self, mongo_connector, retails, force_insert=False):
        retails_length = len(retails)
        if retails_length > 0 and (len(retails) % 1000 == 0 or force_insert):
            try:
                mongo_connector.insert_bulk_retails(retails)
            except Exception as e:
                my_logger.error(e)
            finally:
                retails.clear()

    def parse_row(self, row, sheet_name):
        retail = {}
        i = 0
        column_errors = []

        while i < len(self.__parser_dic_func):
            try:
                retail[self.__parser_dic_func[i][0]] = self.__parser_dic_func[i][1](row[i].value)
            except Exception as e:
                my_logger.warning(e)
                column_errors.append(row[i].coordinate)
            i += 1
        if retail['quantity'] < 0:
            raise FileFormatError("Parse error in sheet {}, columns : {}, quantity invalid".format(sheet_name, ", ".join(column_errors)))
        if len(column_errors) > 0:
            raise FileFormatError("Parse error in sheet {}, columns : {}".format(sheet_name, ", ".join(column_errors)))
        return retail

    def __check_and_load_input_file(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError
        FileUtils.check_file_type(file_path, ".xlsx")
        return openpyxl.load_workbook(file_path)


def parse_argv():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-mongo_host', required=False, default="localhost", help="Set mongodb host")
        parser.add_argument('-mongo_port', required=False, default=27017, type=int, help="Set mongodb port")
        parser.add_argument('-file', required=True, help="Set xlsx file path")
        return parser.parse_args()
    except Exception as e:
        my_logger.exception(e)
        sys.exit(2)


if __name__ == "__main__":
    init_base_logger()
    args = parse_argv()
    scrapper = RetailScrapper(args.mongo_host, args.mongo_port)
    scrapper.parse_file(args.file)
