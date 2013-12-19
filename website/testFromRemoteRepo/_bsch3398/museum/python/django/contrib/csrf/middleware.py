import warnings

warnings.warn(
    "This import for CSRF functionality is deprecated.  Please use django.middleware.csrf for the middleware and django.views.decorators.csrf for decorators.",
    PendingDeprecationWarning
)
