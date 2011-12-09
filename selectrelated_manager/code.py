"""
Jakub Krajniak <jkrajniak@gmail.com>
Custom manager with added select_related for filter, exclude, all() methods

"""

from django.db.models import Manager

class SelectRelatedManager(Manager):
    _select_field_lookup = []
        
    def filter(self, *args, **kwargs):
        return super(SelectRelatedManager, self).select_related(*self._select_field_lookup).filter(*args, **kwargs)
        

    def exclude(self, *args, **kwargs):
        return super(SelectRelatedManager, self).select_related(*self._select_field_lookup).exclude(*args, **kwargs)

    def all(self):
        return super(SelectRelatedManager, self).select_related(*self._select_field_lookup).all()

def selectrelated_manager(field_lookup):
    """
    Create manager
    """
    cls = SelectRelatedManager
    cls._select_field_lookup = field_lookup
    return cls()
