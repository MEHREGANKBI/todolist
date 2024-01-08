from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, timezone
from rest_framework.request import Request


from todoappv5.models import *
from todoappv5.views import TaskView

class TestTaskViewGET(TestCase):
    '''
    The following tests, test the functionality of the <get> method of TaskView in a vaccum. In other words, the urlconf
    and authorization processes are avoided. To narrow down error causes, each testcase 
    will have valid attributes for all the attributes that are not the subject of that test. 
    For instance, when testing the behavior of passing invalid <type_params>, the user is considered to be authorized
    and authenticated and present in the user model.
    '''
    def setUp(self):
        user_model = get_user_model()
        userwithtasks = user_model.objects.create(username='userwithtasks', email='tasky@example.com', first_name='with',
                                   last_name='task', password='12345678')
        notaskuser = user_model.objects.create(username='notaskuser', email='nontasky@example.com', first_name='without',
                                   last_name='task', password='12345678')
        
        self.users = [userwithtasks, notaskuser]
        
        dt_obj = datetime.fromtimestamp(1704492435, tz= timezone.utc)

        # ids 1 to 5 should be created with the following commands. one user has 3 tasks with different done status.
        Task.objects.create(task='Wash the dishes.', is_complete= True, User= userwithtasks, deadline_at= dt_obj)
        Task.objects.create(task='Wash the clothes.', is_complete= False, User= userwithtasks, deadline_at= dt_obj)
        Task.objects.create(task='Drink some water.', is_complete= False, User= userwithtasks, deadline_at= dt_obj)
        
        
    def tearDown(self):
        get_user_model().objects.all().delete()
        Task.objects.all().delete()


    def test_valid_params(self):
        # Testing almost all valid cases. All upper-case, all lower-case, a mix of both. 
        #valid_type_params = ['ALL', 'DONE', 'UNDONE','doNe', 'aLL', 'undone', 'UnDoNe']
        # A user with tasks
        pass

        
    def test_user_with_no_tasks(self):
        pass
    def test_block_listed_user(self):
        pass
    
