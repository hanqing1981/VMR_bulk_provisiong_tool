from API import Get_put_post
from all_profile_ids import profiles
import configparser



def get_all_profile_ids():
    cf = configparser.ConfigParser()
    cf.read("system_init_info.ini")
    server_ip = dict(cf.items("server_ip"))
    login = dict(cf.items("server_login"))
    api = Get_put_post(server_ip['dbserver'],login['username'],login['password'])
    vmr_profiles = {}
    vmr_profiles['calllegprofile'] = profiles('calllegprofiles',api)()#setupinstance & run it
    vmr_profiles['callprofile'] = profiles('callprofiles',api)()
    vmr_profiles['tenant'] = profiles('tenants', api)()
    vmr_profiles['callbrandingprofile'] = profiles('callbrandingprofiles', api)()
    return (vmr_profiles)

vmr_profiles=get_all_profile_ids()

def decorator_check_profile_ids(func): # decorator: make sure new parameters are in the correct range
    def wrapped(*args):
        vmr_features=func(*args)
        if ((int(vmr_features['Vmr Number']) in range(200000000,399999999))or (int(vmr_features['Vmr Number']) in range(700000000,899999999))) :
            pass
        else:
            raise ValueError('vmr %s is in incorrect number range' % (vmr_features['Vmr Number']))

        if vmr_features['host']:
            for k,v in vmr_features['host'].items():
                if k in vmr_profiles.keys():
                    if v not in vmr_profiles[k]:
                        raise ValueError('vmr %s host has incorrect %s value' % (vmr_features['Vmr Number'],k))
                elif k=='passcode':
                    if (1000<int(vmr_features['host']['passcode'])<9999):
                        pass
                    else:
                        raise ValueError('vmr %s has incorrect host pin value' % (vmr_features['Vmr Number']))
        if vmr_features['guest']:
            for k,v in vmr_features['guest'].items():
                if k in vmr_profiles.keys():
                    if v not in vmr_profiles[k]:
                        raise ValueError('vmr %s guest has incorrect %s value' % (vmr_features['Vmr Number'],k))
                elif 'passcode' in vmr_features['guest'].keys():
                    if int(vmr_features['guest']['passcode'])==int(vmr_features['host']['passcode']):
                        raise ValueError('vmr %s should have different guest and host passcode' %vmr_features['Vmr Number'])
                    elif (1000<int(vmr_features['guest']['passcode'])<9999):
                        pass
                    else:
                        raise ValueError('vmr %s has incorrect guest pin value' % (vmr_features['Vmr Number']))

    return (wrapped)