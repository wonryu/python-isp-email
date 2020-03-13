class BaseEmail:
   def connect(self):
      raise NotImplementedError("Subclass must implement abstract method ") 

   def getRawMessage(self, index):
      raise NotImplementedError("Subclass must implement abstract method ")

   def deleteMessage(self, index):
      raise NotImplementedError("Subclass must implement abstract method ")

   def close(self):
      raise NotImplementedError("Subclass must implement abstract method ")

