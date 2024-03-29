import unittest

from django.contrib.messages.middleware import MessageMiddleware

from django import http


class MiddlewareTest(unittest.TestCase):
    def setUp(self):
        self.middleware = MessageMiddleware()

    def test_response_without_messages(self):
        """
        Makes sure that the response middleware is tolerant of messages not
        existing on request.
        """
        request = http.HttpRequest()
        response = http.HttpResponse()
        self.middleware.process_response(request, response)
