# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

class Project(models.Model):
    _inherit = "project.project"
    
    state = fields.Selection([
            ('0_contract', 'Signed Contract'),
            ('1_in_progress', 'In Progress'),
            ('2_finished', 'Finished'),
            ('3_closed', 'Closed'),
        ],
        string='Work Status', required=True,
        default='0_contract',
    )
    project_code = fields.Char(string='Work Code', help='Unique work code')
    payment_method = fields.Selection(
        selection=[
            ('certifications', 'Certifications'),
            ('agreed', 'Agreed Payment')
        ], 
        string='Payment Method', required=True, default='certifications')
    date_start = fields.Date(string='Start date', help="Date the work starts")
    date_end = fields.Date(string='End date', help="Date the work ends, linked with the aproval of the liquidation certification")
    is_licensed = fields.Boolean(string='Licenses', default=False, help='Work has the required licenses') # groups= isusko 9
    is_work_center_open = fields.Boolean(string='Work center opening', default=False, help ='Management of documentation related to the opening of a work center') # groups= isusko 9
    #budget = fields.Monetary(string='Budget', related="lead_id.planned_revenue / lead_id.expected_revenue")
    penalties = fields.Boolean(string='Penalties', default=False, help='Penalties for the late delivery of the work') #groups= jefe de obra
    penalties_amount = fields.Float(string='Penalties Amount', digits=(9,2), help='Penalty amount per day late') # control gari 8
    penalties_date_start = fields.Date(string='Penalties Start date', help="Date the penalization starts")
    notes = fields.Text(string='Notes')
    
    # Many2one
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity Code', ondelete='set null')
    work_manager_id = fields.Many2one('res.users', string='Work Manager', ondelete='cascade', help='User responsible of the managing of the work', domain="[('category_id.id', '=', ('5'))]") # id tag jefe de obra
    architect_id = fields.Many2one('res.partner', string='Architect', ondelete='set null', domain="[('category_id.id', '=', ('4'))]") #id tag arquitecto
    prevention_coordinator_id = fields.Many2one('res.partner', string='Prevention Coordinator', ondelete='set null', domain="[('category_id.id', '=', ('7'))]") #id tag coordinacion prevencion
    #promoter_id = fields.Many2one('res.partner', string='Client', ondelete='set null', domain="[('category_id.id', '=', ('2'))]") #id tag comunidad propietarios
    prescriber_id = fields.Many2one('res.partner', string='Prescriber', ondelete='set null', domain="[('category_id.id', '=', ('1'))]") #id tag administrador de fincas
    
    # One2many
    work_certification_ids = fields.One2many('work.work_certification', inverse_name='project_id', string="Work Certifications")
    provider_ids = fields.One2many('work.work_material', string='Providers', inverse_name='project_id')
    
    
    #######################
    # Gestion de residuos #
    #######################
    # Si los campos sa y dsc no estan como aceptados al finalizar la obra, aviso informativo
    sa = fields.Selection(
        selection=[
            ('not sent', 'Not Sent'),
            ('sent', 'Sent'),
            ('accepted','Accepted')
        ], 
        string='SA', required=True, default='not sent')
    dsc = fields.Selection(
        selection=[
            ('not sent', 'Not Sent'),
            ('sent', 'Sent'),
            ('accepted','Accepted')
        ], 
        string='DSC', required=True, default='not sent')
    management_type = fields.Selection(
        selection=[
            ('container', 'Container'),
            ('pavilion', 'Managed in pavilion')
        ], 
        string='Management Type', required=True, default='container')
    date_disposal = fields.Date(string='Disposal Date', help="Date the wastes are disposed from the pavilion")
    work_wastes_ids_sa = fields.One2many('work.waste_management', inverse_name='project_id_sa', string="SA Wastes")
    work_wastes_ids_dsc = fields.One2many('work.waste_management', inverse_name='project_id_dsc', string="DSC Wastes")
    
    ###############
    # Subcontrata #
    ###############
    work_outsources_ids = fields.One2many('work.work_outsource', inverse_name='project_id', string="Outsourcing Companyes")
    
    @api.model
    def create(self, values):
        project = super().create(values)
        #self._generate_unique_project_code(project.id, project.company_id.id)
        project.project_code = self._generate_unique_project_code(project)
        project.name = project.project_code
        project.analytic_account_id.name = project.project_code
        # Si viene desde Oportunidad
        if project.sale_order_id and project.sale_order_id.opportunity_id:
            project.name += ' - ' + project.sale_order_id.opportunity_id.name
            project.opportunity_id = project.sale_order_id.opportunity_id
            if project.sale_order_id.opportunity_id.prescriber_farm_administrator:
                project.prescriber_id = project.sale_order_id.opportunity_id.prescriber_farm_administrator.id
        elif values.get('name'):
            project.name += ' - ' + values.get('name')
        return project
    
    # Generar Tarea y Actividad al crear el primer work_wastes_ids_sa
    def write(self, vals):
        if vals.get('work_wastes_ids_sa') and not len(self.work_wastes_ids_sa) > 0:
            task = self._create_waste_task()
            self._create_waste_activity(task)
        return super(Project, self).write(vals)
    
    def _create_waste_task(self):
        task_vals = {
            'name': 'Comunicar Gestión de Residuos',
            'stage_id': self.env['project.task.type'].search([('id', '=', 19)]).id, #Tareas Administrativas
            'project_id': self.id,
            'user_id': self.env['res.users'].search([('id', '=', 9)]).id #Edurne
        }
        task = self.env['project.task'].create(task_vals)
        return task
    
    def _create_waste_activity(self, task):
        activity_vals = {
            'res_id': task.id,
            'res_model_id': self.env['ir.model'].search([('model', '=', 'project.task')]).id,
            'res_model': 'project.task',
            'activity_type_id': 4,
            'summary': 'Comunicar Gestión de Residuos',
            'date_deadline': date.today(),
            'user_id': self.env['res.users'].search([('id', '=', 9)]).id #Edurne
        }
        activity = self.env['mail.activity'].create(activity_vals)
        return activity
        
    # def _create_work_manager_activity(self, project_id, company_id):
    #     if company_id == 2: #Fachadas
    #         user_id = 12 #Jose Luis
    #     elif company_id == 3: #Estructuras
    #         user_id =  11 #Leire
            
    #     activity_vals = {
    #         'res_id': project_id,
    #         'res_model_id': 233,
    #         'res_model': 'project.project',
    #         'activity_type_id': 4,
    #         'summary': 'Asignar jefe de obra',
    #         'note': 'Nueva obra creada, por favor asigne jefe de obra',
    #         'date_deadline': datetime.datetime.now(),
    #         'user_id': user_id
    #     }
    #     activity = self.env['mail.activity'].create(activity_vals)
    #     return True    
    
    def _generate_unique_project_code(self, project):
        if project.company_id.id == 1: #Fachadas
            seq = self.env['ir.sequence'].search([('id', '=', 82)])
        elif project.company_id.id == 2: #Estructuras
            seq = self.env['ir.sequence'].search([('id', '=', 99)])
        project_code = seq.next_by_id()
        return project_code
    
    @api.onchange('state')
    def _on_change_state(self):
        # ('0_contract', 'Signed Contract'), default
        # ('1_in_progress', 'In Progress'),
        # ('2_finished', 'Finished'),
        # ('3_closed', 'Closed'),           
        
        if (self.state == '1_in_progress'):
            self.state_in_progress()
        elif (self.state == '2_finished'):
            self.state_finished()
            if self.sa != 'accepted' or self.dsc != 'accepted':
                return {
                    'warning': {
                        'title': _('Gestion de Residuos'),
                        'message': _("Revise los campos SA y DSC de la gestion de residuos, "
                                    "alguno de ellos no ha sido aceptado.")
                    }
                }
        elif (self.state == '3_closed'):       
            self.state_closed()
            
    def state_in_progress(self):
        if self.is_licensed:
            if self.is_work_center_open:
                self.state = '1_in_progress'
            else:
                raise UserError("Revise la apertura del centro de trabajo.")
        else:
            raise UserError("Revise las licencias de la obra.")
        
    def state_finished (self):
        if self.date_end:
            # Desarchivar analytic account y sus lines
            if not self.analytic_account_id.active:
                self.analytic_account_id.active = True
                analytic_account_lines = self.env['account.analytic.line'].with_context(active_test=False).search([('account_id', '=', self.analytic_account_id.id)])
                for line in analytic_account_lines:
                    line.active = True
            self.state = "2_finished"
        else:
            raise UserError("Debe introducir fecha fin de obra.")
        
    def state_closed (self):
        self.analytic_account_id.active = False
        analytic_account_lines = self.env['account.analytic.line'].search([('account_id', '=', self.analytic_account_id.id)])
        for line in analytic_account_lines:
                line.active = False
        self.state = "3_closed"
        
    # Accion planificada cerrar obras finalizadas >= 1 año
    def autoclose_finished_works(self):
        projects_finished = self.env['project.project'].search([('state', '=', '2_finished')])
        for project in projects_finished:
            if project.date_end + relativedelta(years=1) <= date.today():
                project.state_closed()