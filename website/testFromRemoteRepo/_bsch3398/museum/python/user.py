#!/usr/local/bin/python

from util import *
import connect
import sessions

#django for templates only
from django.conf import settings
from django.template import Template, Context

methods = ("login", "logout", "add", "delete", "view", "update")


def login(fields, cookie):
    if fields.has_key('user') and fields.has_key('password'):
        user = fields['user'].value #.value
        password = fields['password'].value #.value

        db = connect.connect()
        temp = db.read('users', {'userid': user})
        #print temp # testing
        # user does exist and password matches
        if temp and temp[0]['PASSWORD'] == password:
            # create session cookie
            sid = sessions.create(user)
            newcookie = 'id=' + str(sid)
            # redirect to catalogue menu page
            t = loader('loggedin')
            c = Context({}) #TODO
            print http_response(t.render(c), newcookie)

        # no match
        else:
            t = loader('login')
            c = Context({'errors': 'Incorrect username or password. Also, I slept with your sister.'})
            print http_response(t.render(c))
        # go back to login page with error message
    else:
        t = loader('login')
        c = Context({})
        print http_response(t.render(c))


def logout(fields, cookie):
    pass


def add(fields, cookie):
    pass


def delete(fields, cookie):
    pass


def view(fields, cookie):
    pass


def update(fields, cookie):
    pass


def run(fields, cookie):
    if fields.has_key('method'):
        method = fields['method'].value
        if method in methods:
            if method == "login":
                login(fields, cookie)
            elif method == "logout":
                logout(fields, cookie)
            elif method == "add":
                add(fields, cookie)
            elif method == "delete":
                delete(fields, cookie)
            elif method == "view":
                view(fields, cookie)
            elif method == "update":
                update(fields, cookie)


if __name__ == "__main__":
    pass
