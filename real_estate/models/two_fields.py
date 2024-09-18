from odoo import models, fields, api


class SaleQuotationFields(models.Model):
    _inherit = 'sale.order.line'


    quotation_date = fields.Datetime(string="Last Quotation Date", compute="_last_price")
    quotation_price = fields.Float(string="Last Unit Price", compute="_last_price")


    # def _last_date(self):
    #     for record in self:
    #         quotation_date = self.env['sale.order.line'].search(
    #             [('create_date', '=', record.product_template_id.id)],  # Ensure partner_id matches
    #             order='create_date desc',
    #             limit=1
    #         )
    #         record.quotation_date = quotation_date.create_date if quotation_date else False

    @api.depends('product_template_id')
    def _last_price(self):
        for record in self:
            # Search for the last price on sale.order.line for the product
            last_order_line = self.env['sale.order.line'].search(
                [('product_template_id', '=', record.product_template_id.id)],  # Check product_id, not price_unit
                order='create_date desc',  # Sort by creation date, not price
                limit=1
            )
            record.quotation_price = last_order_line.price_unit if last_order_line else 0.0  # Set 0 if no record
            record.quotation_date = last_order_line.create_date if last_order_line else False