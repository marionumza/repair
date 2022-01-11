from odoo import api, fields, models

class WorkWasteManagement(models.Model):
    _name = 'work.waste_management'
    _description = 'Waste Management'
    _rec_name = 'waste_id'
    
    waste_id = fields.Many2one('work.waste', string="Code")
    related_waste_id_description = fields.Char(string = 'Description', related='waste_id.description', store = False)
    date_waste = fields.Date(string="Date")
    weight = fields.Float(string="Kg", digits='Stock Weight')
    attachment = fields.Binary(string="Attachment Doc")
    attachment_file_name = fields.Char('Attachment')
    state = fields.Selection(
        selection=[
            ('not sent', 'Not Sent'),
            ('sent', 'Sent'),
            ('accepted','Accepted')
        ], 
        string='State', required=True, default='not sent')
    project_id_sa = fields.Many2one('project.project', string='Project SA')
    project_id_dsc = fields.Many2one('project.project', string='Project DSC')
    

class WorkWaste(models.Model):
    _name = 'work.waste'
    _description = 'Waste'
    _rec_name = 'code'
    _order = 'code desc, id desc'
    
    code = fields.Char(string='Code', required=True)
    description = fields.Char(string='Description', required=True)
    
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, rec.code + ' - ' + rec.description))
        return res