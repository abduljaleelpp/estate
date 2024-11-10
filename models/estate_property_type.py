
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyType(models.Model):
      _name = 'estate.property.type'
      _description = 'estate.property.type'
      _order = "name"

      name = fields.Char(required =True)
      property_ids = fields.One2many("estate.property",'property_type_id', string="Properties")
      offer_ids = fields.One2many("estate.property.offer", 'property_type_id', string ="Offers")
      offer_count = fields.Integer(compute="_compute_offer_count",store = True)
      
      _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'The property type name must be unique!')]

      @api.depends('offer_ids')
      def _compute_offer_count(self):
        for property in self:
          property.offer_count = len(property.offer_ids)


          