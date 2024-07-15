from odoo import http
from odoo.http import request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import datetime

import logging
_logger = logging.getLogger(__name__)

class AuthController(http.Controller):
    @http.route('/user/signup', type='http', auth='public', website=True, csrf=True)
    def signUp(self, **post):
        email = post.get('email')
        login = post.get('login')
        password = post.get('password')
        name = post.get('name')

        # if password != confirm_password:
        #     return request.render('your_module_name.website_signup_page', {
        #         'error': 'Passwords do not match',
        #     })

        values = {
                'email': email,
                'password': password,
                'name' : name,
                'login': login
            }

        try:
            _logger.info(f"----------------> GET EMAIL <--------------: {email}")
            _logger.info(f"----------------> GET PASSWORD <--------------: {password}")

            # Create a new user
            request.env['res.users'].sudo().create(values)

            _logger.info(f"----------------> GET EMAIL BOTTOM <--------------: {email}")

            # Generate JWT
            encoded_jwt = jwt.encode(
                {"email": email, "status": "accepted", "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                "secr3t#$673et",
                algorithm="HS256",
            )

            # function sendemail
            self.sendEmailConfirmation(email, encoded_jwt)

            # Membuat Session
            _logger.info(f"----------------> SET SESSION FROM POST EMAIL <--------------: {email}")
            request.session['almostEmail'] = email

        except Exception as e:
            _logger.error('------->Error creating user: %s---->', e)
            return request.redirect('/registration/failed', {
                'error': 'An error occurred. Please try again.',
            })
        finally:
            return request.redirect('/emailconfirmation')

    @http.route('/emailconfirmation', auth='public', website=True)
    def almost_page(self, **kwargs):
        email = request.session.get('almostEmail')
        _logger.info(f"----------------> GET EMAIL FORM SESSION <--------------: {email}")

        return request.render('event_management.almost_template_id',{
                'almostEmail': email
            })

    @http.route('/email-confirm/<token>',  type='http', website=True, csrf=True)
    def email_confirm(self, token):
        if token:
            _logger.info(f"----------------> GET Token <--------------: {token}")
            try:
                decoded_payload = jwt.decode(token, "secr3t#$673et", algorithms=['HS256'])
                _logger.info(f"---------> GET Decode Token <-----------: {decoded_payload}")
                return request.redirect('/payment')
            except jwt.ExpiredSignatureError:
                _logger.info("JWT ExpiredSignatureError: -------> Token sudah kadaluarsa <-------")
            except jwt.InvalidTokenError:
                _logger.info("JWT InvalidTokenError: -------> Token tidak valid <---------")
        else:
            return request.redirect('/notoken')

    def sendEmailConfirmation(self, to_email, token):
        _logger.info(f"----------------> Enter The Email <--------------:")
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        try:
            sender_email = 'rifqiammarkontak@gmail.com'
            sender_password = 'ybwv atax yake lfgo'

            subject = 'Konfirmasi Email'
            body = f'Silakan konfirmasi email Anda dengan tautan berikut: http://localhost:8069/email-confirm/{token}'

            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = to_email
            message['Subject'] = subject

            message.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, to_email, text)
        except Exception as e:
            _logger.info(f"Gagal mengirim email. Error: -------><------- {str(e)}")

        finally:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if server:
                _logger.info(f"----------------> Send Email to {to_email} Success <--------------:")
                server.quit()



