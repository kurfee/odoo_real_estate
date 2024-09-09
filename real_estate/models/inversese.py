from odoo import models, fields, api

class TtootaTest(models.Model):
    _name = 'ttoota.test'

    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity")
    total_price = fields.Float(string="Total Price", compute="_compute_total_price", inverse="_set_total_price")

    @api.depends('unit_price', 'quantity')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.unit_price * record.quantity

    def _set_total_price(self):
        for record in self:
            if record.quantity:
                record.unit_price = record.total_price / record.quantity

# very powerfull inverse some time we might want to know the clinet oppenion on something and contiue with the callculation...