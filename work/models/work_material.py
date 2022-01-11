from odoo import api, fields, models

class WorkMaterial(models.Model):
    _name = 'work.work_material'
    _description = 'Material'
    _rec_name = 'partner_id'
    
    partner_id = fields.Many2one('res.partner', string="Provider", domain="[('category_id.id', '=', ('9'))]") #id tag proveedor 
    budget_accepted = fields.Binary(string='Accepted Budget')
    budget_accepted_file_name = fields.Char(string='Accepted Budget File')
    project_id = fields.Many2one('project.project', string='Project')