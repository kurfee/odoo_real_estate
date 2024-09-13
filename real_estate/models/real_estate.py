import base64

from odoo import models, fields, api, http
from odoo.exceptions import UserError, ValidationError
import io
import xlsxwriter
from odoo.http import request


class Property(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Property'
    _inherit = ['mail.thread']
    _order = 'sequence'

    name = fields.Char(required=True, string="Property Name", tracking=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code", size=6)  # Restricting length to 6 characters
    date_availability = fields.Date(string="Available From", default=fields.Date.today)
    expected_price = fields.Float(string="Expected Price", required=True)  # Restrict to 2 decimal places
    selling_price = fields.Float(string="Selling Price")
    best_price = fields.Float(string="Best Offer", compute="_best_offer")
    bedrooms = fields.Integer(string="Number of Bedrooms", default=1)
    age = fields.Integer(string="Age", default=0, store=True)
    living_area = fields.Integer(string="Living Area (sqm)", required=True)
    facades = fields.Integer(string="Number of Facades", default=1)
    garage = fields.Boolean(string="Has Garage?")
    mature = fields.Boolean(string="Mature", compute='mature_enough')
    garden = fields.Boolean(string="Has Garden?")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(string="Total Area (sqm)", compute='_total_area')
    offers_ids = fields.One2many('estate.offers', 'property_id')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")
    state = fields.Selection(
        [
            ('canceled', 'Canceled'),
            ('sold', 'Sold'),
        ],
        tracking=True, string="Status")

    property_type_ids = fields.Many2one("estate.property.type", string="Property Type")
    buyer_ids = fields.Many2one("res.partner", string="Buyer")
    salesperson_ids = fields.Many2one("res.users", string="SalesPerson", default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    sequence = fields.Integer(string='Sequence')

    # New fields to store the number of smart buttons acctions
    offer_count = fields.Integer(string=" Offers", compute="_compute_offer_count", store=True)
    doc_count = fields.Integer(string=" Documents", store=True)
    approval_count = fields.Integer(string=" Pending Approvals", store=True)



    @api.depends('offers_ids')
    def _compute_offer_count(self):
        """Compute the number of offers for each property"""
        for property in self:
            property.offer_count = len(property.offers_ids)

    @api.depends('name')
    def _compute_doc_count(self):
        """Compute the number of offers for each property"""
        for property in self:
            return True

    @api.depends('name')
    def _compute_approval_count(self):
        """Compute the number of offers for each property"""
        for property in self:
            return True

    # this is about the smart buttons function
    def action_view_doc(self):
        """ This method will open a list view of offers related to the property """
        self.ensure_one()  # Ensures that the method is triggered only for a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Documents',
            'view_mode': 'tree,form',
            'res_model': 'estate.offers',
            'domain': [('property_id', '=', self.id)],  # Filters offers by the current property
            'context': {'default_property_id': self.id},
        }

    def action_view_approval(self):
        """ This method will open a list view of offers related to the property """
        self.ensure_one()  # Ensures that the method is triggered only for a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pending Approvals',
            'view_mode': 'tree,form',
            'res_model': 'estate.offers',
            'domain': [('property_id', '=', self.id)],  # Filters offers by the current property
            'context': {'default_property_id': self.id},
        }

    def action_view_offers(self):
        """ This method will open a list view of offers related to the property """
        self.ensure_one()  # Ensures that the method is triggered only for a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'view_mode': 'tree,form',
            'res_model': 'estate.offers',
            'domain': [('property_id', '=', self.id)],  # Filters offers by the current property
            'context': {'default_property_id': self.id},
        }

    # the functions section
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be canceled.")
            record.state = 'canceled'

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled property cannot be set as sold.")
            record.state = 'sold'

    # this is a function for the button to print the report
    def do_something(self):
        pass

    # compute and on_change functions

    @api.depends('offers_ids.price')
    def _best_offer(self):
        for record in self:
            # Calculate the best offer by getting the maximum price from related offers
            if record.offers_ids:
                record.best_price = max(record.offers_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.depends('garden_area', 'living_area')
    def _total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('age')
    def mature_enough(self):
        if self.age >= 25:
            self.mature = True
        else:
            self.mature = ''

    # Excel Report

    def action_generate_excel_report(self):
        # Ensure only one record is processed
        self.ensure_one()

        # Create an in-memory output file for the Excel file
        output = io.BytesIO()

        # Create a new Excel file using xlsxwriter
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Add a bold format for headers
        bold = workbook.add_format({'bold': True})

        # Add column headers
        worksheet.write('A1', 'Field', bold)
        worksheet.write('B1', 'Value', bold)

        # Write the record's data to the Excel sheet
        worksheet.write('A2', 'Name', bold)
        worksheet.write('B2', self.name or 'N/A')

        worksheet.write('A3', 'Status', bold)
        worksheet.write('B3', self.state or 0)

        #  Close the workbook after writing
        workbook.close()

        # Move the file pointer to the start of the in-memory buffer
        output.seek(0)

        # Read the data from the buffer
        xls_data = output.read()

        # Encode the data in base64 to store it as an Odoo attachment
        xls_data_base64 = base64.b64encode(xls_data)

        # Create an attachment record for downloading
        attachment = self.env['ir.attachment'].create({
            'name': 'real_estate_report.xlsx',
            'type': 'binary',
            'datas': xls_data_base64,
            'store_fname': 'real_estate_report.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        # Return the action to download the file
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }
