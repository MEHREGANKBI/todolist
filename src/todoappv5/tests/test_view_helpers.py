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


    def test_non_existing_tags(self):
        tag1 = 'Cahrity'
        tag2 = 'school' # This case is to ensure the case sensitivity of the function that is being tested.
        tag3 = 'Taxes'

        self.assertFalse(tag_exists(tag= tag1))
        self.assertFalse(tag_exists(tag= tag2))
        self.assertFalse(tag_exists(tag= tag3))



class TestUserExists(TestCase):
    '''
    This class tests two major cases, a user that exsists and a user that doesn't. 
    Invalid users will not be the subject of this test class since this function expects its sole parameter to be
    sanitized. Tests regarding the invalid usernames are out of scope for this class and
    are related to its own correspoding serializer.

    For every type of test in this class, there will be a minimum of 3 test cases that'll be run to make sure
    the first or second one wasn't a fluke. 

    The primary focus of this class is to ensure the username check works fine or not and as such, time consuming
    tasks like password digestion will be ignored if and/or when possible. The same goes for unrelated fields like email 
    uniqueness and so on.
    '''

    def setUp(self):
        user_model = get_user_model()
        user_model.objects.create(username='Jafarr', email='Jar@example.com', first_name='Jafar',
                                   last_name='Jafari', password='12345678')
        
        user_model.objects.create(username='Jaferam', email='Jafir1369@example.com', first_name='Jafer',
                                   last_name='Jaferi', password='1234')
        
        user_model.objects.create(username='jnant', email='heaven@example.com', first_name='Janat',
                                   last_name='Janati', password='2580')


        
    def tearDown(self):
        get_user_model().objects.all().delete()


    def test_existing_users(self):
        user1 = 'Jafarr'
        user2 = 'Jaferam'
        user3 = 'jnant'

        self.assertTrue(user_exists(username= user1))
        self.assertTrue(user_exists(username= user2))
        self.assertTrue(user_exists(username= user3))


    def test_non_existing_users(self):
        user1 = 'Jafar' # Test similarity to other fields i.e first name in this case.
        user2 = 'saber'
        user3 = 'jnanT' # Test case-sensitivity

        self.assertFalse(user_exists(username= user1))
        self.assertFalse(user_exists(username= user2))
        self.assertFalse(user_exists(username= user3))
