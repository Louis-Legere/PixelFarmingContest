## How to set up the motors:

Hey future Fontys MINOR pixel farming group. Here is a guide on how to setup the motors so that they are able to move.

### Wiring

Here is an image of how to wire the ODESC 3.6 motor controller:
<br>
![wiringController](imgs/motorController.jpg) 
<br>
<br>
<br>
 **Note:** The power resister is Polarity-insensitive and the Quinder 8” 48V DC Brushless HUB motor already has encoders built in. 
<br> 
<br>
Here you can see an image of how the motors are connected (please excuse the wire colours):
![wiring](imgs/wiring.jpg)


### Configuration:

The ODESC might already be configured. If not, then please connect your pc to it with a micro usb-cable.

To configure the ODESC you need the odrivetool. It can be downloaded via python in your terminal with:
<br>
<br>
 `pip install odrive`
<br>
<br>
Once installed you can just write `odrivetool` in your command line. However after connecting the ODESC via usb you are likely to get this error:
![error](imgs/error.png)
**Note:** this error is normal for first time connecting
<br>
<br>
If that happens you can fix that by reinstalling your drivers with [Zadig](https://zadig.akeo.ie/). 
<br>
**IMPORTANT:** Check that you have the correct device listed before changing the driver. It should look something like this:
![Zadig](imgs/zadig.png)
<br>
Once you are successfully connected we strongly advise you to use our [config file](/workingSetupBothWheels.json). You can load it onto the ODESC by using the following command: 
<br>
`odrivetool restore-config configName.json`
<br>
**Note:** To run this command you have to be outside of the odrivetool.


