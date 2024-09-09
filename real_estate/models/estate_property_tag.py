from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'

    name = fields.Char(string="Property Tag", required=True)