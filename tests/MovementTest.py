import sys
import os
from unittest.mock import MagicMock, patch
import pytest



#mock the connection object from uartConnection before import
sys.modules['src.utils.uartConnection'] = MagicMock()

#import movement module
import src.operations.movement.movement as movement


@pytest.fixture
def mock_connection():
    """Fake UART connection for testing."""
    mock_conn = MagicMock()
    mock_conn.is_open = True
    return mock_conn


def test_send_command(mock_connection):
    movement.connection = mock_connection

    movement.send_command("test_command")

    mock_connection.write.assert_called_once_with(b"test_command\n")

def test_moveForward(mock_connection):
    movement.connection = mock_connection

    movement.moveForward(1.5)

    mock_connection.write.assert_any_call(b"v 0 1.5\n")
    mock_connection.write.assert_any_call(b"v 1 1.5\n")
    assert mock_connection.write.call_count == 302

def test_moveBackwards(mock_connection):
    movement.connection = mock_connection

    movement.moveBackwards(1.5)

    mock_connection.write.assert_any_call(b"v 0 -1.5\n")
    mock_connection.write.assert_any_call(b"v 1 -1.5\n")
    assert mock_connection.write.call_count == 302

def test_StopMoving(mock_connection):
    #Arrange
    movement.connection = mock_connection
    movement.current_velocity["0"] = 1.7
    movement.current_velocity["1"] = 1.5

    #Act
    movement.stopMoving()

    #Assert
    mock_connection.write.assert_any_call(b"v 0 0\n")
    mock_connection.write.assert_any_call(b"v 1 0\n")
    assert mock_connection.write.call_count == 202

def test_turnLeft(mock_connection):
    #ARRANGE
    movement.connection = mock_connection
    movement.current_velocity["0"] = 1.5
    movement.current_velocity["1"] = 1.5

    #ACT
    movement.turnLeft(20)

    #ASSERT
    mock_connection.write.assert_any_call(b"v 0 " + str(1.5 * 1.20).encode() + "\n".encode())

def test_turnRight(mock_connection):
    # ARRANGE
    movement.connection = mock_connection
    movement.current_velocity["0"] = 1.5
    movement.current_velocity["1"] = 1.5

    # ACT
    movement.turnRight(20)

    # ASSERT
    mock_connection.write.assert_any_call(b"v 1 " + str(1.5 * 1.20).encode() + "\n".encode())

def test_stopTurning(mock_connection):
    #ARRANGE
    movement.connection = mock_connection
    movement.current_velocity["0"] = 1.7
    movement.current_velocity["1"] = 1.5
    #ACT

    movement.stopTurning()

    #ASSERT

    mock_connection.write.assert_any_call(b"v 0 1.5\n")
    assert mock_connection.write.call_count == 2