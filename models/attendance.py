from odoo import models, fields, api, _


class attendance_register(models.Model):
    _name = "attendance.register"
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    def func_set_to_accepted(self):
        if self.status != "accepted":
            self.status = 'accepted'


    def func_set_to_rejected(self):
        if self.status != "accepted":
           self.status = "rejected"

    def func_set_to_hold(self):
        if self.status != "accepted":
           self.status = "hold"

    def func_set_to_banned(self):
           self.status = "banned"

    def get_email_confirmation_url(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/send_payment_confirmation/%s' % (self.id),
            'target': 'new',
        }


    name = fields.Char(string="Name", require=True)
    attendance_register_id = fields.Many2one('attendance.register', string='Attendance Register ID')
    visit_date = fields.Date(string="Visit Date", require=True)
    visit_time = fields.Float(stirng="Visit Time", require=True)
    photo = fields.Binary("Photo", help="Select Photo here")
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('hold', 'Hold'),
        ('banned', 'Banned')
    ], default='pending', string='Status')

    address = fields.Char(string="Address", required=True)
    company = fields.Char(string="Company", required=True)
    phone = fields.Char(string="Phone", required=True)
    visit_purpose = fields.Char(string="Visit Purpose", required=True)
    email = fields.Char(string="email", required=True)
    expected_duration = fields.Char(string="Expected Duration", require=True)
    additional_info = fields.Char(string="Additional Info")
    id_card_num = fields.Char(string="Id Card Number", required=True)
    visit_note = fields.Char(string="Visit Note")
    employee_type = fields.Selection([
        ('employee', 'Employee'),
        ('guest', 'Guest'),
    ], string="Employee Type", require=True)
    qrcode = fields.Binary(string="QR Code")


