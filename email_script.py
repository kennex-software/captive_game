import smtplib, ssl

port = 465
sender = "messingwithjack@gmail.com"
password = "x4&&b4@UxAIy"
receive = 'm.novak@redswinggroup.com'


message = """From: Bars <p.kennedy@redswinggroup.com>
To: m.novak@redswinggroup.com
Subject: Timesheet is Due

This is why you need to do your timesheet on time.
This is why you need to do your timesheet on time.
This is why you need to do your timesheet on time.
This is why you need to do your timesheet on time.


"""


context = ssl.create_default_context()

print("Starting to send...")
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
      server.login(sender, password)

      for x in range(101):
            server.sendmail(sender, receive, message)

print('Sent Email!')


