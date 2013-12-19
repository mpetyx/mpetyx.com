# enable CGI debugging - remove before production!!!
import cgitb; cgitb.enable()

import cx_Oracle

HOST = 'oracle10g.it.usyd.edu.au'
PORT = 1521
SERVICE_ID = 'ORCL'
USERNAME = 'bsch3398'
PASSWORD = 'bsch3398'

dsn = cx_Oracle.makedsn(HOST, PORT, SERVICE_ID)
conn = cx_Oracle.connect(USERNAME, PASSWORD, dsn)

print 'Content-Type: text/html'
print
print 'cx_Oracle has been imported and has connected! :)'

