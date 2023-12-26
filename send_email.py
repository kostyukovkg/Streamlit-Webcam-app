import smtplib, mimetypes
import streamlit as st

def attach_bytesio_to_email(email, buf, filename):
    """Attach a file identified by filename, to an email message"""
    # Reset read position & extract data
    buf.seek(0)
    binary_data = buf.read()
    # Guess MIME type or use 'application/octet-stream'
    maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
    # Add as attachment
    email.add_attachment(binary_data, maintype=maintype, subtype=subtype, filename=filename)


def send_mail_smtp(msg, host, username, password = st.secrets["gmail_key"]):
    s = smtplib.SMTP(host)
    s.starttls()
    s.login(username, password)
    s.send_message(msg)
    s.quit()


