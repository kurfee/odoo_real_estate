from odoo import models, fields

class ResPartnerSequance(models.Model):
    _inherit = 'res.partner'

    customer_sequence = fields.Char(string='Customer Sequence')
    vendor_sequence = fields.Char(string='Vendor Sequence')
    customer = fields.Boolean(string="Customer")
    vender = fields.Boolean(string="Vendor")
