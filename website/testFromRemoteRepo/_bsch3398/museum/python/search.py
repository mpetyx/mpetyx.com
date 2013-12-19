#!/usr/local/bin/python

from util import *
import connect

import advsearch

import BKTree
#django for templates only
from django.template import Context

methods = ("add", "delete", "view", "update", "menu")


def results(fields, cookie):
    results = []
    bktree = []

    if fields.has_key('query'):
        keyword = fields['query'].value
        if keyword:
            find = BKTree.finder()
            find.find('BKTree', keyword, 1)
            bktree = find.getMatches()

        results = advsearch.getmatches(keyword)
    res = []

    related = None
    if results and results != str(results):
        con = connect.connect()
        max = 10

        if len(results) <= max:
            max = len(results)

        for r in results[0:max]:
            con.custom("""
			SELECT * FROM objects
			WHERE id = '%s'
			""" % ( r['ID'] ))
        res = con.getrecords()

        # we only reach here if real search term with results
        related = advsearch.getrelated(keyword.lower())
    #		related = [{'WORD': 'test'}]



    #	related=[{'WORD':'test'}]
    t = loader('results')
    #	res = {'test' : str(related)}
    c = Context({'results': res, 'related': related, 'bktree': bktree})
    #	print con.getrecords()

    print http_response(t.render(c))


def run(fields, cookie):
#	print "hi honey, i'm home"
    results(fields, cookie)


