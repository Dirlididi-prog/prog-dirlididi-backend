from models.user import User
from pytest import fixture
from tests.helpers import clear_db_data


@fixture
def user(clear_db_data):
    from services.user_service import UserService
    user = UserService().create_user(email="test@test.com", password="12345", name="test")
    return user


def test_user_add_problem(user):
    user.add_problem(name="Hello World!", description="Make your Python script print 'Hello World!' on the screen", publish=True, tip=None, tests=[{
        "output": "Hello World!"
    }])
    assert len(user.owned_problems) == 1
    assert user.owned_problems[0].name == "Hello World!"
    assert user.owned_problems[0].tests[0].output == "Hello World!"
