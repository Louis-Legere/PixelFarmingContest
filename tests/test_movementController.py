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


@pytest.mark.parametrize("state,expected_calls", [
    (movementController.DrivingState.STOP, [call.moveForward(1)]),
    (movementController.DrivingState.FORWARD, []),
    (movementController.DrivingState.BACKWARD, [call.stopMoving(), call.moveForward(1)]),
    (movementController.DrivingState.TURN_LEFT, [call.stopTurning(), call.moveForward(1)]),
    (movementController.DrivingState.TURN_RIGHT, [call.stopTurning(), call.moveForward(1)]),
])
@patch("time.sleep", return_value=None)
@patch("src.controllers.movementController.movement")
def test_transferToForward(mock_movement, mock_sleep, state, expected_calls):
    # Arrange
    movementController.currentDrivingState = state

    # Act
    movementController.transferToForward(1)

    # Assert
    actual_calls = mock_movement.mock_calls
    assert actual_calls == expected_calls


@pytest.mark.parametrize("state,expected_calls", [
    (movementController.DrivingState.STOP, [call.moveBackwards(1)]),
    (movementController.DrivingState.FORWARD, [call.stopMoving(), call.moveBackwards(1)]),
    (movementController.DrivingState.BACKWARD, []),
    (movementController.DrivingState.TURN_LEFT, [call.stopTurning(), call.moveBackwards(1)]),
    (movementController.DrivingState.TURN_RIGHT, [call.stopTurning(), call.moveBackwards(1)]),
])
@patch("time.sleep", return_value=None)
@patch("src.controllers.movementController.movement")
def test_transferToBackward(mock_movement, mock_sleep, state, expected_calls):
    # Arrange
    movementController.currentDrivingState = state

    # Act
    movementController.transferToBackward(1)

    # Assert
    actual_calls = mock_movement.mock_calls
    assert actual_calls == expected_calls

@pytest.mark.parametrize("state,expected_calls", [
    (movementController.DrivingState.STOP, [call.turnLeft(20)]),
    (movementController.DrivingState.FORWARD, [call.turnLeft(20)]),
    (movementController.DrivingState.BACKWARD, []),
    (movementController.DrivingState.TURN_LEFT, []),
    (movementController.DrivingState.TURN_RIGHT, [call.stopTurning(), call.turnLeft(20)]),
])
@patch("time.sleep", return_value=None)
@patch("src.controllers.movementController.movement")
def test_transferToLeft(mock_movement, mock_sleep, state, expected_calls):
    # Arrange
    movementController.currentDrivingState = state

    # Act
    movementController.transferToLeft(20)

    # Assert
    actual_calls = mock_movement.mock_calls
    assert actual_calls == expected_calls


@pytest.mark.parametrize("state,expected_calls", [
    (movementController.DrivingState.STOP, [call.turnRight(20)]),
    (movementController.DrivingState.FORWARD, [call.turnRight(20)]),
    (movementController.DrivingState.BACKWARD, []),
    (movementController.DrivingState.TURN_LEFT, [call.stopTurning(), call.turnRight(20)]),
    (movementController.DrivingState.TURN_RIGHT, []),
])
@patch("time.sleep", return_value=None)
@patch("src.controllers.movementController.movement")
def test_transferToRight(mock_movement, mock_sleep, state, expected_calls):
    # Arrange
    movementController.currentDrivingState = state

    # Act
    movementController.transferToRight(20)

    # Assert
    actual_calls = mock_movement.mock_calls
    assert actual_calls == expected_calls


@pytest.mark.parametrize("state,expected_calls", [
    (movementController.DrivingState.STOP, []),
    (movementController.DrivingState.FORWARD, [call.stopMoving()]),
    (movementController.DrivingState.BACKWARD, [call.stopMoving()]),
    (movementController.DrivingState.TURN_LEFT, [call.stopMoving()]),
    (movementController.DrivingState.TURN_RIGHT, [call.stopMoving()]),
])
@patch("time.sleep", return_value=None)
@patch("src.controllers.movementController.movement")
def test_transferToStop(mock_movement, mock_sleep, state, expected_calls):
    # Arrange
    movementController.currentDrivingState = state

    # Act
    movementController.transferToStop()

    # Assert
    actual_calls = mock_movement.mock_calls
    assert actual_calls == expected_calls
