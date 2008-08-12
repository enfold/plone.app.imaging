from unittest import defaultTestLoader
from unittest import TestCase
from zope.interface.verify import verifyClass
from zope.publisher.interfaces import IPublishTraverse
from plone.app.imaging.traverse import ImageTraverser
from Products.Archetypes.atapi import ImageField


data_marker = object()
fallback_marker = object()


class BaseMockField:

    def getAvailableSizes(self, context):
        return dict(mini=1, maxi=2)

    def getScale(self, context, scale):
        return data_marker


class MockField(BaseMockField, ImageField):

    pass


class MockContext:

    def Schema(self):
        return self

    def get(self, key):
        return getattr(self, key, None)


class TraverseTests(TestCase):

    def setUp(self):
        def fallback(self, request, name):
            return fallback_marker
        ImageTraverser.org_fallback = ImageTraverser.fallback
        ImageTraverser.fallback = fallback

    def tearDown(self):
        ImageTraverser.fallback = ImageTraverser.org_fallback
        del ImageTraverser.org_fallback

    def testInterface(self):
        self.failUnless(verifyClass(IPublishTraverse, ImageTraverser))

    def testUnknownField(self):
        traverser = ImageTraverser(MockContext(), None)
        self.failUnless(traverser.publishTraverse(None, 'missing') is fallback_marker)

    def testWrongFieldType(self):
        context = MockContext()
        context.field = BaseMockField()
        traverser = ImageTraverser(context, None)
        self.failUnless(traverser.publishTraverse(None, 'field') is fallback_marker)

    def testCorrectFieldType(self):
        context = MockContext()
        context.field = MockField()
        traverser = ImageTraverser(context, None)
        self.failUnless(traverser.publishTraverse(None, 'field') is data_marker)

    def testFullImage(self):
        context = MockContext()
        context.field = MockField()
        traverser = ImageTraverser(context, None)
        self.failUnless(traverser.publishTraverse(None, 'field') is data_marker)

    def testUnknownScale(self):
        context = MockContext()
        context.field = MockField()
        traverser = ImageTraverser(context, None)
        self.failUnless(traverser.publishTraverse(None, 'field_poster') is fallback_marker)

    def testKnownScale(self):
        context = MockContext()
        context.field = MockField()
        traverser = ImageTraverser(context, None)
        self.failUnless(traverser.publishTraverse(None, 'field_mini') is data_marker)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
