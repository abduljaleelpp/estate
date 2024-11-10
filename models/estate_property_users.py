from odoo import models,fields,api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class EstatePropertyUsers(models.Model):
    _inherit = 'res.users'


    property_ids = fields.One2many('estate.property','sales_person_id',string="Properties", domain="[('state', 'not in', ['cancelled', 'sold'])]")


