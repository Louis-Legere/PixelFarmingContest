Here is what happens when transitioning from one state to another with the **movementController.py** functions. You can see the **movement.py** functions that get called under the hood.

| From ↓ / To →  | FORWARD               | BACKWARD               | TURN_LEFT                  | TURN_RIGHT                  | STOP        |
| -------------- | --------------------- | ---------------------- | -------------------------- | --------------------------- | ----------- |
| **FORWARD**    | —                     | Stop → Backward        | StopTurning → TurnLeft     | StopTurning → TurnRight     | StopMoving  |
| **BACKWARD**   | Stop → Forward        | —                      | (optional) Stop → TurnLeft | (optional) Stop → TurnRight | StopMoving  |
| **TURN_LEFT**  | StopTurning → Forward | StopTurning → Backward | —                          | StopTurning → TurnRight     | StopTurning |
| **TURN_RIGHT** | StopTurning → Forward | StopTurning → Backward | StopTurning → TurnLeft     | —                           | StopTurning |
| **STOP**       | MoveForward           | MoveBackward           | TurnLeft                   | TurnRight                   | —           |
