import os
import tempfile
from odoo import http
from odoo.http import content_disposition, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import segno
import jwt

import logging
_logger = logging.getLogger(__name__)
class AttendanceRegisterController(http.Controller):
    @http.route(
        [
            '/send_email_accepted/<model("attendance.register"):data>',
        ],
        type="http",
        auth="user",
        csrf="False",
    )
    def sendMail(self, data=None, **args):
        email_pengirim = "rifqiammarkontak@gmail.com"
        password = "ybwv atax yake lfgo"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        msg = MIMEMultipart()
        # path = os.path.abspath("temp/img/qrcode/qrcode.png")
        try:
            for item in data:
                msg["From"] = email_pengirim
                msg["To"] = item.email
                msg["Subject"] = "Visitor Accepted"

                _logger.warning(f"Ini adalah pesan log {item.name}")

                # Generate JWT
                encoded_jwt = jwt.encode(
                    {"name": item.email, "status": "accepted"},
                    "secr3t673et",
                    algorithm="HS256",
                )

                # Generate QR code
                qrcode = segno.make_qr(encoded_jwt)


                # Membuat temporary file dan membuat qrcode
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file_path = tmp_file.name
                    _logger.info(f"QR CODE PATH{tmp_file_path}")
                    qrcode.save(tmp_file_path, scale=5)

                html_content = f"""
                <html>
                <body>
                    <p>Halo,{item.name}<br>
                    Selamat registrasi untuk visitor anda telah di <b>Terima</b>.<br>
                    Berikut adalah QR code untuk konfirmasi:<br>
                    <img src="cid:qrcode_image" alt="QR Code">
                    </p>
                </body>
                </html>
                """
                body = MIMEText(html_content, "html")
                msg.attach(body)

                with open(tmp_file_path, "rb") as f:
                    attachment = MIMEBase("application", "octet-stream")
                    print({"attachment": attachment})
                    attachment.set_payload(f.read())
                    encoders.encode_base64(attachment)
                    attachment.add_header(
                        "Content-Disposition", "attachment", filename="qrcode.png"
                    )
                    attachment.add_header("Content-ID", "<qrcode_image>")
                    msg.attach(attachment)

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()  # aktifkan enkripsi TLS
                server.login(email_pengirim, password)
                server.send_message(msg)

                _logger.info("Email berhasil dikirim!")
        except Exception as e:
            _logger.info(f"Gagal mengirim email. Error: {str(e)}")
        finally:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if server:
                server.quit()

            # # Delete temp file
            # qr_code_file = "temp/img/qrcode/qrcode.png"
            # if os.path.exists(qr_code_file):
            #     os.remove(qr_code_file)
            #     print(f"File QR code sementara {qr_code_file} telah dihapus.")
