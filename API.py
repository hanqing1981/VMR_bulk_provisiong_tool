from lxml import etree
import requests
from requests.auth import HTTPBasicAuth
import logging

logging.basicConfig(filename="systemlogs.txt",
                    format='levelname:%(levelname)s filename: %(filename)s '
                           'outputNumber: [%(lineno)d]  func: %(funcName)s output msg:  %(message)s'
                           ' - %(asctime)s', datefmt='[%d/%b/%Y %H:%M:%S]', level=logging.INFO)

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass




class Get_put_post():
    def __init__(self,ip,username,password):
        self.ip=ip
        self.username=username
        self.password=password
        self.baseurl=('https://%s/api/v1/' %self.ip)

    def get(self,subject,payload=None,quering=None):
        self.url=self.baseurl+subject
        try:
            self.content= requests.get(self.url, data=payload,verify=False, auth=HTTPBasicAuth(self.username,self.password), stream=True,
                                  params=quering)
        except Exception as error:
            raise ValueError(error)
        if self.content.status_code in [400,401]:
            all_alarms = int(self.content.status_code)
            logging.error('bad request: %s',all_alarms)
        else:
            return (etree.HTML(self.content.text))

    def put(self,subject,payload=None):
        try:
            self.url = self.baseurl + subject
            self.content = requests.put(self.url, data=payload, verify=False,
                                        auth=HTTPBasicAuth(self.username, self.password), stream=True)
            return(self.content.status_code)
        except:
            raise KeyError('incorrect key')

    def post(self,subject,payload):
        try:
            self.url = self.baseurl + subject
            self.content = requests.post(self.url, data=payload, verify=False,
                                        auth=HTTPBasicAuth(self.username, self.password), stream=True)
            return(self.content.status_code)
        except:
            raise KeyError('incorrect key')

    def deleltes(self,subject):
        try:
            self.url = self.baseurl + subject
            response=requests.delete(self.url,verify=False,
                                        auth=HTTPBasicAuth(self.username, self.password), stream=True)
            # print(response.status_code)
        except Exception as error:
            raise ValueError('failed to delete vmr')







if __name__=='__main__':
    api=Get_put_post('144.131.216.94','admin','admin')
    api.get(subject='cospaces/44194fbe-b61b-44a4-b29c-914ae261bd43')
    api.deleltes(subject='cospaces/44194fbe-b61b-44a4-b29c-914ae261bd43')

