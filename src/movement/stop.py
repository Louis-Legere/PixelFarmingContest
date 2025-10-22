import odrive

odrv0 = odrive.find_any()

odrv0.axis0.controller.input_vel = 0
odrv0.axis1.controller.input_vel = 0