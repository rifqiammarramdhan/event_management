from odoo import http
from odoo.http import content_disposition, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class AttendanceRegisterController(http.Controller):
    @http.route(['/send_payment_confirmation/<model("attendance.register"):data>',],type="http", auth="user",csrf="False")
    def sendMail(self, data=None, **args):
        email_pengirim = "rifqiammarkontak@gmail.com"
        password = "ybwv atax yake lfgo"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        try:

            msg = MIMEMultipart()
            for item in data:
                msg["From"] = email_pengirim
                msg["To"] = item.email
                msg["Subject"] = "Visitor Accepted"
                print(item.email)
                html_content = """
                <html>
                <body>
                    <p>Halo,<br>
                    Ini adalah contoh email dengan <b>format HTML</b>.<br>
                    Berikut adalah gambar sederhana:<br>
                    <img src="cid:image1" alt="image1">
                    </p>
                </body>
                </html>
                """

                body = MIMEText(html_content, "html")
                msg.attach(body)

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()  # aktifkan enkripsi TLS
                server.login(email_pengirim, password)
                server.send_message(msg)
                print("Email berhasil dikirim!")
        except Exception as e:
            print(f"Gagal mengirim email. Error: {str(e)}")
        finally:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.quit()

# class AttendanceRegisterController(http.Controller):
#
#     @http.route('/send_payment_confirmation/<int:record_id>', type='http', auth='public', website=True)
#     def send_payment_confirmation(self, record_id, **kw):
#         # Ambil record berdasarkan ID
#         record = request.env['attendance.register'].browse(record_id)
#         if not record:
#             return request.not_found()
#
#         # Dapatkan template email
#         template = request.env.ref('event_management.email_template_payment_confirmation')
#         if template:
#             # Kirim email
#             template.send_mail(record.id, force_send=True)


