from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile

from paperclip.models import Attachment, FileType
from paperclip.views import add_url_for_obj

from mapentity.views.generic import MapEntityDetail
from .models import DummyModel


User = get_user_model()


class EntityAttachmentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('howard', 'h@w.com', 'booh')
        self.object = DummyModel.objects.create()

    def createRequest(self):
        request = RequestFactory().get('/dummy')
        request.session = {}
        request.user = self.user
        return request

    def createAttachment(self, obj):
        uploaded = SimpleUploadedFile('file.odt',
                                      '*' * 128,
                                      content_type='application/vnd.oasis.opendocument.text')
        kwargs = {
            'content_type': ContentType.objects.get_for_model(obj),
            'object_id': obj.pk,
            'filetype': FileType.objects.create(),
            'creator': self.user,
            'title': "Attachment title",
            'legend': "Attachment legend",
            'attachment_file': uploaded
        }
        return Attachment.objects.create(**kwargs)

    def test_list_attachments_in_details(self):
        self.createAttachment(self.object)
        request = self.createRequest()
        view = MapEntityDetail.as_view(model=DummyModel,
                                       template_name="mapentity/entity_detail.html")
        response = view(request, pk=self.object.pk)
        html = unicode(response.render())
        self.assertTemplateUsed(response, template_name='paperclip/details.html')

        self.assertEqual(1, len(Attachment.objects.attachments_for_object(self.object)))

        self.assertFalse("Upload attachment" in html)

        for attachment in Attachment.objects.attachments_for_object(self.object):
            self.assertTrue(attachment.legend in html)
            self.assertTrue(attachment.title in html)
            self.assertTrue(attachment.attachment_file.url in html)
            self.assertTrue('paperclip/fileicons/odt.png')

    def test_upload_form_in_details_if_perms(self):
        subclass = type('DummyDetail', (MapEntityDetail,), {'can_edit': lambda x: True})
        view = subclass.as_view(model=DummyModel,
                                template_name="mapentity/entity_detail.html")

        request = self.createRequest()
        response = view(request, pk=self.object.pk)
        html = unicode(response.render())
        self.assertTrue("Upload attachment" in html)
        self.assertTrue("""<form method="post" enctype="multipart/form-data"
      action="/paperclip/add-for/tests/dummymodel/1/""" in html)


class UploadAttachmentTestCase(TestCase):

    def setUp(self):
        self.object = DummyModel.objects.create()
        user = User.objects.create_user('aah', 'email@corp.com', 'booh')
        success = self.client.login(username=user.username, password='booh')
        self.assertTrue(success)

    def attachmentPostData(self):
        filetype = FileType.objects.create()
        uploaded = SimpleUploadedFile('face.jpg',
                                      '*' * 128,
                                      content_type='image/jpeg')
        data = {
            'filetype': filetype.pk,
            'title': 'A title',
            'legend': 'A legend',
            'attachment_file': uploaded,
            'next': self.object.get_detail_url()
        }
        return data

    def test_upload_redirects_to_dummy_detail_url(self):
        response = self.client.post(add_url_for_obj(self.object),
                                    data=self.attachmentPostData())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://testserver/dummy-detail')

    def test_upload_creates_attachment(self):
        data = self.attachmentPostData()
        self.client.post(add_url_for_obj(self.object), data=data)
        att = Attachment.objects.attachments_for_object(self.object).get()
        self.assertEqual(att.title, data['title'])
        self.assertEqual(att.legend, data['legend'])
        self.assertEqual(att.filetype.pk, data['filetype'])

    def test_title_gives_name_to_file(self):
        data = self.attachmentPostData()
        self.client.post(add_url_for_obj(self.object), data=data)
        att = Attachment.objects.attachments_for_object(self.object).get()
        self.assertTrue('a-title' in att.attachment_file.name)

    def test_filename_is_used_if_no_title(self):
        data = self.attachmentPostData()
        data['title'] = ''
        self.client.post(add_url_for_obj(self.object), data=data)
        att = Attachment.objects.attachments_for_object(self.object).get()
        self.assertTrue('face' in att.attachment_file.name)
