###############################################################################
# TODO:
# - change domain and credentials (NEED NEW DOMAIN!!!)
# - create new email for network maintenance mass mail
# - create new robots email
###############################################################################

import smtplib

def send(subject, text, to):
    server = smtplib.SMTP("mail.blackhat.sh", 587)
    server.ehlo()
    server.starttls()
    server.login("robot@arachnid.cc", "NFgVWtJQPEWgboTLmgXkwYQbQurQd5XvtqBKL9qkp")
    
    body = '\r\n'.join(['To: %s' % to, 'From: %s' % str("Arachnid Network"), 'Subject: %s' % subject, '', text])
    
    server.sendmail("robot@arachnid.cc", [to], body)

    server.quit()

body = """
Hello,

During the above window, the Constellation networking team will be making changes to our servers.

Expected Impact:
    <INSERT INFO HERE>

Do not hesistate to contact our NOC team at <NOC EMAIL> for any comments or questions. Our NOC team will be monitoring that address during the maintenance period.

Thank you,

Constellation Network Team

"""

send("Network Maintenance", body, "robot@arachnid.cc")
