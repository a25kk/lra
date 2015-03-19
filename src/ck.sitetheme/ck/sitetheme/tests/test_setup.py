# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from ck.Chis Kolonko.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of ck.Chis Kolonko into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ck.Chis Kolonko is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ck.Chis Kolonko'))

    def test_uninstall(self):
        """Test if ck.Chis Kolonko is cleanly uninstalled."""
        self.installer.uninstallProducts(['ck.Chis Kolonko'])
        self.assertFalse(self.installer.isProductInstalled('ck.Chis Kolonko'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICkChis kolonkoLayer is registered."""
        from ck.Chis Kolonko.interfaces import ICkChis kolonkoLayer
        from plone.browserlayer import utils
        self.failUnless(ICkChis kolonkoLayer in utils.registered_layers())
