
from odoo import models,fields,api
from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate.property.offer'
    _order ='price desc'


    price =fields.Integer(required=True)
    status = fields.Selection(selection= [('acepted','Accepted'),('refused','Refused')],copy =False)
    partner_id = fields.Many2one("res.partner", string="Partner",required=True)
    property_id = fields.Many2one("estate.property", string="Property", required = True)
    validity = fields.Integer(string="Validity")
    date_deadline = fields.Date( compute="_compute_validity",inverse="_inverse_validity" , string="Deadline", default= fields.date.today() + timedelta(days=90),readonly=False)

    _sql_constraints = [('_check_offer_price','CHECK(price > 0)','Price must be grater than Zero')]

    @api.depends('validity','create_date')
    def _compute_validity(self):
        for record in self:
            create_date = record.create_date or fields.date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)


    def _inverse_validity(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 0


