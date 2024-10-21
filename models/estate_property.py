# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate.property'

    name = fields.Char(required =True)
    living_area = fields.Integer()
    postcode=fields.Char() 
    facades =fields.Integer()
    date_availability = fields.Date(default=lambda self: datetime.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(string='Expected Price', required =True)
    selling_price=fields.Float(readonly=True,copy=False)
    description = fields.Text()
    bedrooms =fields.Integer(default=2)
    garage =fields.Boolean()
    garden =fields.Boolean()
    garden_area =fields.Integer()
    garden_orientation = fields.Selection(selection=[('east', 'East'), ('west', 'West'), ('south', 'South'), ('north', 'North')], string='Garden Orientation')
    active =fields.Boolean( default =True)
    state =fields.Selection( selection=[('new','New'),('offer_recived','Offer Received'),(' offer_accepted',"offer accepted"),('sold','Sold'),('cancelled','Canceled')],default ='new',required =True,copy =False)
    property_type_id = fields.Many2one("estate.property.type" , string="Property Type")
    partner_id = fields.Many2one("res.partner", string="Partner")
    sales_person_id = fields.Many2one("res.users", string ="Sales Person")
    tag_ids = fields.Many2many("estate.property.tag",string="Tags")
    offer_ids = fields.One2many("estate.property.offer", 'property_id', string="offers")
