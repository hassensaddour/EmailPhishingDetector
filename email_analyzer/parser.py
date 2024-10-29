import email

def parse_email(raw_email):
    msg = email.message_from_string(raw_email)
    email_data = {
        'subject': msg['Subject'],
        'from': msg['From'],
        'to': msg['To'],
        'body': get_email_body(msg)
    }
    return email_data

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ['text/plain', 'text/html']:
                return part.get_payload(decode=True).decode('utf-8')
    else:
        return msg.get_payload(decode=True).decode('utf-8')
