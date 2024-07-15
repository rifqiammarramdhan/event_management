from odoo import http
from odoo.http import request
import logging
import base64

_logger = logging.getLogger(__name__)

class CustomRegistrationController(http.Controller):

    @http.route(['/submit/form'], type='http', auth="public", website=True)
    def submit_form(self, **post):
        try:

            file = request.httprequest.files.get('photo')
            if file:
                photo_base64 = base64.b64encode(file.read())
                photo_base64 = photo_base64.decode('utf-8')  # Pastikan ini string, bukan byte
            else:
                photo_base64 = None

            # _logger.info(f"Form Submission Name: {file}")
            # _logger.info(f"Form Submission Name: {photo_base64}")

            photo = post.get('photo')
            photo_base64 = base64.b64encode(photo.read())
            photo_base64 = photo_base64.decode('utf-8')

            form_submission = request.env['form.submission'].sudo().create({
                'name': post.get('name'),
                'phone': post.get('phone'),
                'email': post.get('email'),
                'visitingDate': post.get('visitingDate'),
                'KTP_number': post.get('KTP_number'),
                'company_name': post.get('company_name'),
                'visit_purpose': post.get('visit_purpose'),
                'intended_person': post.get('intended_person'),
                'photo': photo_base64,
                # 'photo': photo_base64,
                # 'photo': post.get('photo'),
            })

            # _logger.info(f"GET ID FROM FORM: ------------->{form_submission.id}<-------------")

            request.session['session_form_submission_id'] = form_submission.id

            # return request.redirect('/regpay/%s' % form_submission.id)

            # file = post.get('photo')
            # if file:
            #     file_name = file.filename
            #     attachment_id = request.env['ir.attachment'].create({
            #         'name': file_name,
            #         'type': 'binary',
            #         'datas': base64.b64encode(file.read()),
            #         'res_model': 'res.partner',
            #         'res_id': request.env.user.partner_id.id
            #     })
            #     request.env.user.partner_id.update({
            #         "file_attachment_ids": [(4, attachment_id.id)],
            #     })

            # return request.redirect('/contactus-thank-you')
        except Exception as e:
            _logger.info(f"Error: ______-------______-> {e}")
        finally:
            # return request.redirect('/contactus-thank-you')
            # return request.redirect('/regpay')
            # return request.redirect('/regpay/%s' % form_submission.id)
            return request.redirect('/regpay')

    # @http.route('/regpay/<int:form_submission_id>',type='http', auth='public',methods=['GET', 'POST'], website=True)
    @http.route('/regpay',type='http', auth='user',methods=['GET', 'POST'], website=True)
    def payment(self,  **post):
        # Get Session
        session_form_submission_id = request.session.get('session_form_submission_id')

        if request.httprequest.method == 'POST':
            try:
                # Simpan data pembayaran
                request.env['ticket.payment'].create({
                    'form_submission_id': session_form_submission_id,
                    'category': post.get('category'),
                    'duration': post.get('duration'),
                    'quantity': post.get('quantity'),
                    'payment_date': post.get('payment_date'),
                })
            except Exception as e:
                _logger.info(f"Error: ______-------______-> {e}")
            finally:
                # del request.session['session_form_submission_id']
                # _logger.info(f"DELETED SESSION: ______-------______-> {session_form_submission_id}")
                return request.redirect('/payment-confirmation')

        return request.render('event_management.payment_template')

    #
    # @http.route('/regpay/<int:form_submission_id>', type='http', auth='public', methods=['POST'], csrf=False)
    # def payment(self, form_submission_id, **post):
    #     _logger.info(f"GET ID FROM URL: ______-------______-> {form_submission_id}")
    #     try:
    #         # Simpan data pembayaran
    #         request.env['ticket.payment'].create({
    #             'form_submission_id': form_submission_id,
    #             'category': post.get('category'),
    #             'duration': post.get('duration'),
    #             'quantity': post.get('quantity'),
    #             'payment_date': post.get('payment_date'),
    #         })
    #
    #         # Redirect ke halaman konfirmasi atau halaman lainnya
    #
    #         # Render halaman pembayaran
    #         # return request.render('event_management.visitor_registration_and_payment_template', {
    #         #     'form_submission_id': form_submission_id,
    #         # })
    #     except Exception as e:
    #         _logger.info(f"Error: ______-------______-> {e}")
    #     finally:
    #         return request.redirect('/payment/confirmation')
