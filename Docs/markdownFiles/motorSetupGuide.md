## How to set up the motors:

Hey future Fontys MINOR pixel farming group. Here is a guide on how to setup the motors so that they move.

#### Wiring

Here is an image of how to wire the ODESC 3.6 motor controller:
![wiringController](imgs/motorController.jpg) 
<br>
The power resister is Polarity-insensitive. 
Note that the Quinder 8” 48V DC Brushless HUB motor already has encoders build in. <br>
Here you can see an image of how the motors are connected (pls excuse the wire colour):
![wiring](imgs/wiring.jpg)


#### Configuration:

The ODESC might already be configured. If not then please connect your pc to it with a micro usb-cable.

To configure the ODESC you need the odrivetool. It can be downloaded via python. Once installed you can just write "odrivetool" in your command line. However after connecting the ODESC via usb you are likely to get this error:
![error](imgs/error.png)
If that happens you can fix that by reinstalling your drivers with [Zadig](https://zadig.akeo.ie/). <br>
IMPORTANT: Check that you have the correct device listed before changing the driver. It should look something like this:
![Zadig](imgs/zadig.png)
<br>
Once you are successfully connected I strongly advise you to use our [config file](workingSetupBothWheels.json). You can load it onto the ODESC by using the following command: <br>
"odrivetool restore-config configName.json"
<br>


