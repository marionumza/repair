# -*- coding: utf-8 -*-
{
    'name': 'Repair',
    'summary': 'Gestión Integral de Obras',
    
    'author': "SCA Asesores, S.A.",
    'website': "http://www.gruposca.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'SCA',
    'version': '0.93.1',
    # sudo en mails
    # plantillas mail v0.3;
    # mostrar opportunity_id en presupuesto
    
    # any module necessary for this one to work correctly
    'depends': ['base','mail', 'project', 'account_move_tier_validation', 'sale_subscription'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/work_certification_views.xml',
        'views/work_certification_menuitems.xml',
        'views/work_outsource_views.xml',
        'views/project_extended_views.xml',
        'views/res_partner_extended_views.xml',
        'views/res_partner_menuitems.xml',
        'views/historical_views.xml',
        'views/mail_templates.xml',
        'views/account_move_extended_views.xml',
        'views/work_waste_views.xml',
        'views/work_material_views.xml',
        'views/crm_lead_extended_views.xml',
        'views/sale_order_extended_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
