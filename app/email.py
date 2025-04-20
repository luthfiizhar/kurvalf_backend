import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.models import ReceivedEmail

from dotenv import load_dotenv
load_dotenv('.env')

class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_APP_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT',"25"))
    MAIL_SERVER = os.getenv('MAIL_SERVER',"smtp.gmail.com")
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')

conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME="Stock Of Valve",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email_async(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')

def send_email_background(background_tasks: BackgroundTasks, form: ReceivedEmail):
    html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Template</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background: #007bff;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    font-size: 20px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }}
                .content {{
                    padding: 20px;
                    text-align: left;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                    padding: 10px;
                    border-top: 1px solid #ddd;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    color: white;
                    background: #28a745;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">Notification Email</div>
                <div class="content">
                    <p>Hello,</p>
                    <p>Thank you for contacting us. Here are the details of the information you submitted:</p>
                    <p><strong>Topic:</strong> {form.topic}</p>
                    <p><strong>Name:</strong> {form.name}</p>
                    <p><strong>Email:</strong> {form.email}</p>
                    <p><strong>Message:</strong> {form.message}</p>
                </div>
                <div class="footer">
                    &copy; 2025 Stock Of Valve. All rights reserved.
                </div>
            </div>
        </body>
        </html>
    '''
    
    message = MessageSchema(
        subject=form.topic,
        recipients=[form.email],
        cc=[conf.MAIL_FROM],
        body=html,
        subtype='html',
    )
    fm = FastMail(conf)
    background_tasks.add_task(
       fm.send_message, message)