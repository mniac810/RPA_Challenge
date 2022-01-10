from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.FileSystem import FileSystem


class ExcelMaker():

    def __init__(self, content, name, path, exclude_keys, workbook=None):
        excel = Files()
        if workbook is None:
            self._workbook = excel.create_workbook(path=path)
        else:
            self._workbook = workbook    
        self._content = content
        self._name = name
        self._path = path
        self._exclude_keys = exclude_keys
        self._headers_index = {}
        self._workbook.create_worksheet(name)

    # Medium: naming inconsistent
    def _set_headers(self, headers):
        for num, val in enumerate(headers):
            if val != self._exclude_keys:
                self._headers_index[val] = num + 1
                self._workbook.set_cell_value(1, num + 1, val, self._name)

    def _set_row(self, row, row_id):
        for key, value in row.items():
            if key != self._exclude_keys:
                self._workbook.set_cell_value(row_id, self._headers_index[key],
                                              value, self._name)

    def set_content(self):
        self._set_headers(self._content[0].keys())
        row = {}
        for num, row in enumerate(self._content):
            self._set_row(row, num + 2)

    def get_workbook(self):
        return self._workbook

    def save_workbook(self):
        self._workbook.save(self._path)

    def close(self):
        self._workbook.close()
        self._values = None
