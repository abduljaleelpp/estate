
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyType(models.Model):
      _name = 'estate.property.type'
      _description = 'estate.property.type'
      _order = "name"

      name = fields.Char(required =True)
      property_type_ids = fields.One2many("estate.property",'property_type_id', string="Properties")
      
      
      
      
      _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'The property type name must be unique!')]