from odoo import models
from odoo.exceptions import UserError
import io
import xlsxwriter

class RealEstateXlsxReport(models.AbstractModel):
    _name = 'report.real_estate.report_xlsx'
    _description = 'Real Estate XLSX Report'
    # _inherit = 'report.report_xlsx'

    def generate_xlsx_report(self, workbook, data, properties):
        # Create a new Excel sheet
        sheet = workbook.add_worksheet('Real Estate Report')

        # Define formats
        bold = workbook.add_format({'bold': True})

        # Define headers
        headers = ['Property Name', 'Selling Price', 'Buyer', 'State']
        sheet.write_row(0, 0, headers, bold)

        # Write data to the sheet
        row = 1
        for property in properties:
            sheet.write(row, 0, property.name)
            sheet.write(row, 1, property.price)
            sheet.write(row, 2, property.buyer_id.name or '')
            sheet.write(row, 3, property.state)
            row += 1

        if row == 1:
            raise UserError("No data found for the report.")

        # Optional: You can add more formatting or conditional formatting here

