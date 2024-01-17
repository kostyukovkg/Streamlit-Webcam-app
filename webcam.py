import streamlit as st
from PIL import Image
import send_email
from io import BytesIO
from email.message import EmailMessage

st.title('Photo Booth')

img_file_buffer = st.camera_input("You can take a picture and send it to any email you choose") # UploadedFile object

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer) # JPEG image

    st.image(img)

    bytes_img = img_file_buffer.getvalue() # Bytes image
    # Email form to send a picture. Enter.
    with st.form(key="main_form"):
        user_msg = st.text_area("Please enter your message to the recipient (if you want)")
        user_msg = user_msg + \
                   '\n\n\n\nDisclaimer:' \
                   '\nThis message and photo were created on https://kkg-photo-booth.streamlit.app/' \
                   '\nYou can check my other projects on https://kkgweb.streamlit.app/'
        user_email = st.text_input("Please enter the recipient's email")

        button = st.form_submit_button('Send email')  # special button that submits text for the form.


        if button:
            # Attach files
            buf = BytesIO()
            buf.write(bytes_img)

            # Create message and set text content
            msg = EmailMessage()
            msg['Subject'] = 'Hello! You have a new photo from Photo Booth!'
            msg['From'] = st.secrets["gmail_email"]
            msg['To'] = user_email
            msg.set_content(user_msg)

            send_email.attach_bytesio_to_email(msg, buf, "kkg_photo_booth.png")
            send_email.send_mail_smtp(msg, 'smtp.gmail.com', msg['From'])

            st.info("Your email was sent successfully")