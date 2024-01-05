from django.test import TestCase
from todoappv5.models import *


from todoappv5.view_helpers import *
# Create your tests here.

class TestTagExists(TestCase):
    '''
    This class tests two major cases, a tag that exsists and a tag that doesn't. 
    Invalid tags will not be the subject of this test class since this function expects its sole parameter to be
    sanitized. Tests regarding the invalid tags are out of scope for this class and are related to the correspoding serializer.

    For every type of test in this class, there will be a minimum of 3 test cases that'll be run to make sure
    the first or second one wasn't a fluke. 
    '''

    def setUp(self):
        # These tags will exist in the tables and the test cases will be compared against them.
        Tag.objects.create(tag = 'School')
        Tag.objects.create(tag = 'Work')
        Tag.objects.create(tag = 'Chores')

    
    def tearDown(self):
        # This function will remove all records from the <Tag> table. 
        Tag.objects.all().delete()

    def test_existing_tags(self):
        tag1 = 'School'
        tag2 = 'Chores'
        tag3 = 'Work'
        self.assertTrue(tag_exists(tag= tag1))
        self.assertTrue(tag_exists(tag= tag2))
        self.assertTrue(tag_exists(tag= tag3))
