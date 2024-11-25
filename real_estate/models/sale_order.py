from odoo import fields, models, api
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    type = fields.Selection([
        ('quotation', 'Quotation'),
        ('service', 'Service'),
    ], string="Type", default="quotation")

    end_date = fields.Date(string="End Date")

    def action_confirm(self):
        # Call the original confirm method
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.end_date and order.end_date > date.today():
                # Create a new quotation
                new_quotation = order.copy({
                    'state': 'draft',
                    'origin': order.name,
                })
                self.env.cr.commit()  # Save the New Quotation
        return res