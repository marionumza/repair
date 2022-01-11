# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    prescriber_farm_administrator = fields.Many2one(comodel_name='res.partner', string="Prescriptor: ",
                                                 domain="[('category_id', '=', 'Administrador de fincas')]")
