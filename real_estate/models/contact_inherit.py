from odoo import models, fields, api

class ResPartnerSequance(models.Model):
    _inherit = 'res.partner'

    customer_sequence = fields.Char(string='Customer Sequence', readonly=True, copy=False)
    vendor_sequence = fields.Char(string='Vendor Sequence', readonly=True, copy=False)
    customer = fields.Boolean(string="Customer's")
    vendor = fields.Boolean(string="Vendor's")



    # first we need to generate a sequence for vendors and customers when we tick
    @api.model
    def create(self, vals):

        if vals.get('customer') and not vals.get('customer_sequence'):
            vals['customer_sequence'] = self.env['ir.sequence'].next_by_code('res.partner.customer.sequence')

        if vals.get('vendor') and not vals.get('vendor_sequence'):
            vals['vendor_sequence'] = self.env['ir.sequence'].next_by_code('res.partner.vendor.sequence')

        return super(ResPartnerSequance, self).create(vals)

    # then we need to write these sequence to that exact contact
    def write(self, vals):
        for record in self:
            # Generate customer sequence if 'customer' is ticked and no sequence exists
            if vals.get('customer') and not record.customer_sequence:
                vals['customer_sequence'] = self.env['ir.sequence'].next_by_code('res.partner.customer.sequence')


            # Generate vendor sequence if 'vendor' is ticked and no sequence exists
            if vals.get('vendor') and not record.vendor_sequence:
                vals['vendor_sequence'] = self.env['ir.sequence'].next_by_code('res.partner.vendor.sequence')

        return super(ResPartnerSequance, self).write(vals)