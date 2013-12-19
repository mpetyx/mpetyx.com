import connect as c
import distance
#import sys #change this if more search terms added
import csv #temporary

#c.user = c.getuser()
#c.passwd = c.getpass()
node = c.connect()

#sys.setrecursionlimit(10000)

def addNode(table, item): #takes string adds to BK Tree structure in oracle, doing alot of searches is more efficient then implementing a search algorithm imo
	node.clear()
	
	if node.read('BKTree', {'name' : item}):
		return

	head = node.custom("""SELECT * 
					FROM %s
					WHERE Distance = 0
					""" % (table))
#	print head

	if head:
#		print node.read('BKTree', {'parent' : head[0]['NAME'], 'distance' : distance.getDistance(head[0]['NAME'], item)})
		#node.clear()
		return __addNode(table, head[0]['NAME'], item)

	else:

		return node.create(table, {'name' : item, 'parent' : None, 'distance' : 0})


def __addNode(table, root, item):

	node.clear()
	head = node.read(table, {'parent' : root, 'distance' : distance.getDistance(root, item)})
#	print root
	if head:
		
		return __addNode(table, head[0]['NAME'], item)
	
	else:

		return node.create(table, {'name' : item, 'parent' : root, 'distance' : distance.getDistance(root, item)})

class finder:
	def __init__(self):
		self.matches = []

	def find(self, table, item, threshold): #takes in item to compare against and a threshold integer	
		
		node.clear()
		head = node.custom("""SELECT *
						FROM %s
						WHERE distance = 0
						""" % (table))
		node.clear()
		if distance.getDistance(item, head[0]['NAME']) <= threshold:
			self.matches.append(head[0]['NAME'])
#		print head
		results = node.custom("""SELECT *
						FROM %s
						WHERE parent = '%s' AND
						distance >= %d AND
						distance <= %d
						""" %	(
								table,
								head[0]['NAME'], 
								distance.getDistance(item, head[0]['NAME']) - threshold, 
								distance.getDistance(item, head[0]['NAME']) + threshold
								)
							)

#		print results
		for record in results:
#			print record
			self.__find(table, record['NAME'], item, threshold)

		return self.matches
	
	def __find(self, table, root, item, threshold):
		if distance.getDistance(root, item) <= threshold:
			self.matches.append(root)
		
		node.clear()
		results = node.custom("""SELECT *
						FROM %s
						WHERE parent = '%s' AND
						distance >= %d AND
						distance <= %d
						""" %	(
								table,
								root, 
								distance.getDistance(item, root) - threshold, 
								distance.getDistance(item, root) + threshold
								)
							)
#		print results	
		for record in results:
			self.__find(table, record['NAME'], item, threshold)
	
	def getMatches(self):
		return self.matches
	
	def clear(self):
		self.matches = []

if __name__ == "__main__":
	
	c.user = c.getuser()
	c.passwd = c.getpass()
#	print 'creating table'


#	node.custom("drop table bktree")
#	node.custom("""create table bktree (
#						name	VARCHAR(255),
#						parent	VARCHAR(255),
#						distance	INTEGER
#					)""")
	
	"""
	print 'testing add'
	print addNode('bktree', 'test')
	print addNode('bktree', 'test1')
	print addNode('bktree', 'tester')
	print addNode('bktree', '2test')
	print addNode('bktree', 'test3')
	print addNode('bktree', '3test')
	print addNode('bktree', '3test')
	node.clear()
	print node.read('BKTree', {})

	test = finder()
	print 'testing find'
	print test.find('bktree', 'test', 1)
	test.clear()

	print 'finding 3test, threshold 1'
	print test.find('bktree', '3test', 1)
	test.clear()

	print 'finding 3test, threshold 10'
	print test.find('bktree', '3test' , 10)
	test.clear()

	print 'finding test10 threshold 1'
	print test.find('bktree', 'test10', 1)
	test.clear()
	"""
######################################################
#	print "creating table searchterms"	
#
#	node.custom("drop tables searchterms")
#	node.custom("""create table searchterms (
#						ID INTEGER,
#						Word VARCHAR(255)
#				)""")
#	collections = csv.reader(open('data/condensedsearch.csv'), delimiter = '\t')
	"""
	skip = True
	for row in collections:

		temp = []	
		
		for entry in row:
		
			if entry:				
				temp.append(entry)
		if skip:

			skip = False
		
		else:
			
			for e in temp[:-1]:
				addNode('bktree', e)
				node.create('searchterms', {'word' : e, 'id' : temp[-1]})

#		print 'search terms ' + str(temp[:-1]) + '- clicked ' + str(temp[-1])
	"""	
#######################################################

	print node.read('BKTree', {})
	node.clear()
	
	test = finder()
	print 'finding sydney, syd'

	print test.find('bktree', 'sydney', 1)
	test.clear()

	print test.find('bktree', 'sydne', 1)
	test.clear()
	
	test = c.connect()

	print test.custom("select * from searchterms where rownum < 26")
	node.clear()

