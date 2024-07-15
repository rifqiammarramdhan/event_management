from odoo import models, fields

class form_submission(models.Model):
    _name = 'form.submission'
    _description = 'Form Submission'

    name = fields.Char(string="Name",  required=True)
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email", required=True)
    visitingDate = fields.Char(string="Visiting Date")
    KTP_number = fields.Char(string="KTP Number", required=True)
    company_name = fields.Char(string="Company Name", required=True)
    visit_purpose = fields.Char(string="Visiting Purpose", required=True)
    intended_person = fields.Char(string="Intended Person", required=True)
    photo = fields.Binary("Photo", help="Select Photo here")
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('hold', 'Hold'),
        ('banned', 'Banned')
    ], default='pending', string='Status')
    # file_attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

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
            'url': '/send_email_accepted/%s' % (self.id),
            'target': 'new',
        }

    # # Create Insert data To Model Ticket_Payment from controller
    # def create_payment(self):
    #     self.env['ticket.payment'].create({
    #         'customer': self.name,
    #         'form_submission_id': self.id,
    #         # Tambahkan field lain sesuai kebutuhan
    #     })

