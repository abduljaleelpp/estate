
from odoo import models,fields,api

class EstatePropertyTag(models.Model):
    _name ="estate.property.tag"
    _description ="estate property tag"

    name =fields.Char(required=True)