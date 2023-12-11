from email.utils import formataddr

import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
import smtplib
from email.message import EmailMessage
from src.config import SMTP_FROM, SMTP_SERVER, SMTP_PASSWORD, SMTP_USER


def generate_invoice(data) -> bytes:
    path = os.getcwd() + '/src/modules/admin/mail/templates'
    templateLoader = FileSystemLoader(searchpath=path)
    templateEnv = Environment(loader=templateLoader, autoescape=True)
    template = templateEnv.get_template('invoice.html')
    raw_html = template.render(data)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    return pdfkit.from_string(raw_html)


def send_invoice(to: str, subject: str, data: dict):

    smtp_server = SMTP_SERVER
    sender = SMTP_FROM
    destination = [to]

    username = SMTP_USER
    password = SMTP_PASSWORD

    conn = smtplib.SMTP(smtp_server)
    conn.set_debuglevel(False)
    conn.login(username, password)

    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = formataddr(('WoodenGames', sender))
    msg['To'] = destination
    invoice_data = generate_invoice(data)
    msg.add_attachment(invoice_data, maintype='application', subtype='pdf', filename='Invoice.pdf')

    try:
        conn.send_message(msg)
        conn.close()
    except Exception as e:
        print(f'Email not send! order: {data["order"]["id"]} {e}')
