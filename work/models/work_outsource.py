from odoo import api, fields, models

class WorkOutsource(models.Model):
    _name = 'work.work_outsource'
    _description = 'Work Outsource'
    _rec_name = 'outsource_id'
    _order = 'date_get_in'
    
    project_id = fields.Many2one('project.project', string='Project')
    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required=True, domain="['|',('category_id.id', '=', ('6')),('category_id.id', '=', ('8'))]") #id tag subcontrata con y sin
    adhesion_certificate = fields.Binary(string="Adhesion Certificate Doc")
    adhesion_certificate_file_name = fields.Char('Adhesion Certificate File')
    date_get_in = fields.Date(string='Get in date', help="Date the outsource get in the work")
    date_end = fields.Date(string='End date', help="Date the outsource ends the work")
    contract_required = fields.Boolean(string='Contract Required', required = True)
    contract = fields.Binary(string="Contract Doc")
    contract_file_name = fields.Char('Contract File')
    
    
class WorkOutsourceWorkers(models.Model):
    _name = 'work.work_outsource_workers'
    _description = 'Work Outsource Workers'
    _rec_name = 'name'
    
    name = fields.Char(string='Name')
    prl_formation = fields.Binary(string="PRL Formation Doc")
    prl_formation_file_name = fields.Char('PRL Formation File')
    prl_formation_check = fields.Boolean(string='PRL Formation', default=False)
    epi_handing_over = fields.Binary(string="EPI Handing Over Doc")
    epi_handing_over_file_name = fields.Char('EPI Handing Over File')
    date_epi_handing_over = fields.Date(string='EPI Expiration date')
    medical_examination = fields.Binary(string="Medical Examination Doc")
    medical_examination_file_name = fields.Char('Medical Examination File')
    date_medical_examination = fields.Date(string='Medical Examination Expiration date')
    job_risks = fields.Binary(string="Job Risks Doc")
    job_risks_file_name = fields.Char('Job Risks File')
    job_risks_check = fields.Boolean(string='Job Risks', default=False)
    machinery_use = fields.Binary(string="Machinery Use Information Doc")
    machinery_use_file_name = fields.Char('Machinery Use Information File')
    machinery_use_check = fields.Boolean(string='Machinery Use Information', default=False)
    
    outsource_id = fields.Many2one('res.partner', string='Outsource Company', domain="[('category_id.id', '=', ('6'))]") #id tag subcontrata con