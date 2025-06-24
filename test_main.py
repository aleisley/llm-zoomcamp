from main import add, divide, UserManager, Database, is_prime, get_weather, save_user
import pytest


def test_add():
    assert add(2, 3) == 5, '2 + 3 should be 5'
    assert add(-1, 1) == 0, '-1 + 1 should be 0'
    assert add(0, 0) == 0, '0 + 0 should be 0'
    
    
def test_divide():
    with pytest.raises(ValueError, match='Cannot divide by zero'):
        divide(10, 0)
    assert divide(10, 2) == 5, '10 / 2 should be 5'


@pytest.fixture
def user_manager():
    """ Creates a fresh instance of UserManager before each test """
    return UserManager()


def test_add_user(user_manager):
    assert user_manager.add_user('john_doe', 'john@example.com') == True
    assert user_manager.get_user('john_doe') == 'john@example.com'
    
    
def test_add_duplicate_user(user_manager):
    user_manager.add_user('john_doe', 'john@example.com')
    with pytest.raises(ValueError):
        user_manager.add_user('john_doe', 'another@example.com')
        
        
@pytest.fixture
def db():
    """ Provides a fresh instance of the Dtabase class and cleans up after the test """
    database = Database()
    yield database # provide the fixture instance
    database.data.clear() # cleanup step (not needed for in memory, but useful for real dbs)
    
    
def test_add_user(db):
    db.add_user(1, 'Alice')
    assert db.get_user(1) == 'Alice'
    

def test_add_duplicate_user(db):
    db.add_user(1, 'Alice')
    with pytest.raises(ValueError, match='User already exists'):
        db.add_user(1, 'Bob')
        

def test_delete_user(db):
    db.add_user(2, 'Bob')
    db.delete_user(2)
    assert db.get_user(2) is None
    
    
@pytest.mark.parametrize('num, expected', [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    # (17, True),
    (18, False),
    # (19, True),
    (25, False)
])
def test_is_prime(num, expected):
    assert is_prime(num) == expected
    
    
def test_get_weather(mocker):
    # mock requests.get
    mock_get = mocker.patch('main.requests.get')
    
    # Set return values
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'temperature': 25, 'condition': 'Sunny'}
    
    # Call function
    result = get_weather('Dubai')
    
    # Assertions
    assert result == {'temperature': 25, 'condition': 'Sunny'}
    mock_get.assert_called_once_with('https://api.weather.com/v1/Dubai')
    
    
def test_save_user(mocker):
    mock_conn = mocker.patch('main.sqlite3.connect')
    mock_cursor = mock_conn.return_value.cursor.return_value
    
    save_user('Alice', 30)
    
    mock_conn.assert_called_once_with('users.db')
    mock_cursor.execute.assert_called_once_with(
        'INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30)
    )