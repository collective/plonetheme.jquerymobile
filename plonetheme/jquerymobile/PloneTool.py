from collective.monkeypatcher import meta
from zope import component
from zope import interface
from plonetheme.jquerymobile import interfaces
from plonetheme.jquerymobile import logger
from plone.app.layout.globals.interfaces import IViewView

def browserDefault(self, obj):
    """We monkey patch this method. We want to control html rendering
    throw @@jquerymobile view"""
    request = getattr(self, 'REQUEST', None)

    if interfaces.IThemingLayer.providedBy(request):
        if obj.isPrincipiaFolderish:
            defaultPage = self.getDefaultPage(obj)
            if defaultPage is not None:
                logger.info('apply original browserDefault with defaultpage')
                return self._old_browserDefault(obj)

        try:
            view = component.getMultiAdapter((obj, request), name='jquerymobile')
            if view.apply_to_context():
                logger.info('apply jquerymobile view')
                return obj, ['@@jquerymobile']
        except component.ComponentLookupError, e:
            logger.info('can t find jquerymobile view on %s'%obj)
        except AttributeError, e:
            logger.info('attribute error on view for %s'%(view, obj))

    logger.info('apply original browserDefault')
    return self._old_browserDefault(obj)

