import os
import pathlib
import requests
import logging


#    Version 1
# Anton Kralin

logging.basicConfig(filename='err.log')
path_save = str(pathlib.Path("/mnt/ftp/Updates/SOS"))
print(path_save)
path_site = "http://coc.mnsupdate.mns"

def download_file(url: str, get_file: str, save_file: str):
    try:
        if os.path.isfile(get_file):
            os.remove(get_file)
        path_to_save = os.path.join(path_save, save_file)
        f = open(path_to_save, 'wb')
        ufr = requests.get(url + get_file)
        if not ufr:
            raise FileNotFoundError
        f.write(ufr.content)
        f.close()
    except Exception as exc:
        print(exc, url, get_file, save_file)
        logging.error(url + get_file)
        


crl_list = ('cas_ruc.crl', 'kuc.crl', 'mns-ca.crl', 'mns-ra.crl', 'ruc.crl', 'ruc_old.crl')
my_crl_list = ('cas_ruc.crl', 'kuc.crl', 'mns-ca.crl', 'mns-ra.crl', 'ruc.crl', 'ruc_old.crl')
cer_list = ('kuc.cer', 'mns-ca-new.cer', 'mns-ra-new.cer', 'ruc.cer', 'ruc_old.cer')
my_cer_list = ('kuc.cer', 'mns-ca.cer', 'mns-ra.cer', 'ruc.cer', 'ruc_old.cer')


for i in range(len(crl_list)):
    download_file(path_site + '/crl/', crl_list[i], my_crl_list[i])
    
    
for i in range(len(cer_list)):
    download_file(path_site + '/cert/', cer_list[i], my_cer_list[i])

