from addNewObject import stored
#authentication
from getpass import getuser, getpass
import cx_Oracle as cx
import csv
import BKTree #add BKTree into imports 

# The details to access the Oracle server
user, passwd = None, None
dsn = cx.makedsn("oracle10g.it.usyd.edu.au", 1521, "ORCL")
user = getuser() #manually set username here
#get password
passwd = getpass()
#user, passwd = 'bsch3398', 'bsch3398'
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

        finally:
            try:
                conn.close()
            except UnboundLocalError:
                pass #might not be needed if all possible errors are done elsewhere.. currently used for incorrect login error. Error printed by the dbms already

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

        finally:
            try:
                conn.close()
            except UnboundLocalError:
                pass

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

        finally:
            try:
                conn.close()
            except UnboundLocalError:
                pass

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

        finally:
            try:
                conn.close()
            except UnboundLocalError:
                pass


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

        finally:
            try:
                conn.close()
            except UnboundLocalError:
                pass


if __name__ == "__main__":
    #assumes username works for all


    #testing
    #everything except read returns None on success
    #'null' >> None BUT NOT None >> 'null', pass shit in/out as None object
    #use connect.getrecords(), connect.getfields() to get output of previous query, connect.clear() to clear results.
    test = connect()

    print "Creating table: users"
    test.custom("drop table users cascade constraints")
    test.custom("""create table users (
						userid		varchar(255) primary key,
						password	varchar(255),
						field		varchar(500)
					)""")

    print "creating 4 users"
    test.create('users', {'userid': 'dave', 'password': 'dave', 'field': 'owning'})
    test.create('users', {'userid': 'adave', 'password': 'adavce', 'field': 'getting owned by dave'})
    test.create('users', {'userid': 'ben', 'password': 'ben',
                          'field': 'since he was young he has always been infatuated with oracle'})
    test.create('users', {'userid': 'uwe', 'password': 'iliekjewishfood', 'field': 'photography'})

    print "Creating table: sessions"
    test.custom("drop table sessions")
    test.custom("""create table sessions (
						userid			varchar(255) references users (userid),
						id				integer	primary key
					)""")

    print "Creating table: collections"
    print test.custom("drop table collections cascade constraints")
    test.custom("drop sequence seq_coll_id")
    test.custom("create sequence seq_coll_id")
    print test.custom("""create table collections (
						ID integer PRIMARY KEY,
						Regnum	varchar(255),
						title varchar(255),
						type varchar(255),
						description varchar(255)
						)""")
    test.custom("drop trigger coll_id_trigger")
    test.custom("""create trigger coll_id_trigger
						before insert on collections
						for each row
						begin
							select seq_coll_id.nextval into :new.id from dual;
						end;""")

    print "Creating table: usercollections"
    test.custom("drop table usercollections")#deleted references on userid
    print test.custom("""create table usercollections (
						userid			varchar(255),
						ID	integer	REFERENCES collections (ID)
					)""")
    print "Creating sample user's collections"
    print test.create('usercollections', {'userid': 'ben', 'id': '2'})
    test.create('usercollections', {'userid': 'ben', 'id': '3'})

    collections = csv.reader(open('data/collections-v3.csv'), delimiter=',')
    first = True

    for row in collections:
        if first:
            first = False
        else:
            collID = row[0]
            title = row[1]
            desc = row[2]

            test.create('collections', {'regnum': collID, 'title': title, 'description': desc, 'type': ""})

    print "Creating table: locations"
    test.custom("drop table locations")
    test.custom("""create table locations (
						ID	VARCHAR(255) PRIMARY KEY,
						Description	VARCHAR(255)
					)""")

    locations = csv.reader(open('data/locations-v3.csv'), delimiter=',')
    first = True

    for row in locations:
        if first:
            first = False
        else:
            location = row[0]
            description = row[1]

            test.create('locations', {'id': location, 'Description': description})

    def insertprovenance(connection, table, recordid, provenance): # takes an array
        #for line in provenance:
        #line = line.split('|')
        line = provenance.split('|')
        for part in line:
            part = part.split(';')
            if len(part) > 1:
                print part
                people = part[0].strip()
                if len(part) == 2:
                    time = part[1].strip()
                    place = ""
                else:
                    place = part[1].strip()
                    time = part[2].strip()
                connection.create(table + "provenance", {'people': people, 'location': place, 'time': time})
                connection.create("object" + table, {'recordid': recordid})

    print "Creating table: objects"
    test.custom("drop table objects cascade constraints")
    test.custom("""create table objects (
						ID integer primary key,
						title varchar(255),
						description varchar(3999),
						marks varchar(1000),
						productiondate varchar(255),
						url varchar(255),
						height varchar(255),
						width varchar(255),
						depth varchar(255),
	                    diameter varchar(255),
	                    weight varchar(255)
	                    )""")

    print "Creating table: objectcollections"
    test.custom("drop table objectcollections")
    test.custom("""create table objectcollections (
						CollectionID	VARCHAR(255)	REFERENCES collections (ID),
						RecordID		INTEGER			REFERENCES objects (ID)
					)""")

    print "Creating table: objectlocation"
    test.custom("drop table objectlocation")
    test.custom("""create table objectlocation (
						RecordID		INTEGER			REFERENCES objects (ID),
						LocationID		VARCHAR(50)		REFERENCES locations (ID)
					)""")

    print "Creating table: productionprovenanace"
    test.custom("drop table productionprovenance")
    test.custom("drop sequence seq_prod_id")
    test.custom("create sequence seq_prod_id")
    test.custom("""create table productionprovenance (
						ID			INTEGER			PRIMARY KEY,
						People		VARCHAR(255),
						Location	VARCHAR(255),
						Time		VARCHAR(255)
					)""")
    test.custom("drop trigger prod_id_trigger")
    test.custom("""create trigger prod_id_trigger
						before insert on productionprovenance
						for each row
						begin
							select seq_prod_id.nextval into :new.id from dual;
						end;""")

    print "creating table: objectproduction"
    test.custom("drop table objectproduction")
    print test.custom("""create table objectproduction (
						RecordID		Integer		REFERENCES Objects (ID),
						ProvenanceID	Integer		REFERENCES Productionprovenance (ID),
					)""")
    # note that the following trigger assumes an insert into objproduction
    # will always occur immediately after an insert into productionprovenance
    test.custom("drop trigger obj_prod_trigger")
    test.custom("""create trigger obj_prod_trigger
						before insert on objectproduction
						for each row
						begin
							select seq_prod_id.currval into :new.provenanceid from dual;
						end""")

    print "creating table historicprovenance"
    test.custom("drop table historicprovenance")
    test.custom("create or replace sequence historic_id_seq start with 1 increment by 1")
    test.custom("""create table historicprovenance (
						ID			INTEGER			PRIMARY KEY,
						People		VARCHAR(255),
						Location	VARCHAR(255),
						Time		VARCHAR(255)
					)""")
    test.custom("drop trigger hist_id_trigger")
    test.custom("""create trigger hist_id_trigger
						before insert on historicprovenance
						for each row
						begin
							select seq_hist_id.nextval into :new.id from dual;
						end;""")

    print "creating table: objecthistoric"
    test.custom("drop table objectHistoric")
    test.custom("""create table objectHistoric (
						RecordID	INTEGER	REFERENCES Objects (ID),
						HistoricID	INTEGER REFERENCES historicprovenance (ID)
					)""")
    # note that the following trigger assumes an insert into objhistoric
    # will always occur immediately after an insert into historicprovenance
    test.custom("drop trigger obj_hist_trigger")
    test.custom("""create trigger obj_hist_trigger
						before insert on objecthistoric
						for each row
						begin
							select seq_prod_id.currval into :new.historicid from dual;
						end""")

    print "Creating table: category"
    test.custom("drop table category")
    print test.custom("""create table category (
						ID			VARCHAR(255),
						RecordID	INTEGER
					)""")

    objects = csv.reader(open('data/objects-v3.csv'), delimiter=',')
    first = True

    #print 'inserting into objects using stored procedure'

    test.custom(stored)

    print "Inserting objects..."
    for row in objects:
        if first:
            first = False
        else:
            recordid = row[0]
            title = row[1]
            regnum = row[2]  #collections
            desc = row[3]
            marks = row[4]
            productiondate = row[5]
            url = row[9]
            height = row[10]
            width = row[11]
            depth = row[12]
            diameter = row[13]
            weight = row[14]
            location = row[15]
            #####
            ## adave's shit?
            #
            #	conn = connectDB()
            #	cursor = conn.cursor()
            #	print 	row[0:5] + row[9:14]
            #	cursor.callproc('addNewObject', row[0:6] + row[9:15])
            #
            ## end ~adave's shit~
            #####

            # provenance
            provenance = [row[6], row[7]]
            prodprov = provenance[0]
            histprov = provenance[1]

            insertprovenance(test, "production", recordid, prodprov)
            insertprovenance(test, "historic", recordid, histprov)

            #for provenance in prodprov:
            #	test.create('productionprovenance', {'id': ,'people':provenance[0],'location':provenance[1],'time':provenance[2]})
            #	test.create('objectproduction', {'recordid':recordid,'provenanceid':})

            #for provenance in histprov:
            #	test.create('historicprovenance', {'id': ,'people':provenance[0],'location':provenance[1],'time':provenance[2]})
            #	test.create('objectHistoric', {'recordid':recordid,'provenanceid':})

            # categories
            category = row[8].split('|')
            for cat in category:
                test.create('category', {'id': cat, 'recordid': recordid})

            # unnecessary?
            #	license_info = row[16]

            test.create('objects', {'id': recordid, 'title': title, 'description': desc, 'marks': marks,
                                    'productiondate': productiondate, 'url': url, 'height': height, 'width': width,
                                    'depth': depth, 'diameter': diameter, 'weight': weight})
            test.create('objectcollections', {'collectionid': regnum, 'recordid': recordid})
            test.create('objectlocation', {'recordid': recordid, 'locationid': location})

        ### on adave's request this has been commented out
        #	print "creating table searchterms"
        #
        #	test.custom("drop tables searchterms")
        #	test.custom("""create table searchterms (
        #						ID INTEGER,
        #						Word VARCHAR(255)
        #				)""")
        #
        #
        #	test.custom("drop table bktree")
        #	test.custom("""create table bktree (
        #						name	VARCHAR(255),
        #						parent	VARCHAR(255),
        #						distance	INTEGER
        #					)""")
        #NOTE THIS TAKES AT LEAST 1 MINUTE to run - run this once then comment it out to test the rest
        #	collections = csv.reader(open('data/condensedsearch.csv'), delimiter = '\t')
        #
        #	skip = True
        #	for row in collections:

        #		temp = []

        #		for entry in row:
        #			if entry:
        #				temp.append(entry)
        #		if skip:
        #			skip = False

        #else:
        #			for e in temp[:-1]:

        #				BKTree.addNode('bktree', e)
        #				test.create('searchterms', {'word' : e, 'id' : temp[-1]})




        #	print 'creating table bktree'
        #	test.custom("drop table bktree")
        #	test.custom("""create table bktree (
        #						name	VARCHAR(255),
        #						parent	VARCHAR(255),
        #						distance	INTEGER
        #					)""")

        #	cusor.commit()
        #	cursor.close()


        #use something like this
        #import connection
        #insert = connection.connection()
        #insert.create('table', {RecordID : recordid})
        #returns None or prints dbms error use insert.geterror() to reprint
#but we were going to use a stored procedure to create, so it can be reused as recommended
#also rename the schema primary key's ids to just 'id'
