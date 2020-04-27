from PyInquirer import *
from boofuzz import *
from pwn import *

# FTP protocols
class ftp_protocols():
    def __init__(self):
        creds = [
                {
                    'type':'input',
                    'name':'ip',
                    'message':'Please put ip address:',
                    'default':'127.0.0.1',
                    },
                {
                    'type':'input',
                    'name':'port',
                    'message':'Please put port:',
                    'default':'21',
                    },

                {
                    'type':'input',
                    'name':'username',
                    'message':'Please input username:',
                    'default':'anonymous',
                    },
                {
                    'type':'password',
                    'name':'password',
                    'message':'Please input password:',
                    'default':'anonymous',
                    }
                ]
        creds = prompt(creds)
        #holder
        ret_fuzz_username=''
        ret_fuzz_password=''
        #session create
        session = Session(target=Target(connection=SocketConnection(creds['ip'], int(creds['port']), proto='tcp')))
        self.ftp_start_fuzz(session,creds['username'],creds['password'])

    def fuzz_username(self,username):
        s_initialize("user")
        s_string("USER")
        s_delim(" ")
        s_string(username)
        s_static("\r\n")
        return s_get("user")

    def fuzz_password(self,password):
        s_initialize("password")
        s_string("PASS")
        s_delim(" ")
        s_string(password)
        s_static("\r\n")
        return s_get("password")

    def ftp_start_fuzz(self,session,username,password):
        fuzz_param = [
                {
                    'type':'checkbox',
                    'name':'list_param',
                    'message':'Select options:',
                    'choices': [{'name':'username'},{'name':'password'}]
                    }
                ]
        fuzz_param = prompt(fuzz_param)
        if 'username' in fuzz_param['list_param']:
            self.ret_fuzz_username = self.fuzz_username(username)
            session.connect(self.ret_fuzz_username)
        if 'password' in fuzz_param['list_param']:
            self.ret_fuzz_password = self.fuzz_password(password)
            session.connect(self.ret_fuzz_username,self.ret_fuzz_password)

        session.fuzz()

# Define new protocols
prot_list = [
        {
            'type':'list',
            'name':'prot_list',
            'message':'Which do you want to Fuzz?',
            'choices':[
                    'FTP',
                    'None',
                ]
            }
        ]
             
# Define switch
def switch(prot_list):
    switcher={
            'FTP': ftp_protocols(),
            }
    return switcher.get(prot_list,'Protocols does not exists!')

answers = prompt(prot_list)
trigger = switch(answers['prot_list'])
