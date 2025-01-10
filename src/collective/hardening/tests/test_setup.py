"""Setup tests for this package."""

from collective.hardening import testing
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from plone.base.utils import get_installer
except ImportError:
    from Products.CMFPlone.utils import get_installer


class TestSetup(unittest.TestCase):
    """Test that collective.hardening is properly installed."""

    layer = testing.COLLECTIVE_HARDENING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.hardening is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.hardening"))

    def test_browserlayer(self):
        """Test that ICollectiveHardeningLayer is registered."""
        from collective.hardening import interfaces
        from plone.browserlayer import utils

        self.assertIn(interfaces.ICollectiveHardeningLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    layer = testing.COLLECTIVE_HARDENING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.hardening")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.hardening is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.hardening"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveHardeningLayer is removed."""
        from collective.hardening import interfaces
        from plone.browserlayer import utils

        self.assertNotIn(
            interfaces.ICollectiveHardeningLayer, utils.registered_layers()
        )
