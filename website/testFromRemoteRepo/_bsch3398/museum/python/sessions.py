import datetime

import connect as c


now = datetime.datetime.now()


class session:
    def __init__(self, sessionid):
        self.sessionid = sessionid
        self.exists = False
        self.expired = True
        self.userid = ''

    def setexists(self, exist):
        self.exists = exist

    def setexpired(self, expire):
        self.expired = expire

    def setuser(self, userid):
        self.userid = userid

    def info(self):
        return {'sessionid': self.sessionid, 'userid': self.userid, 'expired': self.expired, 'exists': self.exists}


def create(userid): #might need to change field names later


    conn = c.connect()
    temp = conn.read('sessions', {'userid': userid})
    #	print temp
    if temp:
        conn.delete('sessions', {'userid': userid})

    conn.clear()

    newid = conn.custom("""
		SELECT MAX(id) as id
		FROM sessions
		""")[0]['ID']

    if newid:
        newid += 1
    else:
        newid = 1

    #change format of the expiration if needed here #%b
    #	if now.day + 2  > 30 :
    #		day = -1
    #	expdate = str((day + 2)) + now.strftime("-%b-") + str(now.year)# + " " + str(now.second) + ":" + str(now.minute) + ":" + str(now.hour)
    #	print expdate
    #expdate = "%d-%s-%d %d:%d" % (now.day + 2, now.strftime("%b"), now.year, now.minute, now.hour)
    #	conn.create('sessions', {'userid' : userid, 'id' : newid, 'expired' : expdate})
    conn.create('sessions', {'userid': userid, 'id': newid})

    return newid


def getuser(sessionid):
    record = c.connect()
    record.read('sessions', {'id': sessionid})
    s = session(sessionid)

    if record.getrecords():
        s.setexists(True)
        s.setuser(record.getrecords()[0]['USERID'])

    #check if expired - change format here
    #		exptime = str(record.getrecords()[0]['EXPIRED']).replace('-', ' ').split(' ') #replace ':'
    #		time = now.strftime("%Y %m %d").split(' ')# %s:%M:%H
    #		for t in range(3): #extend to 6 to add finer granularity
    #			if exptime[t] > time[t]:
    #				s.setexpired(False)
    #				break

    return s.info()


if __name__ == "__main__":
#	c.user = c.getuser()
#	c.passwd = c.getpass()
    test = c.connect()
    print 'creating table'
    print test.custom("DROP TABLE sessions")
    print test.custom("CREATE TABLE sessions (userid int, id int PRIMARY KEY, expired date)")

    print 'creating new sessions'
    print create(42)
    print create(210)
    print create(320)
    print create('blah')
    print test.read('sessions', {})
    test.clear()

    print 'get user from id = 3'
    print getuser(3)
    print 'testing if session does not exists'
    print getuser(100)
    print 'testing invalid input'
    print getuser(None)
