#authentication
from getpass import getuser, getpass
import csv
import cx_Oracle as cx


# The details to access the Oracle server
user, passwd = 'bsch3398', 'bsch3398'
dsn = cx.makedsn("oracle10g.it.usyd.edu.au", 1521, "ORCL")


def connectDB():
    return cx.connect(user, passwd, dsn)


class connect:
    def __init__(self): #contains a list of field names and a list of dictionaries of each record mapped to field name
        self.record = []
        self.fieldnames = []
        self.error = ''

    def addfields(self, fields): #takes a field name as a string
        self.fieldnames.append(fields)

    def getfields(self): #returns field names as a list
        return self.fieldnames

    def addrecord(self, tuple): #takes a tuple, maps in a dictionary
        result = {}
        field = self.getfields()

        for counter in range(len(tuple)):
            result[field[counter]] = tuple[counter]

        self.record.append(result)

    def getrecords(self): #returns a list of records as dictionaries of fields mapping to entries
        return self.record

    def seterror(self, err):
        self.error = err

    def geterror(self):
        return self.error

    def clear(self): #clears previous queries from object
        self.record = []
        self.fieldnames = []

    def custom(self, sql): #takes sql statement
        try:
            conn = connectDB()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            if cursor.description:
                for fieldname in cursor.description:
                    self.addfields(fieldname[0])

                for record in cursor:
                    self.addrecord(record)

                return self.record

            return

        except cx.DatabaseError, exc:
            error, = exc.args
            self.seterror(error.message)
            return error.message

            #finally:
            #	try:
            conn.close()
        #	except UnboundLocalError:
        #		pass #might not be needed if all possible errors are done elsewhere.. currently used for incorrect login error. Error printed by the dbms already

    def create(self, table,
               values): #takes table name, dictionary of {fields : values}. Returns None or an error. Assumes values must exist.
        if not values:
            self.seterror("Dictionary must not be empty")
            return "Dictionary must not be empty"

        try:
            fields = ''
            records = ''
            for f in values:
                fields += f + ", "
                if values[f] == None:
                    records += "', '"
                else:
                    records += str(values[f]) + "', '"

            conn = connectDB()
            cursor = conn.cursor()
            #			print "INSERT INTO %s (%s) VALUES ('%s)" % (table, fields[:-2], records[:-3])

            cursor.execute("INSERT INTO %s (%s) VALUES ('%s)" % (table, fields[:-2], records[:-3]))
            conn.commit()

            return

        except cx.DatabaseError, exc:
            error, = exc.args
            self.seterror(error.message)
            return error.message

            #	finally:
            #		try:
            conn.close()

    #		except UnboundLocalError:
    #			pass

    def read(self, table,
             values): #takes table name, dictionary of {fields : values}. Returns list of dictionaries {field : value} or an error. Empty dictionary returns all
        try:
            conditions = ''
            for f in values:
                if values[f] == None:
                    conditions += f + " IS NULL AND "
                else:
                    conditions += f + " = '" + str(values[f]) + "' AND "
            if conditions:
                conditions = 'WHERE ' + conditions

            conn = connectDB()
            cursor = conn.cursor()
            #			print "SELECT * FROM %s %s" % (table, conditions[:-5])
            cursor.execute("SELECT * FROM %s %s" % (table, conditions[:-5]))
            conn.commit()
            for fieldname in cursor.description:
                self.addfields(fieldname[0])
            for record in cursor:
                self.addrecord(record)

            return self.record

        except cx.DatabaseError, exc:
            error, = exc.args
            self.seterror(error.message)
            return error.message

            #finally:
            #	try:
            conn.close()
        #	except UnboundLocalError:
        #		pass

    def update(self, table,
               values): #takes table name, dictionary of {fields : values}. Updates based on 'id' field. Returns None or an error
        #convert None to null for id...or not neccesary?
        if (not values) or (not len(values) > 1):
            self.seterror("Dictionary must include id and one other field")
            return "Dictionary must include id and one other field"
        try:
            set = ''
            id = ''
            for f in values:
                if f == 'id':
                    id = str(values[f])
                else:
                    if values[f] == None:
                        set += f + " = null, "
                    else:
                        set += f + " = '" + str(values[f]) + "', "

            if not id:
                self.seterror("Must enter an id")
                return "Must enter an id"

            #			print "UPDATE %s SET %s WHERE id = %s" % (table, set[:-2], id)
            conn = connectDB()
            cursor = conn.cursor()
            cursor.execute("UPDATE %s SET %s WHERE id = %s" % (table, set[:-2], id))
            conn.commit()

            return

        except cx.DatabaseError, exc:
            error, = exc.args
            self.seterror(error.message)
            return error.message

            #		finally:
            #			try:
            conn.close()
        #			except UnboundLocalError:
        #				pass


    def delete(self, table,
               values): #takes table name, dictionary of {fields : values}. Returns None or an error. Empty dictionary throws error
        if not values:
            self.seterror("Dictionary must not be empty")
            return "Dictionary must not be empty"
        try:
            conditions = ''
            nulls = ''
            for f in values:
                if values[f] == None:
                    nulls += f + " IS NULL AND "
                else:
                    conditions += f + " = '" + str(values[f]) + "' AND "

            if nulls:
                conditions += '    '

            conn = connectDB()
            cursor = conn.cursor()
            #			print "DELETE %s WHERE %s %s" % (table, conditions[:-5], nulls[:-5])
            cursor.execute("DELETE %s WHERE %s %s" % (table, conditions[:-5], nulls[:-5]))
            conn.commit()

            return

        except cx.DatabaseError, exc:
            error, = exc.args
            self.seterror(error.message)
            return error.message

            #		finally:
            #			try:
            conn.close()

#			except UnboundLocalError:
#				pass 


if __name__ == "__main__":
    #assumes username works for all
    user = getuser() #manually set username here
    #get password
    passwd = getpass()

    #testing
    #everything except read returns None on success
    #'null' >> None BUT NOT None >> 'null', pass shit in/out as None object
    #use connect.getrecords(), connect.getfields() to get output of previous query, connect.clear() to clear results.
    test = connect()

    collections = csv.reader(open('data/collections-v3.csv'), delimiter=',')
    for row in collections:
        collID = row[0]
        title = row[1]
        desc = row[2]

        test.create('collections', {'collectionno': collID, 'title': title, 'decs': desc, 'type': ""})

    print 'creating table and inserting values'
    print test.custom("drop table test")
    print test.custom("create table test (a varchar(5), b int, id int)")

    print 'geterror()'
    print test.custom("blah")
    if test.geterror():
        print 'error: ' + test.geterror()

    print 'creating some values'
    print test.create('test', {'a': 'test1', 'b': 6, 'id': 3})
    print test.create('test', {'a': 'empty', 'b': None})
    print test.custom("insert into test values ('test2', 6, 4)")
    print test.custom("insert into test values ('test3', 2, '' )")

    print 'testing invalid input for create'
    print test.create('test', {})

    print 'stored procedure'

    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""CREATE OR REPLACE PROCEDURE teststored(p_a IN varchar2,
						p_b IN int,
						p_id IN int
						)
						IS
						BEGIN
							INSERT INTO test
							(
							a, b, id)
							VALUES
							(p_a, p_b, p_id);
							COMMIT;
						END teststored;
					""")

    #print test.custom("""SELECT * FROM all_Procedures""")

    cursor.callproc('teststored', ['st', 1, 2])
    conn.commit()
    conn.close()

    print 'testing custom read'
    print test.custom("select * from test")
    test.clear()

    print 'testing reads'
    print test.read('test', {})
    test.clear()
    print test.read('test', {'a': 'test1'})
    test.clear()
    print test.read('test', {'b': '6'})
    test.clear()
    print 'read id = null, a = test3'
    print test.read('test', {'id': None, 'a': 'test3'})
    test.clear

    print 'updating b where id = 3'
    print test.update('test', {'a': 'upd', 'b': 2, 'id': 3})

    print 'updating to null value id = 4'
    print test.update('test', {'id': 4, 'b': None})

    print 'testing invalid input for update'
    print test.update('test', {'id': 3})
    print test.read('test', {})
    test.clear()

    print 'delete where b = 2, id = 3'
    print test.delete('test', {'b': 2, 'id': 3})

    print 'testing invalid input for delete'
    print test.delete('test', {})

    print test.read('test', {})
    test.clear()

    print 'deleting all'
    for r in test.read('test', {}): test.delete('test', r)
    test.clear()

    print test.read('test', {'a': 'blah'})
