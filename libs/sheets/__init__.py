import re
from typing import List

import gspread
from gspread import WorksheetNotFound

from libs.constants import OperationTypes
from libs.models import Operation
from libs.utils import get_now


class SheetsClient:
    _template_title = "template"
    _title_format = "%m/%Y"
    _date_format = "%d.%m.%Y"
    _first_row = 4
    _income_column = 1
    _expenses_column = 5

    def __init__(self, credentials: dict, sheet_id: str):
        self.service = gspread.service_account_from_dict(credentials)
        self.sheet = self.service.open_by_key(sheet_id)

    def _get_current_title(self):
        return get_now().strftime(self._title_format)

    def _create_page_from_template(self, title):
        template = self.sheet.worksheet(self._template_title)
        new_worksheet_data = template.copy_to(self.sheet.id)
        worksheet = self.sheet.get_worksheet_by_id(new_worksheet_data['sheetId'])
        worksheet.update_title(title)
        return worksheet

    def _get_current_page(self):
        title = self._get_current_title()

        try:
            page = self.sheet.worksheet(title)
        except WorksheetNotFound:
            page = self._create_page_from_template(title)

        return page

    @staticmethod
    def _upload_operations(page, in_column, values):
        cells = page.findall(re.compile(r"\d"), in_column=in_column + 1)
        if len(cells):
            row = cells[-1].row + 1
        else:
            row = 4

        address = page.cell(row, in_column).address
        page.update(address, values, raw=False)

    def upload_operations(self, operations: List[Operation]):
        current_page = self._get_current_page()

        self._upload_operations(
            current_page,
            self._expenses_column,
            [
                [str(o.category.name), o.amount, str(o.created_at.strftime(self._date_format)), o.comment or ""]
                for o
                in operations if o.type == OperationTypes.Expenses
            ]
        )

        self._upload_operations(
            current_page,
            self._income_column,
            [
                [str(o.category.name), o.amount, str(o.created_at.strftime(self._date_format)), o.comment or ""]
                for o
                in operations if o.type == OperationTypes.Income
            ]
        )
