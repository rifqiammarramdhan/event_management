from odoo import models, fields

class form_submission(models.Model):
    _name = 'form.submission'
    _description = 'Form Submission'

    name = fields.Char(string="Name")
    phone = fields.Char(string="Phone")
    # email = fields.Char(string="Your Email", required=True)
    # company = fields.Char(string="Your Company")
    # subject = fields.Char(string="Subject", required=True)
    # question = fields.Text(string="Your Question", required=True)
