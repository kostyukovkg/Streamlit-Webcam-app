import streamlit as st
from PIL import Image
import send_email
from io import BytesIO
from email.message import EmailMessage

st.title('A simple webcam app')

img_file_buffer = st.camera_input("Here you can take a picture and send it to your email") # UploadedFile object

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer) # JPEG image

    st.image(img)

    bytes_img = img_file_buffer.getvalue()
    # Email form to send a picture. Enter.
    with st.form(key="main_form"):

        user_email = st.text_input(
            "Please enter your email address and I will send your photo")

        button = st.form_submit_button(
            'Send email')  # special button that submits text for the form.

        if button:
            # Attach files
            buf = BytesIO()
            buf.write(bytes_img)

            # Create message and set text content
            msg = EmailMessage()
            msg['Subject'] = 'This is your photo!'
            msg['From'] = st.secrets["gmail_email"]
            msg['To'] = user_email
            msg.set_content('Please see the attached file.')

            send_email.attach_bytesio_to_email(msg, buf, "your_photo.png")
            send_email.send_mail_smtp(msg, 'smtp.gmail.com', msg['From'])