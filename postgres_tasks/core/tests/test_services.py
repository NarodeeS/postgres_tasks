from django.test import TestCase
from django.core.files import File

from core.models import Task, User, CompletedTask, DatabaseInfo
from domain import commands
from domain.database_status import DatabaseStatus
from domain.errors import OutOfMovesError, NoSuchDbError
from core.bootstrap import bootstrap
from core.utils.db_utils import get_db_info
from .handlers.handlers import TEST_HANDLERS
from .config import USER_EMAIL, USER_PASSWORD


bus = bootstrap(handlers=TEST_HANDLERS)


class ServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        task_payload = { 
            'title': 'Test',
            'description': 'Test task',
            'difficulty': 100,
            'moves_count': 3 
        }
        task = Task(**task_payload, 
                    creation_script=File(open('./core/tests/data/creation.sql','rb')), 
                    check_script=File(open('./core/tests/data/check_script.sql','rb')), 
                    db_structure=File(open('./core/tests/data/db_structure.png','rb'))
        )
        cls.task = task
        task.save()
        user_data = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'student_group': 'BSBO-01-20',
            'email': USER_EMAIL,
            'password': USER_PASSWORD
        }
        cls.user = User.objects.create_user(**user_data)

    def tearDown(self) -> None:
        try:
            bus.handle(commands.DeleteUserTaskDb('db1_1'))
        except Exception:
            pass

    def test_task_creation(self) -> None:
        db_name = bus.handle(commands.CreateUserTask(1, self.user.id))
        new_db = get_db_info(db_name)
        self.assertTrue(new_db is not None)
        self.assertTrue(new_db.status == DatabaseStatus.UP.value)
    
    def test_send_command_out_of_moves(self) -> None:
        db_name = bus.handle(commands.CreateUserTask(1, self.user.id))
        bus.handle(commands.SendSqlCommand(db_name, 'SELECT * FROM orders;'))
        bus.handle(commands.SendSqlCommand(db_name, 'SELECT * FROM orders;'))
        bus.handle(commands.SendSqlCommand(db_name, 'SELECT * FROM orders;'))
        self.assertRaises(OutOfMovesError, 
                          bus.handle, 
                          commands.SendSqlCommand(db_name, 'SELECT * FROM orders;'))

    def test_check_failure(self) -> None:
        db_name = bus.handle(commands.CreateUserTask(1, self.user.id))
        bus.handle(commands.SendSqlCommand(db_name, 'SELECT * FROM orders;'))
        self.assertEquals(bus.handle(commands.CheckTask(db_name)), False)
    
    def test_check_success(self) -> None:
        db_name = bus.handle(commands.CreateUserTask(1, self.user.id))
        bus.handle(commands.SendSqlCommand(db_name, 
                                           ("INSERT INTO orders(customer_name, order_date, total_amount)" 
                                            "VALUES ('George', now()::date, 1), ('George', now()::date, 1),"
                                            "('George', now()::date, 1),('George', now()::date, 1);")))
        self.assertEquals(bus.handle(commands.CheckTask(db_name)), True)

    def test_finish_task(self) -> None:
        db_name = bus.handle(commands.CreateUserTask(1, self.user.id))
        bus.handle(commands.SendSqlCommand(db_name, 
                                                ("INSERT INTO orders(customer_name, order_date, total_amount)" 
                                                    "VALUES ('George', now()::date, 1), ('George', now()::date, 1),"
                                                    "('George', now()::date, 1),('George', now()::date, 1);")))
        bus.handle(commands.FinishUserTask(db_name))
        completed_task = (CompletedTask.objects
                          .filter(task=self.task, 
                                  user=self.user).first())
        self.assertTrue(completed_task is not None)
        self.assertRaises(NoSuchDbError, get_db_info, db_name)

    def test_delete_db(self) -> None:
        db_name = bus.handle(commands.CreateUserTask(1, self.user.id))
        bus.handle(commands.DeleteUserTaskDb(db_name))
        self.assertRaises(NoSuchDbError, get_db_info, db_name)
