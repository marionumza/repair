# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    labels_selection = [
        ('comunityy', 'Comunidad de vecinos'),
        ('farm_administrator_select', 'Administrador de fincas'),
        ('particular', 'particular'),
    ]

    contact_farm_administrator = fields.Many2one(comodel_name='res.partner', string="Administrador de fincas:",
                                                 domain="[('category_id', '=', 'Administrador de fincas')]")

    contact_comunity = fields.One2many('res.partner', 'contact_farm_administrator',
                                       domain="[('category_id', '=', 'Comunidad de vecinos')]")

    class FarmAdministratorModel(models.Model):
        _name = 'farm.administrator.model'
