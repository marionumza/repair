# -*- coding: utf-8 -*-

import json
from odoo import fields, _, models
from odoo.addons.web.controllers.main import clean_action


class ProjectProject(models.Model):
    _inherit = 'project.project'

    name_abbreviation = fields.Char(string='Abreviación')

    def _qweb_prepare_qcontext(self, view_id, domain):
        values = super()._qweb_prepare_qcontext(view_id, domain)

        projects = self.search(domain)

        view_tree = 'analytic.view_account_analytic_line_tree'
        view_form = 'analytic.view_account_analytic_line_form'

        ts_tree = self.env.ref(view_tree)
        ts_form = self.env.ref(view_form)

        new_button = {
            'name': _('Coste y beneficios'),
            'icon': 'fa fa-usd',
            'action': _to_action_data(
                'account.analytic.line',
                domain=[('account_id', '=', projects.analytic_account_id.id)],
                views=[(ts_tree.id, 'list'), (ts_form.id, 'form')],
            )
        }
        values['stat_buttons'].append(new_button)
        return values


def _to_action_data(model=None, *, action=None, views=None, res_id=None, domain=None, context=None):
    # pass in either action or (model, views)
    if action:
        assert model is None and views is None
        act = clean_action(action.read()[0])
        model = act['res_model']
        views = act['views']
    descr = {
        'data-model': model,
        'data-views': json.dumps(views),
    }
    if context is not None:  # otherwise copy action's?
        descr['data-context'] = json.dumps(context)
    if res_id:
        descr['data-res-id'] = res_id
    elif domain:
        descr['data-domain'] = json.dumps(domain)
    return descr
