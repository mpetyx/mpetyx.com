from django.http import HttpResponseForbidden
from django.template import Context, Template
from django.conf import settings

# We include the template inline since we need to be able to reliably display
# this error message, especially for the sake of developers, and there isn't any
# other way of making it available independent of what is in the settings file.

CSRF_FAILRE_TEMPLATE = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <title>403 Forbidden</title>
</head>
<body>
  <h1>403 Forbidden</h1>
  <p>CSRF verification failed. Request aborted.</p>
  {% if DEBUG %}
  <h2>Help</h2>
    {% if reason %}
    <p>Reason given for failure:</p>
    <pre>
    {{ reason }}
    </pre>
    {% endif %}

  <p>In general, this can occur when there is a genuine Cross Site Request Forgery, or when
  <a
  href='http://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ref-contrib-csrf'>Django's
  CSRF mechanism</a> has not been used correctly.  For POST forms, you need to
  ensure:</p>

  <ul>
    <li>The view function uses <a
    href='http://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext'><code>RequestContext</code></a>
    for the template, instead of <code>Context</code>.</li>

    <li>In the template, there is a <code>{% templatetag openblock %} csrf_token
    {% templatetag closeblock %}</code> template tag inside each POST form that
    targets an internal URL.</li>

    <li>If you are not using <code>CsrfViewMiddleware</code>, then you must use
    <code>csrf_protect</code> on any views that use the <code>csrf_token</code>
    template tag, as well as those that accept the POST data.</li>

  </ul>

  <p>You're seeing the help section of this page because you have <code>DEBUG =
  True</code> in your Django settings file. Change that to <code>False</code>,
  and only the initial error message will be displayed.  </p>

  <p>You can customize this page using the CSRF_FAILURE_VIEW setting.</p>
  {% else %}
  <p><small>More information is available with DEBUG=True.</small></p>

  {% endif %}
</body>
</html>
"""


def csrf_failure(request, reason=""):
    """
    Default view used when request fails CSRF protection
    """
    t = Template(CSRF_FAILRE_TEMPLATE)
    c = Context({'DEBUG': settings.DEBUG,
                 'reason': reason})
    return HttpResponseForbidden(t.render(c), mimetype='text/html')
