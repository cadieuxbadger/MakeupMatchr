from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.test.client import RequestFactory
import makeupApp.views
import io
from PIL import Image
from base64 import b64encode, b64decode

#Unit tests
class imageUploadTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_image_upload(self):
        img = Image.new('RGB', (10, 10), color = 'red')
        b = io.BytesIO()
        img.save(b, "JPEG")
        b.seek(0)
        post_request = self.rf.post('/', {"image": b}, HTTP_USER_AGENT='IMAGE_UPLOAD_TEST')
        post_request.session = {}
        response = makeupApp.views.index(post_request)
        self.assertEqual(response.status_code, 302) #expect a redirect

class colorPickingTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_color_pick(self):
        request = self.rf.post('/picker/', HTTP_USER_AGENT='COLOR_PICKER_TEST')
        img = Image.new('RGB', (10, 10), color = (255, 0, 0))
        b = io.BytesIO()
        img.save(b, "JPEG")
        request.session = {'image': b64encode(b.getvalue()).decode()}
        request.META['QUERY_STRING'] = "?5,5"
        response = makeupApp.views.picker(request)
        self.assertEqual(response.status_code, 302) # Expect redirect
        self.assertEqual(request.session['color-values']['r'], 254)

class databaseModelTests(TestCase):
    pass

class resultsTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_results_base(self): # No filtering
        request = self.rf.get('/results/', HTTP_USER_AGENT='RESULTS_TEST')
        request.session = {'color-values': {'r': 150, 'g': 80, 'b': 70}}
        response = makeupApp.views.results(request)
        self.assertEqual(response.status_code, 200) # Response OK

    def test_results_filter(self): # With Filtering
        request = self.rf.post('/results/', {"brandName": 'e.l.f.'}, HTTP_USER_AGENT='RESULTS_TEST')
        request.session = {'color-values': {'r': 150, 'g': 80, 'b': 70}}
        response = makeupApp.views.results(request)
        self.assertEqual(response.status_code, 200) # Response OK

# Integration Tests
class imageCorrectionPickerPipeline(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
    
    def test_ICP_pipeline(self):
        # upload a dummy image with a skin tone
        img = Image.new('RGB', size = (100, 100), color = (150, 80, 70)) 
        b = io.BytesIO()
        img.save(b, "JPEG")
        b.seek(0)
        request = self.rf.post('/', {"image": b}, HTTP_USER_AGENT='ICP_TEST')
        request.session = {}
        response = makeupApp.views.index(request)
        self.assertEqual(response.status_code, 302) # image uploaded and redirected
        self.assertEqual('image' in request.session.keys(), True) # image added to the sessions
        session = request.session
        request = self.rf.post('/picker/', HTTP_USER_AGENT='ICP_TEST')
        request.session = session
        request.META['QUERY_STRING'] = "?5,5"
        response = makeupApp.views.picker(request)
        self.assertEqual(response.status_code, 302) # Expect redirect
        self.assertEqual('r' in request.session['color-values'].keys(), True)
        self.assertEqual('g' in request.session['color-values'].keys(), True)
        self.assertEqual('b' in request.session['color-values'].keys(), True)

class pickedColorResultsPipeline(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_CR_Pipeline(self):
        request = self.rf.post('/picker/', HTTP_USER_AGENT='RESULTS_TEST')
        img = Image.new('RGB', (10, 10), color = (150, 80, 70))
        b = io.BytesIO()
        img.save(b, "JPEG")
        request.session = {'image': b64encode(b.getvalue()).decode()}
        request.META['QUERY_STRING'] = "?5,5"
        response = makeupApp.views.picker(request)
        self.assertEqual(response.status_code, 302) # Expect redirect
        session = request.session
        request = self.rf.get('/results/', HTTP_USER_AGENT='RESULTS_TEST')
        request.session = session
        response = makeupApp.views.results(request)
        self.assertEqual(response.status_code, 200)


