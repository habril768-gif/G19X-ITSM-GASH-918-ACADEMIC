"""Adaptador SMTP configurable; errores sin diálogo del servidor."""
import os, re, smtplib, ssl
from email.message import EmailMessage
from urllib.parse import urlsplit

class DeliveryError(Exception):
    def __init__(self, transient=False):
        super().__init__('Entrega SMTP no confirmada'); self.transient=transient

def address(value):
    if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+", value):
        raise DeliveryError()
    return value

class SMTPTransport:
    def __init__(self):
        self.host=os.environ.get('SMTP_HOST','mailpit')
        self.port=int(os.environ.get('SMTP_PORT','1025'))
        self.mode=os.environ.get('MAIL_MODE','capture').lower()
        self.tls=os.environ.get('SMTP_TLS','none').lower()
        self.sender=address(os.environ.get('SMTP_FROM','no-reply@plurione.invalid'))
        self.base=os.environ.get('WEB_BASE_URL','http://127.0.0.1:5173').rstrip('/')
        parsed=urlsplit(self.base)
        if parsed.scheme not in {'http','https'} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or any(c.isspace() for c in self.base):
            raise ValueError('URL de plataforma no válida')
        if self.mode not in {'capture','external'} or self.tls not in {'none','starttls','ssl'}:
            raise ValueError('Modo SMTP no válido')
        if self.mode=='capture' and (self.host not in {'mailpit','127.0.0.1','localhost','::1'} or self.tls!='none'):
            raise ValueError('Captura requiere servidor local sin TLS')
        if self.mode=='external' and (self.tls=='none' or parsed.scheme!='https'):
            raise ValueError('Correo externo requiere TLS y enlace HTTPS')

    def send(self, recipient, case_id, delivery_id):
        message=EmailMessage()
        message['From']=self.sender; message['To']=address(recipient)
        message['Subject']=f'PluriOne · Caso {case_id}'
        message['Message-ID']=f'<{delivery_id}@plurione.invalid>'
        message.set_content(f'Hay una actualización disponible. Consulta el expediente con tu cuenta autorizada:\n{self.base}/?incident={case_id}\n')
        smtp=None
        try:
            cls=smtplib.SMTP_SSL if self.tls=='ssl' else smtplib.SMTP
            kwargs={'timeout':5,'local_hostname':'plurione.invalid'}
            if self.tls=='ssl': kwargs['context']=ssl.create_default_context()
            smtp=cls(self.host,self.port,**kwargs)
            smtp.ehlo()
            if self.tls=='starttls': smtp.starttls(context=ssl.create_default_context()); smtp.ehlo()
            username=os.environ.get('SMTP_USERNAME','')
            if username:
                if self.mode=='capture': raise DeliveryError()
                smtp.login(username,os.environ.get('SMTP_PASSWORD',''))
            refused=smtp.send_message(message,from_addr=self.sender,to_addrs=[recipient])
            if refused: raise DeliveryError()
        except smtplib.SMTPRecipientsRefused as exc:
            raise DeliveryError(bool(exc.recipients) and all(400 <= code < 500 for code,_ in exc.recipients.values())) from None
        except smtplib.SMTPResponseException as exc:
            raise DeliveryError(400 <= exc.smtp_code < 500) from None
        except (ssl.SSLError,smtplib.SMTPNotSupportedError):
            raise DeliveryError() from None
        except (OSError,smtplib.SMTPServerDisconnected):
            raise DeliveryError(True) from None
        except (smtplib.SMTPException,ValueError,UnicodeError):
            raise DeliveryError() from None
        finally:
            if smtp is not None:
                try: smtp.close()
                except OSError: pass
