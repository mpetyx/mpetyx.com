from django.core.exceptions import MiddlewareNotUsed
from django.utils.http import http_date


class ConditionalGetMiddleware(object):
    """
    Handles conditional GET operations. If the response has a ETag or
    Last-Modified header, and the request has If-None-Match or
    If-Modified-Since, the response is replaced by an HttpNotModified.

    Also sets the Date and Content-Length response-headers.
    """

    def process_response(self, request, response):
        response['Date'] = http_date()
        if not response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))

        if response.has_header('ETag'):
            if_none_match = request.META.get('HTTP_IF_NONE_MATCH', None)
            if if_none_match == response['ETag']:
                # Setting the status is enough here. The response handling path
                # automatically removes content for this status code (in
                # http.conditional_content_removal()).
                response.status_code = 304

        if response.has_header('Last-Modified'):
            if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE', None)
            if if_modified_since == response['Last-Modified']:
                # Setting the status code is enough here (same reasons as
                # above).
                response.status_code = 304

        return response


class SetRemoteAddrFromForwardedFor(object):
    """
    This middleware has been removed; see the Django 1.1 release notes for
    details.
    
    It previously set REMOTE_ADDR based on HTTP_X_FORWARDED_FOR. However, after
    investiagtion, it turns out this is impossible to do in a general manner:
    different proxies treat the X-Forwarded-For header differently. Thus, a
    built-in middleware can lead to application-level security problems, and so
    this was removed in Django 1.1
    
    """

    def __init__(self):
        import warnings

        warnings.warn("SetRemoteAddrFromForwardedFor has been removed. "
                      "See the Django 1.1 release notes for details.",
                      category=DeprecationWarning)
        raise MiddlewareNotUsed()