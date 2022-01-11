from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        if result.opportunity_id:
            result.opportunity_id.opportunity_code = result.name
            result.name += ' - ' + result.opportunity_id.name
        return result