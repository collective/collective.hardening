from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import collective.hardening


class CollectiveHardeningLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.hardening)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.hardening:default")


COLLECTIVE_HARDENING_FIXTURE = CollectiveHardeningLayer()


COLLECTIVE_HARDENING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_HARDENING_FIXTURE,),
    name="CollectiveHardeningLayer:IntegrationTesting",
)
