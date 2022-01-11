from odoo import api, fields, models

class SaleSubscription(models.Model):
    _description = "Subscription Extension"
    _inherit = ['sale.subscription']
    
    # Extension del metodo de sale.subscription para añadir el project_id en los values con los que se creara despues la factura
    def _prepare_invoice_data(self):
        res = super(SaleSubscription, self)._prepare_invoice_data()
        sale_order = self.env['sale.order'].search([('order_line.subscription_id', 'in', self.ids)], order="id desc", limit=1)
        project = sale_order.order_line[0].project_id
        res["project_id"] = project.id
        res.pop("narration")
        return res
    
    # Extension del metodo de sale.subscription para borrar la cuenta analitica de las lineas de la factura
    def _recurring_create_invoice(self, automatic=False):
        invoices = super(SaleSubscription, self)._recurring_create_invoice(automatic)
        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                 line.analytic_account_id = self.env['account.analytic.account']
        return invoices