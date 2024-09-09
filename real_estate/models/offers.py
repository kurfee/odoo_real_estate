from datetime import timedelta
from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.offers'
    _description = 'this is offers model here we handle all offers'


    price = fields.Float(string="Price")
    property_id = fields.Many2one('real.estate', string="offers_id")
    partner_id = fields.Many2one('res.partner', string="Buyer")
    state = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status")

    validity = fields.Integer(string='Validity (days)')
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', store=True)


    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today()


    def action_accept(self):
        for record in self:
            if record.state != 'accepted':
                # Set the buyer and selling price on the property
                record.property_id.buyer_ids = record.partner_id.id
                record.property_id.selling_price = record.price
                record.state = 'accepted'

    def action_refuse(self):
        for record in self:
            if record.state != 'refused':
                record.state = 'refused'



