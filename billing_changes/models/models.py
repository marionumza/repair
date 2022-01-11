# -*- coding: utf-8 -*-
import http.client
from odoo import models, fields, api
import requests
import math
import json
from datetime import date, datetime


class AccountMove(models.Model):
    _inherit = 'account.move'
    billing_employed = fields.Many2one(comodel_name='hr.employee', string="Realiza la facturación:",
                                       domain="[('company_id', '=', company_id)]")

    data_number = fields.Text(
        compute="numberString")

    expiration_day = fields.Integer(compute="fechDateFormat")
    expiration_month = fields.Integer(compute="fechDateFormat")
    expiration_year = fields.Integer(compute="fechDateFormat")
    expiration_month_finish = fields.Char(compute="fechDateFormat")




    date_issue_day = fields.Integer(compute="fechDateFormat")
    date_issue_month = fields.Integer(compute="fechDateFormat")
    date_issue_year = fields.Integer(compute="fechDateFormat")
    date_issue_month_finish = fields.Char(compute="fechDateFormat")


    def fechDateFormat(self):


        if self.expiration_month == 1:
            self.expiration_month_finish = 'enero'
        if self.expiration_month == 2:
            self.expiration_month_finish = 'febrero'
        if self.expiration_month == 3:
            self.expiration_month_finish = 'marzo'
        if self.expiration_month == 4:
            self.expiration_month_finish = 'abril'
        if self.expiration_month == 5:
            self.expiration_month_finish = 'mayo'
        if self.expiration_month == 6:
            self.expiration_month_finish = 'junio'
        if self.expiration_month == 7:
            self.expiration_month_finish = 'julio'
        if self.expiration_month == 8:
            self.expiration_month_finish = 'agosto'
        if self.expiration_month == 9:
            self.expiration_month_finish = 'septiembre'
        if self.expiration_month == 10:
            self.expiration_month_finish = 'octubre'
        if self.expiration_month == 11:
            self.expiration_month_finish = 'noviembre'
        if self.expiration_month == 12:
            self.expiration_month_finish = 'diciembre'


        self.expiration_day = self.invoice_date_due.day
        self.expiration_month = self.invoice_date_due.month
        self.expiration_year = self.invoice_date_due.year

        self.date_issue_day = self.invoice_date.day
        self.date_issue_month = self.invoice_date.month
        self.date_issue_year = self.invoice_date.year

        if self.date_issue_month == 1:
            self.date_issue_month_finish = 'enero'
        if self.date_issue_month == 2:
            self.date_issue_month_finish = 'febrero'
        if self.date_issue_month == 3:
            self.date_issue_month_finish = 'marzo'
        if self.date_issue_month == 4:
            self.date_issue_month_finish = 'abril'
        if self.date_issue_month == 5:
            self.date_issue_month_finish = 'mayo'
        if self.date_issue_month == 6:
            self.date_issue_month_finish = 'junio'
        if self.date_issue_month == 7:
            self.date_issue_month_finish = 'julio'
        if self.date_issue_month == 8:
            self.date_issue_month_finish = 'agosto'
        if self.date_issue_month == 9:
            self.date_issue_month_finish = 'septiembre'
        if self.date_issue_month == 10:
            self.date_issue_month_finish = 'octubre'
        if self.date_issue_month == 11:
            self.date_issue_month_finish = 'noviembre'
        if self.date_issue_month == 12:
            self.date_issue_month_finish = 'diciembre'


    def numberEntero(self):
        parte_decimal, parte_entera = math.modf(self.amount_total)

        return parte_entera

    def numberDecimal(self):
        parte_decimal, parte_entera = math.modf(self.amount_total)
        parte_decimal = parte_decimal * 100

        return parte_decimal

    def numberString(self):
        url = "https://numeros-a-letras1.p.rapidapi.com/api/NAL/"

        queryString = {"num": self.numberEntero()}
        queryStringDecimal = {"num": round(self.numberDecimal())}
        headers = {
            'x-rapidapi-key': "260402d356msh5a1fb857c57577ap1b66e5jsn933ff06fa7e2",
            'x-rapidapi-host': "numeros-a-letras1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=queryString)
        responseDecimal = requests.request("GET", url, headers=headers, params=queryStringDecimal)

        result = json.loads(response.text)
        resultDecimal = json.loads(responseDecimal.text)

        self.data_number = result['letras'] + ' CON ' + resultDecimal['letras']


class PaymentChanges(models.Model):
    _inherit = 'account.payment'

    invoice_date_duee = fields.Date(string='Fecha de vencimiento',
                                    attrs="{'readonly': [['state', 'not in', ['draft']]]}",
                                    related='invoice_ids.invoice_date_due')
