
from odoo import models,fields,api
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate.property.offer'


    price =fields.Integer()
    status = fields.Selection(selection= [('acepted','Accepted'),('refused','Refused')],copy =False)
    partner_id = fields.Many2one("res.partner", string="Partner",required=True)
    property_id = fields.Many2one("estate.property",string="Property", required = True)