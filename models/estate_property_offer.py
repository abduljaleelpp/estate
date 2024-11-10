
from odoo import models,fields,api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate.property.offer'
    _order ='price desc'


    price =fields.Integer(required=True)
    status = fields.Selection(selection= [('accepted','Accepted'),('refused','Refused')],copy =False)
    partner_id = fields.Many2one("res.partner", string="Partner",required=True)
    property_id = fields.Many2one("estate.property", string="Property", required = True)
    validity = fields.Integer(string="Validity")
    date_deadline = fields.Date( compute="_compute_validity",inverse="_inverse_validity" , string="Deadline", default= fields.date.today() + timedelta(days=90),readonly=False)
    property_type_id = fields.Many2one('estate.property.type', related = "property_id.property_type_id", string="Property Type", store=True)
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

    def action_accepted(self):
        for record in self:
            # Check if the current offer is already refused
            # Set this offer to "accepted"
            record.write({'status': 'accepted'})
            record.property_id.state = 'offer_accepted'

            # Refuse all other offers for this property
            other_offers = record.property_id.offer_ids.filtered(lambda o: o.id != record.id)
            other_offers.write({'status': 'refused'})
            record.property_id.partner_id = record.partner_id
        
        return True

    def action_cancel(self):
        for record in self:
            if record.status:
                record.status = 'refused'
                return True
            else:
                raise UserError("accepted offers can't be set as refuced.")
                return False

                
    @api.model
    def create(self, vals):
        # Retrieve the property_id and price from vals
        property_id = vals.get('property_id')
        price = vals.get('price')

        if property_id and price:
            # Get the highest existing offer for this property
            existing_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', property_id)
            ], limit=1, order='price desc')

            # Raise an error if the new offer price is less than or equal to the highest existing offer price
            if existing_offer and price <= existing_offer.price:
                raise ValidationError("The offer price must be higher than the existing offers for this property.")

            # Convert property_id to a recordset
            property_record = self.env['estate.property'].browse(property_id)
            
            # Update property state to 'Offer Received' if it is in 'new' state
            if property_record.state == 'new':
                property_record.state = 'offer_received'

        # Proceed with the creation of the offer
        return super(EstatePropertyOffer, self).create(vals)

