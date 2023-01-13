import smtplib, ssl
from configparser import ConfigParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

config_object = ConfigParser()
config_object.read("config.ini")

mail_server = config_object["SMTP_SERVER"]

sender_email = mail_server["mail"]
password = mail_server["password"]
port = mail_server["port"]
host = mail_server["host"]



def mail_account_register(email, firstname, lastname):
    # Création de la forme de l'email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Notification de création"
    message["From"] = sender_email
    message["To"] = email

    # Texte qui sera envoyé
    text = f"""\
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; margin: 0; padding: 0;">
        <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Really Simple HTML Email Template</title>
        </head>
        <body bgcolor="#f6f6f6" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; margin: 0; padding: 0;">&#13;
        &#13;
        &#13;
        <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 20px;">
            <tbody>
                <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                    <td bgcolor="#FFFFFF" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;display: block;max-width: 600px;clear: both;margin: 0 auto;padding: 20px;border: 1px solid #f0f0f0;">
                        <div style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;max-width: 600px;display: block;margin: 0 auto;padding: 0;">
                            <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 0;">
                                <tbody>
                                    <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                        <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Bonjour {lastname} {firstname},</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Votre compte à été créer avec succès.</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Cordialement,</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">ItzMyManager.</p>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </td>
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                </tr>
            </tbody>
        </table></body>
        </html>
        """

    # Creation des variables pour le text
    part2 = MIMEText(text, "html")

    # Attachement du text à l'email
    message.attach(part2)

    # Création d'une variable qui implente le ssl pour l'email donc envoie sécuriser
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(host, port)
    server.ehlo()
    server.starttls
    server.login(sender_email, password)
    server.sendmail(sender_email , email , message.as_string())

def user_account_information(new_username, new_email, new_firstname, new_lastname):
    # Création de la forme de l'email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Notification de modification"
    message["From"] = sender_email
    message["To"] = new_email

    # Texte qui sera envoyé
    text = f"""\
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; margin: 0; padding: 0;">
        <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Really Simple HTML Email Template</title>
        </head>
        <body bgcolor="#f6f6f6" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; margin: 0; padding: 0;">&#13;
        &#13;
        &#13;
        <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 20px;">
            <tbody>
                <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                    <td bgcolor="#FFFFFF" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;display: block;max-width: 600px;clear: both;margin: 0 auto;padding: 20px;border: 1px solid #f0f0f0;">
                        <div style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;max-width: 600px;display: block;margin: 0 auto;padding: 0;">
                            <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 0;">
                                <tbody>
                                    <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                        <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Bonjour {new_lastname} {new_firstname},</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Vos informations on été modifié avec succès.</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Voici vos informations mis à jours :</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">- Nom : {new_lastname}</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">- Prénom : {new_firstname}</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">- Nom d&#39;utilisateur : {new_username}</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">- Email : {new_email}</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Cordialement,</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">ItzMyManager.</p>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </td>
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                </tr>
            </tbody>
        </table></body>
        </html>
        """

    # Creation des variables pour le text
    part2 = MIMEText(text, "html")

    # Attachement du text à l'email
    message.attach(part2)

    # Création d'une variable qui implente le ssl pour l'email donc envoie sécuriser
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(host, port)
    server.ehlo()
    server.starttls
    server.login(sender_email, password)
    server.sendmail(sender_email , new_email , message.as_string())

def user_account_address(new_address, new_city, new_country, lastname, firstname, email):
    # Création de la forme de l'email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Notification de modification"
    message["From"] = sender_email
    message["To"] = email

    # Texte qui sera envoyé
    text = f"""\
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; margin: 0; padding: 0;">
        <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Really Simple HTML Email Template</title>
        </head>
        <body bgcolor="#f6f6f6" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; margin: 0; padding: 0;">&#13;
        &#13;
        &#13;
        <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 20px;">
            <tbody>
                <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                    <td bgcolor="#FFFFFF" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;display: block;max-width: 600px;clear: both;margin: 0 auto;padding: 20px;border: 1px solid #f0f0f0;">
                        <div style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;max-width: 600px;display: block;margin: 0 auto;padding: 0;">
                            <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 0;">
                                <tbody>
                                    <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                        <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Bonjour {lastname} {firstname},</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Votre adresse a été modifié avec succès.</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Voici vos informations mis à jours :</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">- Adresse : {new_address}</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">- Ville : {new_city}</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">- Pays : {new_country}</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Cordialement,</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">ItzMyManager.</p>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </td>
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                </tr>
            </tbody>
        </table></body>
        </html>
        """

    # Creation des variables pour le text
    part2 = MIMEText(text, "html")

    # Attachement du text à l'email
    message.attach(part2)

    # Création d'une variable qui implente le ssl pour l'email donc envoie sécuriser
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(host, port)
    server.ehlo()
    server.starttls
    server.login(sender_email, password)
    server.sendmail(sender_email , email , message.as_string())

def user_account_password(email, firstname, lastname):
    # Création de la forme de l'email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Notification de modification"
    message["From"] = sender_email
    message["To"] = email

    # Texte qui sera envoyé
    text = f"""\
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; margin: 0; padding: 0;">
        <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Really Simple HTML Email Template</title>
        </head>
        <body bgcolor="#f6f6f6" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; margin: 0; padding: 0;">&#13;
        &#13;
        &#13;
        <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 20px;">
            <tbody>
                <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                    <td bgcolor="#FFFFFF" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;display: block;max-width: 600px;clear: both;margin: 0 auto;padding: 20px;border: 1px solid #f0f0f0;">
                        <div style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;max-width: 600px;display: block;margin: 0 auto;padding: 0;">
                            <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 0;">
                                <tbody>
                                    <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                        <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Bonjour {lastname} {firstname},</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Votre mot de passe a été modifié avec succès.</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Cordialement,</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">ItzMyManager.</p>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </td>
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                </tr>
            </tbody>
        </table></body>
        </html>
        """

    # Creation des variables pour le text
    part2 = MIMEText(text, "html")

    # Attachement du text à l'email
    message.attach(part2)

    # Création d'une variable qui implente le ssl pour l'email donc envoie sécuriser
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(host, port)
    server.ehlo()
    server.starttls
    server.login(sender_email, password)
    server.sendmail(sender_email , email , message.as_string())


def user_forgot_password(email, new_password):
    # Création de la forme de l'email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Notification de modification"
    message["From"] = sender_email
    message["To"] = email

    # Texte qui sera envoyé
    text = f"""\
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; margin: 0; padding: 0;">
        <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Really Simple HTML Email Template</title>
        </head>
        <body bgcolor="#f6f6f6" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; margin: 0; padding: 0;">&#13;
        &#13;
        &#13;
        <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 20px;">
            <tbody>
                <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                    <td bgcolor="#FFFFFF" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;display: block;max-width: 600px;clear: both;margin: 0 auto;padding: 20px;border: 1px solid #f0f0f0;">
                        <div style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;max-width: 600px;display: block;margin: 0 auto;padding: 0;">
                            <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 0;">
                                <tbody>
                                    <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                        <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Bonjour,</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Votre demande de changement de mot de passe a été prise en compte</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Voici votre nouveau mot de passe:</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;">{new_password}</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;">Veuillez changer ce mot de passe dès que vous vous connectez à votre compte !</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Cordialement,</p>
                                            <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">ItzMyManager.</p>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </td>
                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                </tr>
            </tbody>
        </table></body>
        </html>
        """

    # Creation des variables pour le text
    part2 = MIMEText(text, "html")

    # Attachement du text à l'email
    message.attach(part2)

    # Création d'une variable qui implente le ssl pour l'email donc envoie sécuriser
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(host, port)
    server.ehlo()
    server.starttls
    server.login(sender_email, password)
    server.sendmail(sender_email , email , message.as_string())

def create_account_mail(email, firstname, lastname, username, adresse, city, country, user_password):
    # Création de la forme de l'email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Notification de modification"
    message["From"] = sender_email
    message["To"] = email

    # Texte qui sera envoyé
    text = f"""\
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; margin: 0; padding: 0;">
        <head>
            <meta name="viewport" content="width=device-width" />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Really Simple HTML Email Template</title>
        </head>
        <body bgcolor="#f6f6f6" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 100%; line-height: 1.6; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; margin: 0; padding: 0;">&#13;
        &#13;
        &#13;
        <div>
    <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 20px;">
        <tbody>
            <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
                <td bgcolor="#FFFFFF" style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;display: block;max-width: 600px;clear: both;margin: 0 auto;padding: 20px;border: 1px solid #f0f0f0;">
                    <div style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;max-width: 600px;display: block;margin: 0 auto;padding: 0;">
                        <table style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;width: 100%;margin: 0;padding: 0;">
                            <tbody>
                                <tr style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                    <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;">
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Bonjour {lastname} {firstname},</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">Votre compte à été créer avec succès par un technicien !</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Informations du compte :</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin-bottom: 0px;">Utilisateur : {username}</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin-bottom: 0px;">Nom : {lastname}</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin-bottom: 0px;">Prénom : {firstname}</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin-bottom: 0px;">Email : {email}</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin-bottom: 0px;">Adresse : {adresse}</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin-bottom: 0px;">Ville : {city}</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin-bottom: 16px;">Pays : {country}</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;">Pour vous connecter, voici le mot de passe :</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin-bottom: 16px;">Mot de passe : {user_password}</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;">Sacher qu&#39;il est fortement recommandé de le changer lors de la premier connexion.</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;margin-bottom: 0px;">Cordialement,</p>
                                        <p style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 14px;line-height: 1.6;font-weight: normal;margin: 0 0 10px;padding: 0;">ItzMyManager.</p>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </td>
                <td style="font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;font-size: 100%;line-height: 1.6;margin: 0;padding: 0;"></td>
            </tr>
        </tbody>
    </table></body>
        </html>
        """

    # Creation des variables pour le text
    part2 = MIMEText(text, "html")

    # Attachement du text à l'email
    message.attach(part2)

    # Création d'une variable qui implente le ssl pour l'email donc envoie sécuriser
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(host, port)
    server.ehlo()
    server.starttls
    server.login(sender_email, password)
    server.sendmail(sender_email , email , message.as_string())