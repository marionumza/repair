from odoo import api, fields, models
from datetime import datetime, date, timedelta

class OutsourcePartner(models.Model):
    _inherit = 'res.partner'
    
    email_payments = fields.Char(string='Payments Email', help="If doesnt exists, administration email will be used")
    email_prevention = fields.Char(string='Prevention Email', help="If doesnt exists, administration email will be used")
    
    rea = fields.Binary(string='REA', help="Duration 3 years")
    rea_file_name = fields.Char(string='REA File', help="Duration 3 years")
    date_expiration_rea = fields.Date(string='Expiration Date REA')
    
    rc_insurance = fields.Binary(string='Civil Liability Insurance')
    rc_insurance_file_name = fields.Char(string='Civil Liability Insurance File')
    rc_insurance_payment = fields.Binary(string='Civil Liability Insurance Payment Receipt')
    rc_insurance_payment_file_name = fields.Char(string='Civil Liability Insurance Payment Receipt File')
    date_expiration_rc_insurance = fields.Date(string='Expiration Date Civil Liability')
    
    accident_insurance = fields.Binary(string='Accident Insurance')
    accident_insurance_file_name = fields.Char(string='Accident Insurance File')
    accident_insurance_payment = fields.Binary(string='Accident Insurance Payment Receipt')
    accident_insurance_payment_file_name = fields.Char(string='Accident Insurance Payment Receipt File')
    date_expiration_accident_insurance = fields.Date(string='Expiration Date Accident Insurance')
    
    prevention_service_certificate = fields.Binary(string='Prevention Service Certificate')
    prevention_service_certificate_file_name = fields.Char(string='Prevention Service Certificate File')
    date_expiration_prevention_service_certificate = fields.Date(string='Expiration Date Prevention Service')
    
    ss_certificate = fields.Binary(string='Social Security Certificate', help="Monthly certificate of being up to date with payments with Social Security")
    ss_certificate_file_name = fields.Char(string='Social Security Certificate File', help="Monthly certificate of being up to date with payments with Social Security")
    date_validity_ss_certificate = fields.Date(string='Validity Date Social Security')
    
    tax_authority_certificate = fields.Binary(string='Tax Authority Certificate', help="Annual certificate of being up to date with payments with Tax Authorities")
    tax_authority_certificate_file_name = fields.Char(string='Tax Authority Certificate File', help="Annual certificate of being up to date with payments with Tax Authorities")
    date_expiration_tax_authority_certificate = fields.Date(string='Expiration Date Tax Authority')
    
    ita = fields.Binary(string='ITA', help="Monthly Expiration")
    ita_file_name = fields.Char(string='ITA File', help="Monthly Expiration")
    date_validity_ita = fields.Date(string='Validity Date ITA')
    
    workers_receipt = fields.Binary(string='Workers Monthly Receipt', help="Monthly certificate of being up to date with payments with their workers")
    workers_receipt_file_name = fields.Char(string='Workers Monthly Receipt File', help="Monthly certificate of being up to date with payments with their workers")
    date_validity_workers_receipt = fields.Date(string='Validity Date Workers Monthly Receipt')
    
    rlc = fields.Binary(string='RLC', help="Monthly Expiration")
    rlc_file_name = fields.Char(string='RLC File', help="Monthly Expiration")
    rnt = fields.Binary(string='RNT', help="Monthly Expiration")
    rnt_file_name = fields.Char(string='RNT File', help="Monthly Expiration")
    rlc_rnt_receipt = fields.Binary(string='RLC and RNT Payment Receipt', help="Monthly Expiration")
    rlc_rnt_receipt_file_name = fields.Char(string='RLC and RNT Payment Receipt File', help="Monthly Expiration")
    date_validity_rlc_rnt = fields.Date(string='Validity Date RLC and RNT')
    
    # Campos extra Autonomos
    freelance_payment_receipt = fields.Binary(string='Freelance payment receipt', help="Monthly Expiration")
    freelance_payment_receipt_file_name = fields.Char(string='Freelance payment receipt File', help="Monthly Expiration")
    date_expiration_freelance_payment_receipt = fields.Date(string='Expiration Date Freelance payment receipt')
    prl_formation = fields.Boolean(string='PRL Formation', default=False)
    medical_examination = fields.Binary(string='Medical Examination')
    medical_examination_file_name = fields.Char(string='Medical Examination File')
    date_expiration_medical_examination = fields.Date(string='Expiration Date Medical Examination')
    
    # Empleados
    workers_ids = fields.One2many('work.work_outsource_workers', inverse_name='outsource_id', string="Workers")
    
    def write(self, vals):
        
        if vals.get('rea') and self.rea:
            rea_vals = {
            'rea': self.rea,
            'rea_file_name': self.rea_file_name,
            'date_expiration_rea': self.date_expiration_rea,
            'outsource_id': self.id,
            }
            self.env['work.hist_rea'].create(rea_vals)
            
        if (vals.get('rc_insurance') and self.rc_insurance) or (vals.get('rc_insurance_payment') and self.rc_insurance_payment):
            rc_vals = {
            'rc_insurance': self.rc_insurance,
            'rc_insurance_file_name': self.rc_insurance_file_name,
            'rc_insurance_payment': self.rc_insurance_payment,
            'rc_insurance_payment_file_name': self.rc_insurance_payment_file_name,
            'date_expiration_rc_insurance': self.date_expiration_rc_insurance,
            'outsource_id': self.id,
            }
            self.env['work.hist_rc_insurance'].create(rc_vals)
            
        if (vals.get('accident_insurance') and self.accident_insurance) or (vals.get('accident_insurance_payment') and self.accident_insurance_payment):
            accident_vals = {
            'accident_insurance': self.accident_insurance,
            'accident_insurance_file_name': self.accident_insurance_file_name,
            'accident_insurance_payment': self.accident_insurance_payment,
            'accident_insurance_payment_file_name': self.accident_insurance_payment_file_name,
            'date_expiration_accident_insurance': self.date_expiration_accident_insurance,
            'outsource_id': self.id,
            }
            self.env['work.hist_accident_insurance'].create(accident_vals)
            
        if vals.get('prevention_service_certificate') and self.prevention_service_certificate:
            prevention_vals = {
            'prevention_service_certificate': self.prevention_service_certificate,
            'prevention_service_certificate_file_name': self.prevention_service_certificate_file_name,
            'date_expiration_prevention_service_certificate': self.date_expiration_prevention_service_certificate,
            'outsource_id': self.id,
            }
            self.env['work.hist_prevention_service'].create(prevention_vals)
            
        if vals.get('ss_certificate') and self.ss_certificate:
            ss_vals = {
            'ss_certificate': self.ss_certificate,
            'ss_certificate_file_name': self.ss_certificate_file_name,
            'date_validity_ss_certificate': self.date_validity_ss_certificate,
            'outsource_id': self.id,
            }
            self.env['work.hist_ss_certificate'].create(ss_vals)
            
        if vals.get('tax_authority_certificate') and self.tax_authority_certificate:
            tax_vals = {
            'tax_authority_certificate': self.tax_authority_certificate,
            'tax_authority_certificate_file_name': self.tax_authority_certificate_file_name,
            'date_expiration_tax_authority_certificate': self.date_expiration_tax_authority_certificate,
            'outsource_id': self.id,
            }
            self.env['work.hist_tax_certificate'].create(tax_vals)
            
        if vals.get('ita') and self.ita:
            ita_vals = {
            'ita': self.ita,
            'ita_file_name': self.ita_file_name,
            'date_validity_ita': self.date_validity_ita,
            'outsource_id': self.id,
            }
            self.env['work.hist_ita'].create(ita_vals)
            
        if vals.get('workers_receipt') and self.workers_receipt:
            workers_vals = {
            'workers_receipt': self.workers_receipt,
            'workers_receipt_file_name': self.workers_receipt_file_name,
            'date_validity_workers_receipt': self.date_validity_workers_receipt,
            'outsource_id': self.id,
            }
            self.env['work.hist_workers_receipt'].create(workers_vals)
            
        if (vals.get('rlc') and self.rlc) or (vals.get('rnt') and self.rnt) or (vals.get('rlc_rnt_receipt') and self.rlc_rnt_receipt):
            rlc_vals = {
            'rlc': self.rlc,
            'rlc_file_name': self.rlc_file_name,
            'rnt': self.rnt,
            'rnt_file_name': self.rnt_file_name,
            'rlc_rnt_receipt': self.rlc_rnt_receipt,
            'rlc_rnt_receipt_file_name': self.rlc_rnt_receipt_file_name,
            'date_validity_rlc_rnt': self.date_validity_rlc_rnt,
            'outsource_id': self.id,
            }
            self.env['work.hist_rlc_rnt'].create(rlc_vals)
            
        if vals.get('freelance_payment_receipt') and self.freelance_payment_receipt:
            freelance_vals = {
            'freelance_payment_receipt': self.freelance_payment_receipt,
            'freelance_payment_receipt_file_name': self.freelance_payment_receipt_file_name,
            'date_expiration_freelance_payment_receipt': self.date_expiration_freelance_payment_receipt,
            'outsource_id': self.id,
            }
            self.env['work.hist_freelance_receipt'].create(freelance_vals)
        
        partner = super(OutsourcePartner, self).write(vals)
        return partner
    
    # Control de prevencion: Diaria (documentos con fecha caducidad)
    def _prevention_control_daily(self):
        # Obtenemos las subcontratas que esten en una obra en curso
        outsources = self._get_target_outsources()
        for outsource in outsources:
            worker_errors = dict()
            outsource_errors = self.check_outsource_daily(outsource)
            for worker in outsource.workers_ids:
                # Por cada trabajador, comprobamos sus campos
                errors = self.check_workers_daily(worker)
                # Si hay error en el trabajador, añadimos el trabajador con sus errores
                if errors:
                    list_errors = list(errors.values())
                    worker_temp_errors = {worker.name: list_errors}
                    worker_errors.update(worker_temp_errors)
            # Si la subcontrata o alguno de sus trabajadores tienen errores enviamos mail con todos ellos y lo que les falta
            if outsource_errors or worker_errors:
                email_template = self.env.ref('work.mail_template_prevention_daily_documentation_error')
                outsource_list = list(outsource_errors.values())
                worker_list = list(worker_errors.items())
                email_template.with_context(outsource_errors=outsource_list, worker_errors=worker_list).send_mail(outsource.id, force_send=True)
                # Actividad para isusko
                self._create_prevention_control_activity(outsource.id)
        
    def _get_target_outsources(self):
        works = self.env['project.project'].search([('state', '=', '1_in_progress'), ('work_outsources_ids', '!=', False)])
        outsource_ids = self.env['res.partner']
        for work in works:
            for candidate_outsource in work.work_outsources_ids:
                if candidate_outsource.outsource_id not in outsource_ids:
                    outsource_ids |= candidate_outsource.outsource_id
        return outsource_ids
    
    def check_outsource_daily(self, outsource):
        errors = dict()
        deadline = date.today() + timedelta(days=14)
        if deadline == outsource.date_expiration_rc_insurance:
            errors["rc"] = 'Seguro RC y Recibo de pago'
        if outsource.category_id.id == 6:
            if deadline == outsource.date_expiration_rea:
                errors["rea"] = 'REA'
            if deadline == outsource.date_validity_ita:
                errors["ita"] = 'ITA mensual'
            if deadline == outsource.date_expiration_accident_insurance:
                errors["accident"] = 'Seguro de Accidentes y Recibo de pago'
            if deadline == outsource.date_expiration_prevention_service_certificate:
                errors["prevention"] = 'Certificado del Servicio de Prevencion'
        elif outsource.category_id.id == 8:
            if deadline == outsource.date_expiration_freelance_payment_receipt:
                errors["freelance"] = 'Recibo de pago de autonomos'
            if deadline == outsource.date_expiration_medical_examination:
                errors["medical"] = 'Reconocimiento Medico'
        return errors
    
    def check_workers_daily(self, worker):
        errors = dict()
        deadline = date.today() + timedelta(days=14)
        if deadline == worker.date_epi_handing_over:
            errors["epi"] = 'Documento entrega de EPIs'
        if deadline == worker.date_medical_examination:
            errors["medical"] = 'Reconocimiento Medico'
        return errors
    
    
    def _create_prevention_control_activity(self, outsource_id):
        activity_vals = {
            'res_id': outsource_id,
            'res_model_id': self.env['ir.model'].search([('model', '=', 'res.partner')]).id,
            'res_model': 'res.partner',
            'activity_type_id': 4,
            'summary': 'Caducidad Documentacion Subcontrata',
            'note': 'Algun documento de prevencion de la subcontrata caduca proximamente',
            'date_deadline': date.today() + timedelta(days=14),
            'user_id': 9 #id isusko
        }
        activity = self.env['mail.activity'].create(activity_vals)
        return True
        
    # Control de prevencion: Semanal (campos sin fecha caducidad)
    def _prevention_control_weekly(self):
        # Obtenemos las subcontratas que esten en una obra en curso
        outsources = self._get_target_outsources()
        for outsource in outsources:
            # Por cada subcontrata, obtenemos sus trabajadores
            workers = outsource.workers_ids
            outsource_errors = dict()
            freelance_errors = dict()
            if outsource.category_id.id == 8:
                freelance_errors = self.check_freelance_weekly(outsource)
            for worker in workers:
                # Por cada trabajador, comprobamos sus campos
                errors = self.check_workers_weekly(worker)
                # Si hay error en el trabajador, añadimos el trabajador con sus errores
                if errors:
                    list_errors = list(errors.values())
                    worker_errors = {worker.name: list_errors}
                    outsource_errors.update(worker_errors)
            # Si la subcontrata tiene algun trabajador con errores enviamos mail con todos ellos y lo que les falta
            if outsource_errors or freelance_errors:
                email_template = self.env.ref('work.mail_template_prevention_weekly_documentation_error')
                list_error = list(outsource_errors.items())
                freelance_list = list(freelance_errors.values())
                email_template.with_context(errors=list_error, freelance_errors=freelance_list).send_mail(outsource.id, force_send=True)
                    
        
    def check_freelance_weekly(self, outsource):
        errors = dict()
        if not outsource.prl_formation:
            errors["prl"] = 'Formacion PRL'
        if not outsource.date_expiration_medical_examination:
            errors["medical"] = 'Reconocimiento Medico'
        return errors
    
    def check_workers_weekly(self, worker):
        errors = dict()
        if not worker.date_epi_handing_over:
            errors["epi"] = 'Documento entrega de EPIs'
        if not worker.date_medical_examination:
            errors["medical"] = 'Reconocimiento Medico'
        if not worker.prl_formation_check:
            errors["prl"] = 'Formacion PRL'
        if not worker.job_risks_check:
            errors["risks"] = 'Informacion riesgos puesto trabajo'
        if not worker.machinery_use_check:
            errors["machinery"] = 'Autorizacion uso maquinaria'
        return errors
    
    
    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('show_vat') and record.vat:
                result.append((record.id, "{} - {}".format(record.name, record.vat)))
            else:
                result.append((record.id, record.name))
        return result