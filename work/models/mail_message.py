from odoo import api, fields, models

class Message(models.Model):
    _inherit = 'mail.message'
    
    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            if 'mail_server_id' not in values and values.get('message_type') == 'user_notification':
                values['mail_server_id'] = int(self.env['ir.config_parameter'].sudo().get_param("mail.default.smtp.server", 1))
                values['email_from'] = self.env['ir.mail_server'].sudo().search([('id', '=', values.get('mail_server_id'))]).smtp_user
        return super(Message, self).create(values_list)
        
    
    