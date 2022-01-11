from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
class AccountMove(models.Model):
    _inherit = 'account.move'
    _state_field = "validation_state"
    _state_from = ["pending"]
    _state_to = ["validated"]
    
    validation_state = fields.Selection(selection=[
            ('pending', 'Pending'),
            ('validated', 'Validated'),
            ('cancel', 'Cancelled')
        ], string='Validation State', required=True, readonly=True, copy=False, tracking=True,
        default='pending')
    
    computed_validation_state = fields.Selection(selection=[
            ('pending', 'Pending'),
            ('validated', 'Validated'),
            ('rejected',  'Rejected'),
            ('cancel', 'Cancelled')
        ], string='Validation Status', compute="_compute_validation_state",)
    
    
    payable = fields.Boolean(string='Payable', default = False)
    payment_check = fields.Boolean(string='Checked', default = False)
    project_id = fields.Many2one('project.project', string='Work', required= True, domain="[('state', '!=', '3_closed')]", help='Work associated with this invoice. Only for subcontratas')
    related_project_analytic = fields.Many2one(related='project_id.analytic_account_id', store=True, index=True, copy=True, readonly= False)
    validator_id = fields.Many2one('res.users', string="Validator")
    
    @api.depends("validated", "rejected", "state")
    def _compute_validation_state(self):
        for rec in self:
            if rec.validated:
                rec.computed_validation_state = 'validated'
            if rec.rejected:
                rec.computed_validation_state = 'rejected'
            if not rec.validated and not rec.rejected:
                rec.computed_validation_state = 'pending'
            if rec.state == 'cancel':
                rec.computed_validation_state = 'cancel'
                
    @api.model
    def create(self, values):
        account_move = super().create(values)
        if account_move.type == 'in_invoice' or account_move.type == 'in_refund':
            project_id = values.get('project_id')
            project = self.env['project.project'].search([('id', '=', project_id)])
            if project.work_manager_id:
                account_move.validator_id = project.work_manager_id.id
            else: 
                raise ValidationError(_("The work needs to have stablished a work manager"))
        return account_move
    
    def _payment_control(self):
        account_moves = self.env['account.move'].search([('validation_state', '=', 'validated')])
        # Filtramos las facturas VALIDADAS que vencen en <= 7 dias desde hoy
        account_moves_to_process = self._check_date(account_moves)
        # Filtramos las facturas que sean de subcontrata
        account_moves_to_process = self._check_outsource(account_moves_to_process)
        # Conseguimos los ids de las subcontratas sin repetir
        outsource_ids = self._get_outsources(account_moves_to_process)
        
        # Por cada subcontrata, hacemos la comprobacion con cada una de sus facturas
        for outsource in outsource_ids:
            invoices_to_process = account_moves_to_process.filtered(lambda r: r.partner_id.id == outsource.id)
            outsource_errors = dict()
            for invoice in invoices_to_process:
                errors, error_message = self._check_validity(outsource, invoice.invoice_date_due)
                if not errors:
                    # Si todo esta OK, marcar factura como pagable
                    invoice.payable = True
                    invoice.payment_check = True
                else:
                    # Si hay algun error, escribimos errores en nota de factura si no se ha hecho ya anteriormente
                    if not invoice.payment_check:
                        #invoice.narration += date.today().strftime("%d/%m/%Y") + ":\n"
                        for error in error_message:
                            if not invoice.narration:
                                invoice.narration = ''
                            invoice.narration += error +"\n"
                    outsource_errors = dict(outsource_errors, **errors)
                    invoice.payment_check = True
            # Si la subcontrata tiene alguna factura con errores enviamos mail con todos ellos
            if outsource_errors:
                email_template = self.env.ref('work.mail_template_payment_documentation_error')
                list_error = list(outsource_errors.values())
                email_template.with_context(errors=list_error).send_mail(outsource.id, force_send=True)
        
        
    
    def _check_date(self, account_moves):
        account_move_to_process = self.env['account.move']
        for account_move in account_moves:
            if account_move.invoice_date_due:
                if date.today() <= account_move.invoice_date_due <=  date.today() + timedelta(days=7):
                    account_move_to_process |= account_move
        return account_move_to_process
    
    def _check_outsource(self, account_moves):
        account_move_to_process = self.env['account.move']
        for account_move in account_moves:
            if account_move.partner_id:
                partner = account_move.partner_id
                for category in partner.category_id:
                    if category.id == 6 or category.id == 8:
                        account_move_to_process |= account_move
                        break
        return account_move_to_process
    
    
    def _get_outsources(self, account_moves):
        outsource_ids = self.env['res.partner']
        for account_move in account_moves:
            if account_move.partner_id not in outsource_ids:
                outsource_ids |= account_move.partner_id
        return outsource_ids
    
    
    def _check_validity(self, outsource, deadline):
        errors = dict()
        error_message = []

        if not outsource.date_validity_ss_certificate or self._is_not_on_time(outsource.date_validity_ss_certificate, deadline):
            errors["ss"] = 'Certificado de estar al corriente de pagos con la seguridad social.'
            error_message.append('-El Certificado de Pago con SS de la subcontrata no es valido')
        if not outsource.date_expiration_tax_authority_certificate or self._is_not_on_time(outsource.date_expiration_tax_authority_certificate, deadline):
            errors["tax"] = 'Certificado de Contratación de estar al corriente de pagos con la hacienda.'
            error_message.append('-El Certificado de Pago con Hacienda de la subcontrata no es valido')
        if outsource.category_id.id == 6:
            if not outsource.date_validity_workers_receipt or self._is_not_on_time(outsource.date_validity_workers_receipt, deadline):
                errors["workers"] = ' Recibo mensual firmado por parte de los trabajadores de la subcontrata, en la que se indique que los trabajadores están al corriente de sus sueldos y salarios, y que no tienen ninguna cantidad pendiente de que se les abone por parte de la subcontrata.'
                error_message.append('-El Recibo Mensual Trabajadores de la subcontrata no es valido')
            if not outsource.date_validity_ita or self._is_not_on_time(outsource.date_validity_ita, deadline):
                errors["ita"] = 'ITA mensual.'
                error_message.append('-El documento ITA de la subcontrata no es valido')
            if not outsource.date_validity_rlc_rnt or self._is_not_on_time(outsource.date_validity_rlc_rnt, deadline):
                errors["rlc"] = 'RLC y RNT del mes, así como el recibo bancario correspondiente.'
                error_message.append('-El documento RLC/RNT de la subcontrata no es valido')
            
        return errors, error_message
    
    
    def _is_not_on_time(self, expiration, deadline):
        return expiration < deadline
    
    # VALIDACION DE FACTURA
    # Extension de metodo de tier.validation para poder escribir campos en factura con proceso de validacion
    @api.model
    def _get_under_validation_exceptions(self):
        return ["message_follower_ids", "access_token", "payable", "payment_check", "narration", "state", "name"] 
    
    # Extension de la validacion positiva para que no pida comentario
    def validate_tier(self):
        self.ensure_one()
        sequences = self._get_sequences_to_approve(self.env.user)
        reviews = self.review_ids.filtered(lambda l: l.sequence in sequences)
        #if self.has_comment:
            #return self._add_comment("validate", reviews)
        self._validate_tier(reviews)
        self._update_counter()
        
    # Marcar a validated cuando se acepta la validacion
    def _compute_validated_rejected(self):
        for rec in self:
            rec.validated = self._calc_reviews_validated(rec.review_ids)
            if rec.validated:
                rec.validation_state = 'validated'
            rec.rejected = self._calc_reviews_rejected(rec.review_ids)
        
    # Marcar a pending cuando se cambia a borrador la factura
    def button_draft(self):
        super(AccountMove, self).button_draft()
        if self.validation_state == 'cancel':
            self.write({'validation_state': 'pending'})
        
    # Marcar a cancel cuando se cancela la factura
    def button_cancel(self):
        super(AccountMove, self).button_cancel()
        self.write({'validation_state': 'cancel'})
        
    
    # Extension de tier.validation para solicitar validacion al pulsar en publicar
    def write(self, vals):
        if (
            self.state == 'draft' and vals.get('state') == 'posted' 
            and self.project_id 
            and (self.type == 'in_invoice' or self.type == 'in_refund')
            and self.need_validation
        ):
            self.request_validation()
        return super(AccountMove, self).write(vals)
    
class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    active = fields.Boolean(default=True, help="If the active field is set to False, it will allow you to hide the line without removing it.")
    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    related_project_id = fields.Many2one(related='move_id.related_project_analytic', string ='Project Analytic Account', store=True, index=True, copy=True, readonly= False)