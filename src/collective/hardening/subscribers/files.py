from collective.hardening.adapters.primary_field import IValidateUpload
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


@adapter(IDexterityContent, IObjectCreatedEvent)
@is_package_installed
def validate_created(obj, event):
    """Validate the file."""
    IValidateUpload(obj).validate()


@adapter(IDexterityContent, IObjectModifiedEvent)
@is_package_installed
def validate_modified(obj, event):
    """Validate the file."""
    IValidateUpload(obj).validate()
