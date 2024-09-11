import io
import xlsxwriter
from odoo import models

class RealEstateExcelReport(models.AbstractModel):
    _name = 'report.real_estate.report_property_xlsx'
    _description = 'Real Estate Excel Report'

    def generate_xlsx_report(self, data, objects):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Set headers
        headers = ['ID', 'Name', 'Price', 'Status']
        worksheet.write_row(0, 0, headers)

        # Write data for each real estate property
        row = 1
        for obj in objects:
            worksheet.write(row, 0, obj.id)
            worksheet.write(row, 1, obj.name)
            worksheet.write(row, 2, obj.price)
            worksheet.write(row, 3, obj.state)
            row += 1

        workbook.close()
        output.seek(0)
        return output.getvalue()
