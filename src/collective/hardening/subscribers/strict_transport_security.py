from collective.hardening.interfaces import ICollectiveHardeningLayer
from zope.component import adapter
from ZPublisher.interfaces import IPubSuccess


@adapter(IPubSuccess)
def add_header(event):
    if not ICollectiveHardeningLayer.providedBy(event.request):
        return

    event.request.response.setHeader(
        "Strict-Transport-Security",
        "max-age=31536000; includeSubDomains; preload",
    )
