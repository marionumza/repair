# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    total_acount_client = fields.Monetary(string="Certificaciones anteriores", compute="get_total_later", store="true")
    future_total_acount_client = fields.Monetary(string="Certificacion total", compute="get_total_certification", store="true")


    @api.depends('total_acount_client','invoice_line_ids')
    def get_total_later(self):
        cuenta = None
        importe = 0.0
        for o in self.invoice_line_ids:
            cuenta = o.analytic_account_id.id
            break
        lineas = self.env['account.analytic.line'].search(['&',('account_id','=', cuenta),('partner_id','=',self.partner_id.id)])
        for linea in lineas:
            importe += linea.amount
        self.total_acount_client = importe
#
    @api.depends('total_acount_client','amount_untaxed')
    def get_total_certification(self):
        if self.future_total_acount_client == 0:
            self.future_total_acount_client = self.total_acount_client - self.amount_untaxed

    @api.onchange('invoice_line_ids')
    def onchange_account_line(self):
        for record in self.invoice_line_ids:
            if record.analytic_account_id:
                self.get_total_later()
                self.future_total_acount_client -= self.amount_untaxed





