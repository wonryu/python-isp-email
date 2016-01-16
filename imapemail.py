import imaplib
import re
from baseemail import BaseEmail

class ImapEmail(BaseEmail):
   def __init__(self, user, passwd, server):
      self.user = user
      self.passwd = passwd
      self.server = server


   def connect(self):
      print "connecting..."
      self.imap = imaplib.IMAP4_SSL(self.server)      
      try:
         self.imap.login(self.user, self.passwd)
         self.imap.select("inbox")
      except:
         raise ValueError('username or password is incorrect.');
      else:
         print "connected."
         result, self.data = self.imap.search(None, "ALL")
         self.total = len(self.data[0].split())
         print self.data[0].split()
         print "There are total %i messages" % (self.total)
   
   def getRawMessage(self, index):
      self.__checkIndex(index)
      typ, data = self.imap.fetch(index+1, '(RFC822)')
      return data[0][1]

   def deleteMessage(self, index):
      self.__checkIndex(index)
      self.imap.store(str(index+1), '+FLAGS', '\\Deleted')

   def __checkIndex(self, index):
      if index >= self.total:
         raise ValueError('index is out of bounds.')

   
   def close(self):
      self.imap.expunge()
      self.imap.close()
      self.imap.logout()
