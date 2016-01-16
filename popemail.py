import poplib
import re

from baseemail import BaseEmail

class PopEmail(BaseEmail):
   def __init__(self, user, passwd, server, port):
      self.user = user
      self.passwd = passwd
      self.server = server
      self.port = port

   def connect(self):
      if self.server is None or self.port is None:
         raise ValueError('Server or port is not set')
      print "connecting..."
      self.pop = poplib.POP3_SSL(self.server, self.port)
      try:
         self.pop.user(self.user)
         self.pop.pass_(self.passwd)
      except ValueError as e:
         raise ValueError('username or password is incorrect.')
      else:
         print "connected."
         print "There are %i messages" % (len(self.pop.list()[1]))
   
   def getRawMessage(self, index):
      self.__checkIndex(index)
      return '\n'.join(self.pop.retr(index+1)[1])

   def deleteMessage(self, index):
      self.__checkIndex(index)
      print(self.pop.list()[1][index])
      self.pop.dele(index+1)
      
   def __checkIndex(self, index):
      if index >= len(self.pop.list()[1]):
         raise ValueError('index is out of bounds.')

   def close(self):
      self.pop.quit()
