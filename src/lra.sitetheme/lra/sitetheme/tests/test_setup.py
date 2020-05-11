# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from lra.LRA.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of lra.LRA into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if lra.LRA is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('lra.LRA'))

    def test_uninstall(self):
        """Test if lra.LRA is cleanly uninstalled."""
        self.installer.uninstallProducts(['lra.LRA'])
        self.assertFalse(self.installer.isProductInstalled('lra.LRA'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ILraLraLayer is registered."""
        from lra.LRA.interfaces import ILraLraLayer
        from plone.browserlayer import utils
        self.failUnless(ILraLraLayer in utils.registered_layers())
