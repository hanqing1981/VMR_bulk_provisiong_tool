import logging
from API import Get_put_post

PAGEMAX=10
# api=Get_put_post('144.131.216.94','admin','admin')
class profiles(object):
    def __init__(self,profiletype,api):
        self.profiletype=profiletype
        self.api=api

    def __call__(self):
        profileids=[]
        self.profile=self.profiletype[:-1]
        Data = self.api.get(subject=self.profiletype)
        if Data is not None:
            self.total = Data.xpath('//%s/@total' %self.profiletype)
            self.total=int(self.total[0])
            # logging.info('%s' %self.total[0])
            if ((self.total/10)<=1):
                self.pages=1
                # print(self.pages)
            else:
                if ((self.total%10)>0):
                    self.pages=(self.total//10)+1
                    # print(self.total%10)
                else:
                    self.pages = (self.total // 10)
                    # print(self.pages)


        for i in range(self.pages):
            content = self.api.get(subject=self.profiletype,quering={'offset': i * PAGEMAX, 'limit': PAGEMAX})
            profileids.extend(content.xpath('//@id'))
        return(profileids)




if __name__=='__main__':
    profiles=profiles('callbrandingprofiles',api)
    haha=profiles()
    print(haha)