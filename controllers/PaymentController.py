from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class PaymentController(http.Controller):
    @http.route('/payment-confirmation', auth='user',methods=['GET', 'POST'], website=True)
    def payconf(self, **kwargs):
        payment_records = {}
        form_submission_record = {}
        if request.httprequest.method == 'POST':
            # Logic

            # Delete Session
            del request.session['session_form_submission_id']

            # Redirect
            return request.redirect('/')
        try:
            # Get Session And Validating
            session_fs_id = request.session.get('session_form_submission_id')
            if not session_fs_id:
                return request.redirect('/regpay')

            payment_records = request.env['ticket.payment'].search([('form_submission_id', '=', session_fs_id)])
            form_submission_record = request.env['form.submission'].browse(session_fs_id)
            # payment_record = request.env['event.management.payment'].browse(session_form_submission_id)



        except Exception as e:
            _logger.info(f"ERROR: -------><------- {(e)}")

        finally:
            return request.render('event_management.attendance_registration_payment_id',{
                "paymentrecord" : payment_records,
                "form_submission_record" : form_submission_record
            })

