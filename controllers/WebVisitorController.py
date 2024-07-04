from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class CustomRegistrationController(http.Controller):

    @http.route(['/submit/form'], type='http', auth="public", website=True)
    def submit_form(self, **post):
        try:
            _logger.info(f"Form Submission: {post.get('name')}")
            request.env['form.submission'].sudo().create({
                'name': post.get('name'),
                'phone': post.get('phone'),
            })
            return request.redirect('/contactus-thank-you')
        except Exception as e:
            _logger.error(f"Error: {e}")


    @http.route('/registration', auth='public', website=True)
    def web_form(self, **kwargs):
        return request.render('event_management.contact_form_template')
