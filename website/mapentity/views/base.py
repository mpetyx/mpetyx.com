# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import logging
import traceback
from datetime import datetime
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseServerError)
from django.views.defaults import page_not_found
from django.views.generic.base import TemplateView
from django.views import static
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, Context, loader

from .. import app_settings, _MAP_STYLES
from ..helpers import convertit_url, capture_image, download_to_stream
from ..urlizor import url_layer
from .mixins import JSONResponseMixin


logger = logging.getLogger(__name__)


def handler404(request, template_name='mapentity/404.html'):
    return page_not_found(request, template_name)


def handler500(request, template_name='mapentity/500.html'):
    """
    500 error handler which tries to use a RequestContext - unless an error
    is raised, in which a normal Context is used with just the request
    available.

    Templates: `500.html`
    Context: None
    """
    # Try returning using a RequestContext
    try:
        context = RequestContext(request)
    except:
        logger.warn('Error getting RequestContext for ServerError page.')
        context = Context({'request': request})
    e, name, tb = sys.exc_info()
    context['exception'] = repr(name)
    context['stack'] = "\n".join(traceback.format_tb(tb))
    t = loader.get_template(template_name)
    return HttpResponseServerError(t.render(context))


@login_required()
def serve_secure_media(request, path):
    """
    Serve media/ for authenticated users only, since it can contain sensitive
    information (uploaded documents, map screenshots, ...)
    """
    if settings.DEBUG:
        return static.serve(request, path, settings.MEDIA_ROOT)

    response = HttpResponse()
    response['X-Accel-Redirect'] = settings.MEDIA_URL_SECURE + path
    return response


class JSSettings(JSONResponseMixin, TemplateView):
    """
    Javascript settings, in JSON format.
    Likely to be overriden. Contains only necessary stuff
    for mapentity.
    """
    def get_context_data(self):
        dictsettings = {}
        dictsettings['debug'] = settings.DEBUG
        dictsettings['map'] = dict(
            extent=getattr(settings, 'LEAFLET_CONFIG', {}).get('SPATIAL_EXTENT'),
            styles=_MAP_STYLES,
        )

        # URLs
        root_url = app_settings['ROOT_URL']
        root_url = root_url if root_url.endswith('/') else root_url + '/'
        dictsettings['urls'] = {}
        dictsettings['urls']['root'] = root_url

        class ModelName:
            pass

        dictsettings['urls']['layer'] = root_url + url_layer(ModelName)[1:-1]

        # Useful for JS calendars
        dictsettings['date_format'] = settings.DATE_INPUT_FORMATS[0].replace('%Y', 'yyyy').replace('%m', 'mm').replace('%d', 'dd')
        # Languages
        dictsettings['languages'] = dict(available=dict(app_settings['LANGUAGES']),
                                         default=app_settings['LANGUAGE_CODE'])
        return dictsettings


@csrf_exempt
@login_required
def map_screenshot(request):
    """
    This view allows to take screenshots, via a django-screamshot service, of
    the map **currently viewed by the user**.

    - A context full of information is built on client-side and posted here.
    - We reproduce this context, via headless browser, and take a capture
    - We return the resulting image as attachment.

    This seems overkill ? Please look around and find a better way.
    """
    try:
        printcontext = request.POST['printcontext']
        assert len(printcontext) < 512, "Print context is way too big."

        # Prepare context, extract and add infos
        context = json.loads(printcontext)
        map_url = context.pop('url').split('?', 1)[0]
        context['print'] = True
        printcontext = json.dumps(context)
        contextencoded = urllib2.quote(printcontext)
        map_url += '?context=%s' % contextencoded
        logger.debug("Capture %s" % map_url)

        # Capture image and return it
        width = context.get('viewport', {}).get('width')
        height = context.get('viewport', {}).get('height')

        response = HttpResponse()
        capture_image(map_url, response, width=width, height=height, selector='#mainmap')
        response['Content-Disposition'] = 'attachment; filename=%s.png' % datetime.now().strftime('%Y%m%d-%H%M%S')
        return response

    except Exception, e:
        logger.exception(e)
        return HttpResponseBadRequest(e)


@require_http_methods(["GET"])
@login_required
def convert(request):
    """ A stupid proxy to Convertit.

    Was done by Nginx before, but this is the first step of
    authenticated document conversion.
    """
    source = request.GET.get('url')
    if source is None:
        return HttpResponseBadRequest('url parameter missing')
    source = request.build_absolute_uri(source)

    format = request.GET.get('to')
    url = convertit_url(source, to_type=format)
    response = HttpResponse()
    received = download_to_stream(url, response, silent=True)
    filename = os.path.basename(received.url)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


@require_http_methods(["POST"])
@csrf_exempt
@login_required
def history_delete(request, path=None):
    path = request.POST.get('path', path)
    if path:
        history = request.session['history']
        history = [h for h in history if h.path != path]
        request.session['history'] = history
    return HttpResponse()
