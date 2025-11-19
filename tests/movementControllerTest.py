import sys
from unittest.mock import MagicMock, patch
import pytest
from unittest.mock import call


#mock the connection object from uartConnection before import
sys.modules['src.utils.uartConnection'] = MagicMock()

import src.controllers.movementController as movementController

@pytest.fixture
def mock_connection():
    """Fake UART connection for testing."""
    mock_conn = MagicMock()
    mock_conn.is_open = True
    return mock_conn


def test_set_motor_state_closed_loop(mock_connection):
    #arrange
    # Mock serial responses for each readline() call
    mock_connection.readline.side_effect = [
        b"8\n",  # final axis0 state
        b"8\n",  # final axis1 state
    ]

    movementController.ser = mock_connection

    #act
    movementController.set_motor_state_closed_loop()

    #assert
    expected_calls = [
        call.write(b"w axis0.requested_state 8\n"),
        call.write(b"w axis1.requested_state 8\n"),
        call.write(b"r axis0.current_state\n"),
        call.write(b"r axis1.current_state\n"),
    ]

    mock_connection.write.assert_has_calls(expected_calls, any_order=False)


def test_set_motor_state_idle(mock_connection):
    #arrange
    # Mock serial responses for each readline() call
    mock_connection.readline.side_effect = [
        b"1\n",  # final axis0 state
        b"1\n",  # final axis1 state
    ]

    movementController.ser = mock_connection

    #act
    movementController.set_motor_state_idle()

    #assert
    expected_calls = [
        call.write(b"w axis0.requested_state 1\n"),
        call.write(b"w axis1.requested_state 1\n"),
        call.write(b"r axis0.current_state\n"),
        call.write(b"r axis1.current_state\n")
    ]

    mock_connection.write.assert_has_calls(expected_calls, any_order=False)