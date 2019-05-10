# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from lra.sitecontent.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of lra.sitecontent into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if lra.sitecontent is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('lra.sitecontent'))

    def test_uninstall(self):
        """Test if lra.sitecontent is cleanly uninstalled."""
        self.installer.uninstallProducts(['lra.sitecontent'])
        self.assertFalse(self.installer.isProductInstalled('lra.sitecontent'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ILraSitecontentLayer is registered."""
        from lra.sitecontent.interfaces import ILraSitecontentLayer
        from plone.browserlayer import utils
        self.failUnless(ILraSitecontentLayer in utils.registered_layers())
