import pytest
from service import UserService, APIClient


def test_get_username_with_mock(mocker):
    # mock an entire class instead of one function
    mock_api_client = mocker.Mock(spec=APIClient)
    
    # Mock get_user_data to return a fake user
    mock_api_client.get_user_data.return_value = {'id': 1, 'name': 'Alice'}
    
    # Inject mock api client
    service = UserService(mock_api_client)
    
    # call method that depends on the mock
    result = service.get_username(1)
    
    # Assertions
    assert result == 'ALICE'
    mock_api_client.get_user_data.assert_called_once_with(1)