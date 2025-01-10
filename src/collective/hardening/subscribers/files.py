from collective.hardening.interfaces import ICollectiveHardeningLayer
from functools import wraps
from plone.dexterity.interfaces import IDexterityContent
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


def is_package_installed(func):
    """Decorator to check if this package is installed."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        request = getRequest()
        if ICollectiveHardeningLayer.providedBy(request):
            return func(*args, **kwargs)
        return None

    return wrapper


def _validate_contentType(obj):
    """Check if the mimetype is set."""
    try:
        if obj.file.contentType in (
            "application/x-msdownload",
            "application/x-ms-installer",
            "application/x-msdos-program",
        ):
            raise ValueError("You cannot upload MS executables here.")
    except AttributeError:
        pass


@adapter(IDexterityContent, IObjectCreatedEvent)
@is_package_installed
def validate_created(obj, event):
    """Validate the file."""
    _validate_contentType(obj)


@adapter(IDexterityContent, IObjectModifiedEvent)
@is_package_installed
def validate_modified(obj, event):
    """Validate the file."""
    _validate_contentType(obj)
