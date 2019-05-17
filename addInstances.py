#!/usr/bin/python
import os, socket, smtplib, logging,subprocess
from email.mime.text  import MIMEText



logging.basicConfig(filename="general_lead.log", filemode='a', level=logging.DEBUG, format = "%(asctime)s:%(levelname)s:%(message)s")
logging.debug(" --- Script started --- ")


def email_send():
    smtpaddress = "172.21.12.56"
    smtpport = 25
    from_adr = "message.flow@kapitalbank.az"
    user_pass = ""
    send_adr = ["farid.baxishli@kapitalbank.az"]
    subject = "CRM. Additional instance was not set."
    content = """ Additional instance configured """
    timeout_value = 30 # seconds
    try:
        mail = MIMEText(content, "html", "utf-8")
        mail["From"] = from_adr
        mail["Subject"] = subject
        mail["To"] = ",".join(send_adr)
        mail = mail.as_string()
        socket.setdefaulttimeout(timeout_value)
        s = smtplib.SMTP(smtpaddress,smtpport)
        #s.starttls()                          # Disable it because local email doesn't support tls auth
        #s.login(from_adr, user_pass)          # Disable it because local email doesn't support auth
        s.sendmail(from_adr, send_adr, mail)
        logging.debug(" EMail Sent.")
        #print("EMail Sent.")
        s.quit()
    except Exception as e:
        # Print any error messages to stdout
        logging.debug(' Mail sending host %s and port %s error : %s', smtpaddress, smtpport, e)

checker =  os.popen('/opt/IBM/iib-10.0.0.14/server/bin/mqsireportpolicy CRM -e REST -m gen.CRMApp -k CRMApp | grep BIP1910I').read()
add_instance = '/opt/IBM/iib-10.0.0.14/server/bin/mqsiattachpolicy CRM -e REST -m gen.CRMApp -l REST50 -t WorkloadManagement -k CRMApp'

print(checker)
#exit()
if checker != "":
    subprocess.call(add_instance, shell=True)
    email_send()
