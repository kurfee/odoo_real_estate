from odoo import models, api, exceptions, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        product_id = vals.get('product_id')
        if product_id:
            product = self.env['product.product'].browse(product_id)
            if not product.exists():
                raise exceptions.UserError(_("You cannot create a new product directly in the Sale Order Line."))
        return super(SaleOrderLine, self).create(vals)
