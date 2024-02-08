from odoo import models,fields

class Quotations(models.Model):
    _name = 'transmove.quotations'
    _description = 'this table is used to store Quotations information'


    customer_name = fields.Char(string='Customer Name')
    origin = fields.Char(string='Origin')
    destination = fields.Char(string='Destination')
    mode_of_transport = fields.Selection(selection=[('air','Air'),('sea','Sea')])
    #shipment details
    weight = fields.Float(string='Weight of shipment(kg)')
    Quantity = fields.Integer(string='Quantity Of items')
    description = fields.Text(string='Brief Description')
    expiration_date = fields.Date()
    terms_conditions = fields.Text(string='Terms & Conditions')   
