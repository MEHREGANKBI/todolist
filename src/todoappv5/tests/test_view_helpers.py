from django.test import TestCase
from datetime import datetime, timezone
from django.contrib.auth import get_user_model

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

    The primary focus of this class is to ensure the username check works fine and as such, time consuming
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


class TestTaskExists(TestCase):
    '''
    This class tests two major cases, a task that exsists and a task that doesn't. 
    Invalid tasks will not be the subject of this test class since this function expects its sole parameter to be
    sanitized. Tests regarding the invalid tasks are out of scope for this class and
    are related to its own correspoding serializer.

    For every type of test in this class, there will be a minimum of 3 test cases that'll be run to make sure
    the first or second one wasn't a fluke. 

    The primary focus of this class is to ensure the <id> check works fine and as such, other fields are simply filled
    with valid items to satisfy the model's needs. Non-mandatory fields are ignored in this test.
    '''

    def setUp(self):
        # All of the tasks will be made with the same user as the owner since the owner is not the topic of this test.
        user_model = get_user_model()
        user_model.objects.create(username='Jafarr', email='Jar@example.com', first_name='Jafar',
                                   last_name='Jafari', password='12345678')
        user_obj = user_model.objects.get(username= 'Jafarr')

        dt_obj = datetime.fromtimestamp(1704492435, tz= timezone.utc)

        # ids 1 to 5 should be created with the following commands.
        Task.objects.create(task='Wash the dishes.', is_complete= True, User= user_obj, deadline_at= dt_obj)
        Task.objects.create(task='Wash the clothes.', is_complete= False, User= user_obj, deadline_at= dt_obj)
        Task.objects.create(task='Drink some water.', is_complete= False, User= user_obj, deadline_at= dt_obj)
        Task.objects.create(task='Do homework.', is_complete= False, User= user_obj, deadline_at= dt_obj)
        Task.objects.create(task='Walk the dogs.', is_complete= True, User= user_obj, deadline_at= dt_obj)


    def tearDown(self):
        Task.objects.all().delete()
        get_user_model().objects.all().delete()


    def test_existing_tasks(self):
        id1, id2, id3 = 1, 2, 5

        self.assertTrue(task_exists(task_id= id1))
        self.assertTrue(task_exists(task_id= id2))
        self.assertTrue(task_exists(task_id= id3))


    def test_non_existing_tasks(self):
        id1, id2, id3 = 69, 420, 6   # The id:6 shouldn't exist under normal circumstances.

        self.assertFalse(task_exists(task_id= id1))
        self.assertFalse(task_exists(task_id= id2))
        self.assertFalse(task_exists(task_id= id3))



class TestUserOwnsTask(TestCase):
    '''
    This class tests two major cases, a user owning a task and a user not owning a task. 
    Invalid tasks or users will not be the subject of this test class since this function expects its parameters to be
    sanitized. Tests regarding the invalid tasks are out of scope for this class and
    are related to its own correspoding serializer.

    For every type of test in this class, there will be a minimum of 3 test cases that'll be run to make sure
    the first or second one wasn't a fluke. 

    The primary focus of this class is to ensure the ownership and as such, fields other than <User> are simply filled
    with valid items to satisfy the model's needs. Non-mandatory fields are ignored altogether.
    '''

    def setUp(self):
        # We'll need 6 users. 3 will own tasks and the other 3 won't. 
        user_model = get_user_model()
        user_list = []
        user_list.append(user_model.objects.create(username='Jafarr', email='Jar@example.com', first_name='Jafar',
                                   last_name='Jafari', password='12345678'))
        
        user_list.append(user_model.objects.create(username='Jafer', email='Jarf@example.com', first_name='Jaffar',
                                   last_name='Jafari', password='123'))
        
        user_list.append(user_model.objects.create(username='Jafar', email='Jfaar@example.com', first_name='Jafar',
                                   last_name='Jojari', password='678'))
        
        user_list.append(user_model.objects.create(username='samar', email='sam@example.com', first_name='summer',
                                   last_name='samuel', password='12345678'))
        
        user_list.append(user_model.objects.create(username='Gab9819', email='Gabriella@example.com', first_name='Gaberiel',
                                   last_name='lora', password='5678'))
        
        user_list.append(user_model.objects.create(username='Jayyson', email='Jasondunphy@example.com', first_name='Jamie',
                                   last_name='Davidson', password='abcd'))
        # the deadline field is not important in this test and thus will be the same for every task.
        dt_obj = datetime.fromtimestamp(1704492435, tz= timezone.utc)

        # ids 1 to 5 should be created with the following commands. some users may have more than one task. We'll avoid tags.
        Task.objects.create(task='Wash the dishes.', is_complete= True, User= user_list[0], deadline_at= dt_obj)
        Task.objects.create(task='Wash the clothes.', is_complete= False, User= user_list[5], deadline_at= dt_obj)
        Task.objects.create(task='Drink some water.', is_complete= False, User= user_list[0], deadline_at= dt_obj)
        Task.objects.create(task='Do homework.', is_complete= False, User= user_list[2], deadline_at= dt_obj)
        Task.objects.create(task='Walk the dogs in the morning.', is_complete= False, User= user_list[2], deadline_at= dt_obj)
        


    def tearDown(self):
        get_user_model().objects.all().delete()
        Task.objects.all().delete()

    def test_user_owning_task(self):
        user1, task1 = get_user_model().objects.get(username= 'Jafarr'), 1
        user2, task2 = get_user_model().objects.get(username= 'Jayyson'), 2
        user3, task3 = get_user_model().objects.get(username= 'Jafar'), 4 

        self.assertTrue(user_owns_task(user_obj= user1, task_id= task1))
        self.assertTrue(user_owns_task(user_obj= user2, task_id= task2))
        self.assertTrue(user_owns_task(user_obj= user3, task_id= task3))


    def test_user_not_owning_task(self):
        user1, task1 = get_user_model().objects.get(username= 'Jafarr'), 2  # This user owns a task, but it's not this task.
        user2, task2 = get_user_model().objects.get(username= 'Gab9819'), 3 # Doesn't own any tasks.
        user3, task3 = get_user_model().objects.get(username= 'samar'), 5 # Doesn't own any tasks.

        self.assertFalse(user_owns_task(user_obj= user1, task_id= task1))
        self.assertFalse(user_owns_task(user_obj= user2, task_id= task2))
        self.assertFalse(user_owns_task(user_obj= user3, task_id= task3))
