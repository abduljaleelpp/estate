# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate.property'
    _order = "id desc"

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
    state =fields.Selection( selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted',"Offer Accepted"),('sold','Sold'),('cancelled','Cancelled')],default ='new',required =True,copy =False)
    property_type_id = fields.Many2one("estate.property.type" , string="Property Type")
    partner_id = fields.Many2one("res.partner", string="Buyer")
    sales_person_id = fields.Many2one("res.users", string ="Sales Person", index=True, tracking=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag",string="Tags")
    offer_ids = fields.One2many("estate.property.offer", 'property_id', string="offers")
    total_area =fields.Float(compute="_compute_total")
    best_price = fields.Integer(compute="_compute_best_offer", string = "Best offer")
   

    @api.depends("garden_area","living_area")
    def _compute_total(self):
         for record in self:
            record.total_area = record.garden_area + record.living_area
    

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
        # Get all prices from offer_ids, ensuring to skip over any that are None or not set
            prices = record.offer_ids.mapped('price')
        # Calculate the maximum price if there are any prices, otherwise set to 0
            record.best_price = max(prices) if prices else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area =10
            self.garden_orientation ='north'
        else:
            self.garden_area = 0
            self.garden_orientation = False    


    def action_sold(self):
        for record in self:
            if record.state not in ['sold','cancelled']:
                record.state = 'sold'
                return True
            else:
                raise UserError("sold and cancelled properties can be set sold or cancelled again")
                return False
            
    def action_cancel(self):
        for record in self:
            if record.state not in ['sold','cancelled']:
                record.state = 'cancelled'
                return True
            else:
                raise UserError("sold and cancelled properties can be set cancelled again")
                return False

    @api.ondelete(at_uninstall=False)
    def _check_state_on_delete(self):
        # Ensure only properties in 'new' or 'cancelled' state can be deleted
        if any(property.state not in ['new', 'cancelled'] for property in self):
            raise UserError("Only properties in 'New' or 'Cancelled' state can be deleted.")



