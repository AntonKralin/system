import os
import smtplib
import shutil
import datetime
import zipfile
import logging
import re

#path to files that need copy
pathCopy = 'C:\\Backup\\'
#files that need to copy
files = ["^[\[]"]
#path to copy file
pathBackup = 'D:\\Backup\\Diff'
#copy count
copyCount = 2

SMTP_host = "10.32.0.17"
SMTP_port = "25"
SMTP_to= "logs@vitebsk.imns"
SMTP_from = "directum@nalog.gov.by"

logger = logging.getLogger("log");
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("copy.log")
handler.setLevel(logging.DEBUG)
format = logging.Formatter('%(levelname)s %(asctime)s: %(message)s')
handler.setFormatter(format)
logger.addHandler(handler)

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
    
def checkdiskspace(pathBackup, file):
    b = os.path.getsize(file)    
    disk = (os.path.splitdrive(pathBackup))[0]
    space = shutil.disk_usage(disk)
    return space.free - b

def compress_file(pathFile, pathZip):
    try:
        compressfile = zipfile.ZipFile(pathZip, mode='a', compression=zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=9 )
        compressfile.write(pathFile)
        compressfile.close()
    except Exception as exc:
        logger.error (exc)   
        
def file_rotate(path, count):
    filecount = next(os.walk(path))[2]
    if ( len(filecount) > count ):
        fullfilelist = [os.path.join(path, i ) for i in filecount]
        time_sorted_list = sorted(fullfilelist, key= os.path.getctime)
        logger.info(time_sorted_list)
        for i in range(0, len(filecount)-count, 1):
            logger.warning("remove: "+time_sorted_list[i])
            os.remove(time_sorted_list[i])


now = datetime.datetime.today().strftime("%Y%m%d")
zipname = os.path.join(pathBackup, now + ".zip")
try:
    os.remove(zipname)
    logger.warning("remove "+zipname)
except Exception:
    logger.info("no file to delete")
    
"""" remove files -1 for new file"""    
file_rotate(pathBackup, copyCount-1)

for file in files:
    f2 = next(os.walk(pathCopy))[2]
    col = 0
    for f in f2:
        match = re.search(file, f)
        if match:
            col +=1
            filepath = os.path.join(pathCopy, f)
            logger.info(filepath)
            space = checkdiskspace(pathBackup, filepath)
            if space > 0:
                os.makedirs(pathBackup,  exist_ok=True)
                logger.info(filepath + " "+ zipname)
                compress_file(filepath, zipname)
            else:
                send_email(SMTP_host, SMTP_port, SMTP_from, SMTP_to, "[ERROR] No disk size", pathBackup+" "+file)
                logger.error("[ERROR] No disk size")
                break    

    if (col == 0):
        send_email(SMTP_host, SMTP_port, SMTP_from, SMTP_to, "[ERROR] such file", pathBackup+" "+file)
        logger.error("[ERROR] such file")
        break  
else:
    send_email(SMTP_host, SMTP_port, SMTP_from, SMTP_to, "[OK] Directum", now)
    logger.info("ok")      

