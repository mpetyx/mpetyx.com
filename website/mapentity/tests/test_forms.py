from django.test import TestCase

from mapentity.forms import MapEntityForm
from .models import DummyModel


class DummyForm(MapEntityForm):
    class Meta(MapEntityForm.Meta):
        model = DummyModel


class MapEntityFormTest(TestCase):

    def test_can_delete_actions(self):
        form = DummyForm(instance=DummyModel.objects.create())
        self.assertTrue(form.can_delete)
        self.assertTrue('<a class="btn btn-danger delete" href="">' in form.helper.layout[1][0].html)

        form = DummyForm(instance=DummyModel.objects.create(),
                         can_delete=False)
        self.assertFalse(form.can_delete)
        self.assertTrue('<a class="btn disabled delete" href="#">' in form.helper.layout[1][0].html)
