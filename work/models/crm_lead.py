from odoo import api, fields, models
from datetime import datetime, date, timedelta

class Lead(models.Model):
    _inherit = "crm.lead"
    
    date_request = fields.Date('Request Date')
    date_budget = fields.Date('Budget Date')
    opportunity_code = fields.Char(string='Opportunity Code', help='Unique oportunity code')
    
    def name_get(self):
        result = []
        for record in self:
            if record.opportunity_code:
                result.append((record.id, record.opportunity_code))
            else:
                result.append((record.id, record.name))
        return result