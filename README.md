# python-isp-email
Send and receive from aol, hotmail and yahoo account.

Read email message

from ispemail import IspEmail

e = IspEmail("accountname@aol.com", "password");
e.connect()
message = e.getMessage(0)
e.close()

Send email message

e = IspEmail("accoutname@aol.com", "password");
e.connect()
e.sendMessage("receiver@gmail.com", "subject", "content")
e.close()
