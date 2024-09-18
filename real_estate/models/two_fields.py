from odoo import models, fields, api

class SaleQuotationFields(models.Model):
    _inherit = 'sale.order.line'

    last_quotation_date = fields.Date(string="Last Quotation Date")
    last_quotation_price = fields.Char(string="Last Quotation Price")


