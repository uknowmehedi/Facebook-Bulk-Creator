import imaplib, email, re, time

def get_otp_from_gmail(address, app_password, wait_time=60):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(address, app_password)
    mail.select("inbox")
    end_time = time.time() + wait_time
    otp = None
    while time.time() < end_time:
        result, data = mail.search(None, "UNSEEN")
        ids = data[0].split()
        for num in ids:
            result, msg_data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            body = msg.get_payload(decode=True).decode()
            match = re.search(r"(\\d{5,6})", body)
            if match:
                otp = match.group(1)
                break
        if otp: break
        time.sleep(5)
    mail.logout()
    return otp