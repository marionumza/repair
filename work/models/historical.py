# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HistoricalRea(models.Model):
    _name = 'work.hist_rea'
    _description = 'REA'
    _rec_name = 'rea_file_name'
    _order = 'date_expiration_rea desc'
    
    rea = fields.Binary(string='REA', help="Duration 3 years")
    rea_file_name = fields.Char(string='REA File', help="Duration 3 years")
    date_expiration_rea = fields.Date(string='Expiration Date REA')
    
    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="[('category_id.id', '=', ('6'))]") #id tag subcontrata con
    
    
class HistoricalRcInsurance(models.Model):
    _name = 'work.hist_rc_insurance'
    _description = 'RC Insurance'
    _rec_name = 'rc_insurance_file_name'
    _order = 'date_expiration_rc_insurance desc'
    
    rc_insurance = fields.Binary(string='Civil Liability Insurance')
    rc_insurance_file_name = fields.Char(string='Civil Liability Insurance File')
    rc_insurance_payment = fields.Binary(string='Civil Liability Insurance Payment Receipt')
    rc_insurance_payment_file_name = fields.Char(string='Civil Liability Insurance Payment Receipt File')
    date_expiration_rc_insurance = fields.Date(string='Expiration Date Civil Liability')
    
    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="['|',('category_id.id', '=', ('6')),('category_id.id', '=', ('8'))]") #id tag subcontrata con y sin
    
    
class HistoricalAccidentInsurance(models.Model):
    _name = 'work.hist_accident_insurance'
    _description = 'Accident Insurance'
    _rec_name = 'accident_insurance_file_name'
    _order = 'date_expiration_accident_insurance desc'
    
    accident_insurance = fields.Binary(string='Accident Insurance')
    accident_insurance_file_name = fields.Char(string='Accident Insurance File')
    accident_insurance_payment = fields.Binary(string='Accident Insurance Payment Receipt')
    accident_insurance_payment_file_name = fields.Char(string='Accident Insurance Payment Receipt File')
    date_expiration_accident_insurance = fields.Date(string='Expiration Date Accident Insurance')
    
    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="[('category_id.id', '=', ('6'))]") #id tag subcontrata con
    
    
class HistoricalPreventionService(models.Model):
    _name = 'work.hist_prevention_service'
    _description = 'Prevention Service'
    _rec_name = 'prevention_service_certificate_file_name'
    _order = 'date_expiration_prevention_service_certificate desc'
    
    prevention_service_certificate = fields.Binary(string='Prevention Service Certificate')
    prevention_service_certificate_file_name = fields.Char(string='Prevention Service Certificate File')
    date_expiration_prevention_service_certificate = fields.Date(string='Expiration Date Prevention Service')

    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="[('category_id.id', '=', ('6'))]") #id tag subcontrata con
    

class HistoricalSSCertificate(models.Model):
    _name = 'work.hist_ss_certificate'
    _description = 'SS Certificate'
    _rec_name = 'ss_certificate_file_name'
    _order = 'date_validity_ss_certificate desc'
    
    ss_certificate = fields.Binary(string='Social Security Certificate', help="Monthly certificate of being up to date with payments with Social Security")
    ss_certificate_file_name = fields.Char(string='Social Security Certificate File', help="Monthly certificate of being up to date with payments with Social Security")
    date_validity_ss_certificate = fields.Date(string='Validity Date Social Security')

    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="['|',('category_id.id', '=', ('6')),('category_id.id', '=', ('8'))]") #id tag subcontrata con y sin
    
    
class HistoricalTaxCertificate(models.Model):
    _name = 'work.hist_tax_certificate'
    _description = 'Tax Certificate'
    _rec_name = 'tax_authority_certificate_file_name'
    _order = 'date_expiration_tax_authority_certificate desc'
    
    tax_authority_certificate = fields.Binary(string='Tax Authority Certificate', help="Annual certificate of being up to date with payments with Tax Authorities")
    tax_authority_certificate_file_name = fields.Char(string='Tax Authority Certificate File', help="Annual certificate of being up to date with payments with Tax Authorities")
    date_expiration_tax_authority_certificate = fields.Date(string='Expiration Date Tax Authority')

    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="['|',('category_id.id', '=', ('6')),('category_id.id', '=', ('8'))]") #id tag subcontrata con y sin
    
    
class HistoricalITA(models.Model):
    _name = 'work.hist_ita'
    _description = 'ITA'
    _rec_name = 'ita_file_name'
    _order = 'date_validity_ita desc'
    
    ita = fields.Binary(string='ITA', help="Monthly Expiration")
    ita_file_name = fields.Char(string='ITA File', help="Monthly Expiration")
    date_validity_ita = fields.Date(string='Validity Date ITA')

    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="[('category_id.id', '=', ('6'))]") #id tag subcontrata con
    
    
class HistoricalWorkersReceipt(models.Model):
    _name = 'work.hist_workers_receipt'
    _description = 'Workers Receipt'
    _rec_name = 'workers_receipt_file_name'
    _order = 'date_validity_workers_receipt desc'
    
    workers_receipt = fields.Binary(string='Workers Monthly Receipt', help="Monthly certificate of being up to date with payments with their workers")
    workers_receipt_file_name = fields.Char(string='Workers Monthly Receipt File', help="Monthly certificate of being up to date with payments with their workers")
    date_validity_workers_receipt = fields.Date(string='Validity Date Workers Monthly Receipt')

    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="[('category_id.id', '=', ('6'))]") #id tag subcontrata con
    
    
class HistoricalRlcRnt(models.Model):
    _name = 'work.hist_rlc_rnt'
    _description = 'RLC and RNT'
    _rec_name = 'rlc_file_name'
    _order = 'date_validity_rlc_rnt desc'
    
    rlc = fields.Binary(string='RLC', help="Monthly Expiration")
    rlc_file_name = fields.Char(string='RLC File', help="Monthly Expiration")
    rnt = fields.Binary(string='RNT', help="Monthly Expiration")
    rnt_file_name = fields.Char(string='RNT File', help="Monthly Expiration")
    rlc_rnt_receipt = fields.Binary(string='RLC and RNT Payment Receipt', help="Monthly Expiration")
    rlc_rnt_receipt_file_name = fields.Char(string='RLC and RNT Payment Receipt File', help="Monthly Expiration")
    date_validity_rlc_rnt = fields.Date(string='Validity Date RLC and RNT')

    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="[('category_id.id', '=', ('6'))]") #id tag subcontrata con
    
    
class HistoricalFreelanceReceipt(models.Model):
    _name = 'work.hist_freelance_receipt'
    _description = 'Freelance Receipt'
    _rec_name = 'freelance_payment_receipt_file_name'
    _order = 'date_expiration_freelance_payment_receipt desc'
    
    freelance_payment_receipt = fields.Binary(string='Freelance payment receipt', help="Monthly Expiration")
    freelance_payment_receipt_file_name = fields.Char(string='Freelance payment receipt File', help="Monthly Expiration")
    date_expiration_freelance_payment_receipt = fields.Date(string='Expiration Date Freelance payment receipt')

    outsource_id = fields.Many2one('res.partner', string='Outsource Company', required = True, domain="[('category_id.id', '=', ('8'))]") #id tag subcontrata sin