__author__ = 'mpetyx'


from .models import Museum
from mapentity import registry


urlpatterns = registry.register(Museum)