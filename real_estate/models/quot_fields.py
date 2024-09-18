from odoo import models, fields, api

class OrderQuotationFields(models.Model):
    _inherit = 'sale.order'

    last_quotation_date = fields.Date(string="Last Quotation Date")
    last_quotation_price = fields.Char(string="Last Quotation Price")


