import email
import smtplib
import re
from email.mime.text import MIMEText

from baseemail import BaseEmail
from popemail import PopEmail
from imapemail import ImapEmail

class IspEmail(BaseEmail):
   def __init__(self, user, passwd):
      self.user = user
      self.passwd = passwd
      self.domain = re.search("@[\w.]+\.", user).group()[1:-1]
      self.setting = self.__getServerSetting()
      self.smtpsetting = self.__getSmptServerSetting()

   def connect(self):
      if self.setting is None:
         raise ValueError('Unable to find setting for ' + self.domain + ' domain')
      if self.setting.get("type") == "pop":
         self.mail = PopEmail(self.user, self.passwd, self.setting.get("server"), self.setting.get("port"))
      else:
         self.mail = ImapEmail(self.user, self.passwd, self.setting.get("server"))

      try:
         self.mail.connect()
      except:
         raise ValueError('username or password is incorrect.');
   
   def getMessage(self, index):
      return email.message_from_string(self.mail.getRawMessage(index));

   def printRawMessage(self, index):
      print self.mail.getRawMessage(index)

   def deleteMessage(self, index):
      self.mail.deleteMessage(index)

   def sendMessage(self, to, subject, message):
      msg = MIMEText(message)
      msg['From'] = self.user
      msg['To'] = to
      msg['Subject'] = subject
      
      smtp = smtplib.SMTP(self.smtpsetting.get("server"), self.smtpsetting.get("port"))
      smtp.ehlo()
      smtp.starttls()
      smtp.ehlo()
      smtp.login(self.user, self.passwd)
      smtp.sendmail(self.user, to, msg.as_string())
      smtp.quit()

   def close(self):
      self.mail.close()

   def __getServerSetting(self):
      return {
         'hotmail': {'server':'pop3.live.com', 'port': 995, 'type': 'pop'},
         'live': {'server':'pop3.live.com', 'port': 995, 'type': 'pop'},
         'outlook': {'server':'pop3.live.com', 'port': 995, 'type': 'pop'},
         'yahoo': {'server':'pop.mail.yahoo.com', 'port': 995, 'type': 'pop'},
         'aol': {'server':'imap.aol.com', 'port': 993, 'type': 'imap'}
      }.get(self.domain)

   def __getSmptServerSetting(self):
      return {
         'hotmail': {'server':'smtp.live.com', 'port': 587},
         'live': {'server':'smtp.live.com', 'port': 587},
         'outlook': {'server':'smtp.live.com', 'port': 587},
         'yahoo': {'server':'smtp.mail.yahoo.com', 'port': 587},
         'aol': {'server':'smtp.aol.com', 'port': 587}
      }.get(self.domain)
