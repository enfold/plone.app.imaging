from unittest import TestSuite
from zope.testing import doctest
from Testing import ZopeTestCase as ztc
from plone.app.controlpanel.tests.cptc import ControlPanelTestCase
from plone.app.imaging.tests.base import ImagingFunctionalTestCase
from plone.app.imaging.tests.layer import ImagingLayer


optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


class ImagingControlPanelTestCase(ControlPanelTestCase):
    """ base class for control-panel tests """

    layer = ImagingLayer


def test_suite():
    return TestSuite([
        ztc.FunctionalDocFileSuite(
           'traversal.txt', package='plone.app.imaging.tests',
           test_class=ImagingFunctionalTestCase, optionflags=optionflags),
        ztc.FunctionalDocFileSuite(
           'transforms.txt', package='plone.app.imaging.tests',
           test_class=ImagingFunctionalTestCase, optionflags=optionflags),
        ztc.FunctionalDocFileSuite(
           'configlet.txt', package='plone.app.imaging.tests',
           test_class=ImagingControlPanelTestCase, optionflags=optionflags),
    ])
