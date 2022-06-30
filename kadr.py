import pyodbc

#    Version 1
# Anton Kralin

conn_str = (
    r'Driver=SQL Server;'
    r'Server=kadrs-minfin\sqlexpress,58725;'
    r'Database=KDRMF_MNS;'
    r'Trusted_connection=yes;'
    )

cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()
#cursor.execute("Select dbo.tblPeople.Surname, dbo.tblPeople.room from dbo.tblPeople")
cursor.execute("Select * from dbo.tblPeople")
while True:
    row = cursor.fetchone()
    if not row:
        break
    print(row)
cnxn.close()