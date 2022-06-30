import os
import ftplib
import datetime
import logging
import smtplib
import re
from time import sleep
import shutil

#    Version 1
# Anton Kralin

ftpIp = "10.0.227.103"
#ftpIp = "10.32.0.66"
ftpUser = "imns301"
#ftpUser = "301_Kralin_A_V"
ftpPass = "imns_301"
#ftpPass = "pass"
ftpDir = "/0177"
ftpArhDir= "/0177"
RNpath = "d:\\_загрузка в РН\\"
copypath = "e:\\ARHIV\\vhod\\"
arhBat = "D:\\_WORK\\MAIL\\SendVipiska.bat"

SMTP_host = "10.32.0.17"
SMTP_port = "25"
SMTP_to= "uit@vitebsk.imns"
SMTP_from = "kazna_script@nalog.gov.by"

#setup logger
logger = logging.getLogger("log");
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("kazna.log")
handler.setLevel(logging.DEBUG)
format = logging.Formatter('%(levelname)s %(asctime)s: %(message)s')
handler.setFormatter(format)
logger.addHandler(handler)

#sent email function
def send_email(host, port, from_addr, to_addrs, subg, msg):
    BODY = "\r\n".join((
        "From: %s" % from_addr,
        "TO: %s" % to_addrs,
        "Subject: %s" % subg,
        "",
        msg
        ))
    server = smtplib.SMTP(host, port)
    server.sendmail(from_addr, to_addrs, BODY)

# function sleep to time
def wait_time(hour, minute=0, second=0):
    now = datetime.datetime.now()
    shour = datetime.datetime(now.year, now.month, now.day, hour, minute, second)
    sleeptime = shour.timestamp()-now.timestamp()
    if sleeptime >=0:
        print ("sleep to "+shour.strftime("%H:%M:%S")+": "+ str(sleeptime))
        sleep(sleeptime)
        return True
    else:
        return False

#start script
today = datetime.datetime.today()
previosDay = today-datetime.timedelta(1)
fdata = today.strftime("%d%m%y")
pdata = previosDay.strftime("%d%m%y")
os.makedirs(RNpath,  exist_ok=True)
todaypath=os.path.join(copypath,str(today.year),str(today.month),str(today.day))
os.makedirs(todaypath,  exist_ok=True)
print(today)
logger.debug(today)

#connect to ftp
ftp = ftplib.FTP(ftpIp)
def ftp_connect():
    try:
        global ftp
        ftp = ftplib.FTP(ftpIp)
        ftp.login(ftpUser, ftpPass) 
        ftp.cwd(ftpDir)
        return ftp
    except Exception as exc:
        print("Error connect")
        logger.error (exc)
        return None


def copy_file(name):
    try:
        ftp.retrbinary("RETR "+name, open(name, 'wb').write)
        shutil.copyfile(name, os.path.join(RNpath,name))
        shutil.copyfile(name, os.path.join(todaypath,name))
        os.remove(name)
        ftp.delete(name)
        print ("get file:" +name)
        logger.debug("get file: "+name)
        return True
    except Exception as exc:
        print("Error copy file")
        logger.error (exc)
        return False 

#run 9:00-9:30
r1 = False
r2 = False
r3 = False 
r4 = False
def run_check9():
    ftp = ftp_connect()
    ftp.cwd(ftpDir)
    fileList = ftp.nlst()
    print ("check 9: "+str(fileList))
    patern1 = 'P3'+pdata+'.D*'
    patern2 = 'S'+fdata+'.DBF'
    patern3 = 'M'+pdata+'.*'
    patern4 = 'M'+fdata+'.*'
    global r1
    global r2
    global r3 
    global r4     
    for file in fileList:
        if re.match(patern1, file) is not None:
            copy_file(file)
            r1 = True
        if re.match(patern2, file) is not None:
            copy_file(file)
            r2 = True
        if re.match(patern3, file) is not None or re.match(patern4,file) is not None:
            copy_file(file)
            r3 = True
    
    ftp.cwd(ftpArhDir)
    fileList = ftp.nlst()
    paternA = 'V'+fdata+'.rar'
    for file in fileList:
        if re.match(paternA, file):
            copy_file(file)
            os.system(arhBat)
            ftp.cwd(ftpDir)
            r4 = True  
     
    if r1==True and r2==True and r3==True and r4==True:              
        return True
    else:
        return False

def run_check11():
    ftp = ftp_connect()
    ftp.cwd(ftpDir)
    fileList = ftp.nlst()
    print ("check11: " +str(fileList))
    pattern11 = 'PTMP3'+fdata+'.D*'
    run_res = False
    for file in fileList:
        if re.match(pattern11, file) is not None:
            copy_file(file)
            run_res= True
    return run_res

#run in 9
while True:
    res_wait = wait_time(9)
    if res_wait == False:
        break
    now = datetime.datetime.now()    
    if now.hour == 9 and now.minute <= 30:
        get_file9 = run_check9()
        if get_file9:
            break
    else:
        print("No such file: P3"+fdata+".D01-02")  
        logger.error("No such file: P3"+fdata+".D01-02") 
        send_email(SMTP_host, SMTP_port, SMTP_from, SMTP_to, "[WARN]", "No such file: P3"+fdata+".D01-02")
        break 
    sleep(60)

wait_time(10, 0)
  
#run 11-17
timeHour = 10
while True:
    now = datetime.datetime.now()
    if now.hour <=18 and timeHour<=18:
        run_check11()
        run_check9()
        wait_time(timeHour, 0)
    else:
        print ("Stop: "+now.strftime("%d.%m.%Y %H:%M:%S"))
        break    
    timeHour = timeHour+1   