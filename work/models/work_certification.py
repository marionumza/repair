# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class WorkCertification(models.Model):
    _name = 'work.work_certification'
    _description = 'Certification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _check_company_auto = True #necesario para analytic_account_id?
    
    name = fields.Char( string='Name', required=True)
    # Necesario para fields.Monetary tener un currency_id que este asociado a la compañia
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related="company_id.currency_id", string="Currency", readonly=True)
    amount = fields.Monetary(string='Amount', default = 0.00 , help='Accumulated amount since the start')
    state = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted')
        ], 
        string='Status', required=True,
        default='pending')
    date_send = fields.Date(string='Send date', help="Date the certification is sent")
    date_accepted = fields.Date(string='Accepted date')
    is_estimated = fields.Boolean(string="Estimated", default = False, help = "The certification has been estimated from administration")
    is_liquidation = fields.Boolean(string="Liquidation", default = False, help = "The certification is the liquidation one")
    attached_file = fields.Binary(string='Attached File Doc')
    attached_file_name = fields.Char('Attached File')
    
    # Many2one
    project_id = fields.Many2one('project.project', string='Project', required=True)
    related_project_id_analytic_account_id = fields.Many2one(string = 'Analytic Account', related='project_id.analytic_account_id', store = False, readonly=False,
                                                             help="Analytic account to which this project is linked for financial management. "
                                                                "Always the same for every certification in the project.")
    architect_id = fields.Many2one('res.partner', string='Architect', ondelete='set null', domain="[('category_id.id', '=', ('4'))]") #id tag arquitect
    
    
    @api.model
    def create(self, values):
        project_id = self.env['project.project'].search([('id', '=', values.get('project_id'))])
        if not project_id.date_start:
            raise UserError('El proyecto debe tener establecida la fecha de inicio')
        if values.get('state') == 'accepted' and not values.get('date_accepted'):
            raise UserError("Debe introducir fecha aceptacion en la certificacion "+values.get('name'))
        # Obtenemos la ultima certificacion creada si la hubiera para obtener su importe
        last_certification = self.env['work.work_certification'].search([('project_id', '=', project_id.id)], order='create_date desc', limit=1)
        work_certification = super().create(values)
        # Creacion de account.analytic.line
        amount = 0.00
        if last_certification:
            amount = last_certification.amount
        amount = work_certification.amount - amount
        line_vals = {
            'name': "Certificacion",
            'date': work_certification.create_date,
            'amount': amount,
            'account_id': work_certification.related_project_id_analytic_account_id.id,
            'user_id': work_certification.create_uid.id,
            'company_id': work_certification.company_id.id,
            'create_uid': work_certification.create_uid.id,
        }
        analytic_line = self.env['account.analytic.line'].create(line_vals)
        return work_certification 
    
    def write(self, vals):
        if vals.get('state') == 'accepted' and (not self.date_accepted and not vals.get('date_accepted')):
            raise UserError("Debe introducir fecha aceptacion en la certificacion "+self.name)
        return super(WorkCertification, self).write(vals)
    