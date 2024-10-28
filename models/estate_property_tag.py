
from odoo import models,fields,api

class EstatePropertyTag(models.Model):
    _name ="estate.property.tag"
    _description ="estate property tag"
    _order = "name"

    name =fields.Char(required=True)
    color = fields.Integer(string ="Color Index")