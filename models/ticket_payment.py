from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ticket_payment(models.Model):
    _name = 'ticket.payment'

    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    company_currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id  # Mengambil mata uang perusahaan secara default
    )
    payment_code = fields.Char(string='Payment Order', required=True,
                               default=lambda self: self.env['ir.sequence'].next_by_code('ticket.payment'))
    tax = fields.Float(string='Tax', default=15.0)
    payment_date = fields.Date(string='Payment Date', required=True)
    form_submission_id = fields.Many2one('form.submission', string='Form Submission')
    quantity = fields.Float(string='quantity', required=True)
    price = fields.Float(string='Price', compute='_compute_price')
    customer = fields.Char(
        string="Customer",
        compute='_compute_form_submission',
        store=False
    )
    payment_status = fields.Selection([
        ('draft', 'Draft'),
        ('unpaid', 'Unpaid'),
        ('paid', 'paid')
    ], required=True, string='Payment Status', default='draft')

    category = fields.Selection([
        ('premium', 'Premium'),
        ('regular', 'Regular')
    ], required=True, string='Category')

    duration = fields.Selection([
        ('one_day', 'One Day Pass'),
        ('two_day', 'Two Day Pass'),
        ('three_day', 'Three Day Pass')
    ], required=True, string='Duration')

    @api.depends('form_submission_id')
    def _compute_form_submission(self):
        for record in self:
            record.customer = record.form_submission_id.name if record.form_submission_id else ''

    @api.depends('category', 'duration')
    def _compute_price(self):
        price_map = {
            'premium': {
                'one_day': 50,
                'two_day': 90,
                'three_day': 120,
            },
            'regular': {
                'one_day': 30,
                'two_day': 55,
                'three_day': 75,
            }
        }
        for record in self:
            record.price = price_map.get(record.category, {}).get(record.duration, 0)

    @api.depends('price', 'quantity', 'tax')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = (record.price * record.quantity)
            return

    @api.depends('subtotal', 'tax')
    def _compute_total(self):
        # self.total = 30
        for record in self:
            record.total = record.subtotal * (1 + record.tax / 100.0)
            # record.total = 30
            return

    def func_set_to_paid(self):
        self.payment_status = "paid"
        return 0

    def get_email_confirmation_url(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/send_email_accepted/%s' % (self.id),
            'target': 'new',
        }
