
from odoo import models, fields, api

class EstatePropertyType(models.Model):
      _name = 'estate.property.type'
      _description = 'estate.property.type'
       
      name = fields.Char(required =True)
      
