import connect as c

ignore = ['a', 'the', 'and']


def getmatches(
        keyword): #takes in a string containing the searched keywords seperated by spaces, returns list of dictionaries with the ID primary key in order of relevance(count of matches)
    #do a query based on the return names  (its sorted in order of relevance), limit by the number specified in adv question.
    #check if ascii > 64?? getrelated too?
    words = keyword.split(' ')

    for w in ignore:
        if w in words:
            words.remove(w)

        #	print words
    if len(words) == 0:
        return []
    matches = c.connect()
    select = """SELECT * FROM objects WHERE"""
    query = """SELECT id, count(*) FROM ( """
    for word in words:
        word = '%%%s%%' % (word.strip())

        query += """
					%s	
					ID LIKE '%s'
					UNION ALL
					%s
					title LIKE '%s'
					UNION ALL
					%s
					description LIKE '%s'
					UNION ALL
					SELECT q.id, title, q.description, marks, productiondate, url, height, width, depth, diameter, weight FROM
					objects q INNER JOIN 
					objectlocation w ON (q.id = w.recordid) INNER JOIN
					locations l ON (w.locationid = l.id)
					WHERE l.description LIKE '%s'	
					UNION ALL""" % (select, word, select, word, select, word, word)

    #%s
    #location LIKE '%s'
    #UNION ALL"
    query = query[:-13] + """ )
					GROUP BY id
					ORDER BY count(*) DESC 
					"""
    #	print query
    return matches.custom(query)


def getrelated(keyword): #takes in keyword, returns top 10 related to names of searches
    #return [{'WORD': 'test'}]
    words = keyword.split(' ')

    for w in ignore:
        if w in words:
            words.remove(w)

        #	print words

    related = c.connect()
    #change table name if needed
    select = """
				SELECT id, count(id) as c FROM searchterms
				WHERE"""
    selectminus = """SELECT id, word FROM searchterms
				WHERE"""
    inner = "INNER JOIN searchterms"
    query = """SELECT word FROM
	(SELECT s.id, s.word FROM (
		SELECT id, SUM(c) FROM (
			"""
    minus = """	("""

    for word in words:
        word.strip()

        query += """
					%s word = '%s'
				GROUP BY ID
				UNION ALL
					""" % (select, word)

        minus += """
				%s word = '%s'
					UNION""" % (selectminus, word)

    minus = minus[:-5] + """
		)"""

    query = query[:-15] + """
	) 
	WHERE rownum <= 10
	GROUP BY id 
	ORDER BY sum(c) DESC
	) a
	%s s
	ON (s.id = a.id)
	MINUS
	%s
	)
	WHERE rownum <= 5
	GROUP BY word
	ORDER BY count(word) DESC
	""" % (inner, minus)

    #	print query

    return related.custom(query)


if __name__ == "__main__":
#	c.user = c.getuser()
#	c.passwd = c.getpass()

    test = c.connect()
    """
    print 'creating tables'
    test.custom("drop table testsearch")
    test.custom("CREATE TABLE testsearch (id integer, title varchar(255), description varchar(255), location varchar(255))")

    test.create('testsearch', {'id' : 1, 'title' : 'test1', 'description' : 'this is test 1', 'location' : 'testloc1'})
    test.create('testsearch', {'id' : 2, 'title' : 'test2', 'description' : 'this is test 2', 'location' : 'testloc2'})
    test.create('testsearch', {'id' : 3, 'title' : 'test3', 'description' : 'this is test 3', 'location' : 'testloc3'})
    test.create('testsearch', {'id' : 4, 'title' : 'test4', 'description' : 'this is test 4', 'location' : 'testloc4'})
    test.create('testsearch', {'id' : 42, 'title' : 'a', 'description' : 'and', 'location' : 'the'})
    print test.read('testsearch', {})
    test.clear()

    test.custom("drop table searchhistory")
    test.custom("CREATE TABLE searchhistory (name VARCHAR(255), id INTEGER)")

    test.create('searchhistory', {'name' : 'test1', 'id' : 1})
    test.create('searchhistory', {'name' : 'test1', 'id' : 2})
    test.create('searchhistory', {'name' : 'test2', 'id' : 1})
    test.create('searchhistory', {'name' : 'test1', 'id' : 1})
    test.create('searchhistory', {'name' : 'test3', 'id' : 1})
    test.create('searchhistory', {'name' : 'test1', 'id' : 1})
    test.create('searchhistory', {'name' : 'test4', 'id' : 2})
    test.create('searchhistory', {'name' : 'test4', 'id' : 1})
    test.create('searchhistory', {'name' : 'test4', 'id' : 10})
    test.create('searchhistory', {'name' : 'test4link', 'id' : 10})

    test.create('searchhistory', {'name' : 'arb', 'id' : 100})

    test.read('searchhistory', {})


    print 'testing getmatches - test1'
    print getmatches('test1')

    print '-test 2'
    print getmatches('test2')

    print '-test'
    print getmatches('test')

    print '-test test1'
    print getmatches('test test1')

    print 'test exclude common words - a and thee'
    print getmatches('a and thee')

    print '-a test the'
    print getmatches('a test the')

    print 'testing injection'
    print getmatches(")Drop tables;")
    print test.read('testsearch', {})

    print 'testing related terms - test1'
    print getrelated('test1')

    print '-test1 test4'
    print getrelated('test1 test4')

    print '-43'
    print getrelated('43')
    """

    print 'testing getmatches'
    print getmatches('sydney')
    print getmatches('cat syd')
    print getmatches('sup')
    print 'the'
    print getmatches('the')
    print 'testing related'
    print getrelated('sydney')

