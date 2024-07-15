# from odoo import http
# from odoo.addons.auth_signup.controllers.main import AuthSignupHome
# from odoo.http import request
#
# import logging
# _logger = logging.getLogger(__name__)
#
# class AuthSignupExtended(AuthSignupHome):
#
#     @http.route('/web/signup', type='http', auth='public', website=True)
#     def web_auth_signup(self, *args, **kw):
#         response = super(AuthSignupExtended, self).web_auth_signup(*args, **kw)
#         # Here, you can customize the behavior after signup
#         _logger.info(f"Error: ______-------______-> {response}")
#         # For example, redirect to a page requesting email confirmation
#         return request.redirect('/emailconfirmation')
