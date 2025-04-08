from twilio.rest import Client

# Your Twilio Account SID and Auth Token
account_sid = ''
auth_token = ''

# Initialize Twilio client
client = Client(account_sid, auth_token)

def send_sms(to, body):
    try:
        # Send SMS
        message = client.messages.create(
            body=body,
            from_='',
            to=to
        )
        print("Message sent successfully! SID:", message.sid)
    except Exception as e:
        print("Error:", str(e))

# Example usage
if __name__ == "__main__":
    to_number = input("Enter recipient's phone number: ")
    message_body = input("Enter the message: ")
    send_sms(to_number, message_body)
