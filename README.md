# BOS-Python
## A simple script that can visualize airflows! 💨 

EXAMPLE: Visualising the invisible airflow created by a candle.🔥 
![alt text](https://github.com/Adrian-Winter/BOS-Python-/blob/main/app_in_action.gif)

## What is BOS? 🧐
This little tool lets you visualize currents by using the Background-oriented-schlieren-Technique or short BOS. BOS utilizes the phenomenon that if a local gas current is present, a local in density gradient can be found as well. Mediums with different densities distort light in a differently, therefore a pixel shift can be detected where a change in density is present. Notice that the change in density can have multiple causes such as a change in temperature and does not solely represent the flow of a gas.

![alt text](https://www.dlr.de/as/en/Portaldata/5/Resources/images/abteilungen/abt_ev/artikel/BOS_en_img1.jpg)

## How to use this application? ⚙️

### In order to use this script you need:

* A smartphone with a camera or an IP Webcam 
* A tripod or selfie-stick for your smartphone
* A printer or a second screen for your computer
* Some kind of flow you want to visualize

For this setup you need to download an App that lets you turn your smartphone into a IP webcam. I used the IP webcam app for android: 
(https://play.google.com/store/apps/details?id=com.pas.webcam&hl=de&gl=US)

___Before you execute the script you need to start the IP webcam server on your smartphone and replace the IP address "yourIP" in the script with your actual IP address that is displayed within the IP webcam App.___

To start the app, simply launch the script "BOS-Python".
To start displaying the current airflow a reference image need to be recorded first.

* ___PRESS c___ to record a new reference image. This can be done multiple times during runtime and is very useful while changing the setup. 
* ___PRESS q___ to quit the app. 

## Experiment setup 

### Background 
You can use every static surface as a background as long as it has lots of detail and variety. I recommend using the random background pattern that I provided: https://github.com/Adrian-Winter/BOS-Python-/blob/main/random_Background.png
You can either print it or display it on a second screen. 

### Camera
Make sure your smartphone is steady and the focus is set on the background, not the source of the flow you want to visualize! 

### Flow source 
Best results can be achieved if the layer that contains the flow you want to visualize is closer to the camera then to the background. To achieve bigger deflection the distance between the camera and the background shall be decreased while the distance between the flow and the background shall be increased. Both factor have practical limitations. For a detailed explanation check out this paper: https://e-pub.uni-weimar.de/opus4/frontdoor/deliver/index/docId/4697/file/BOS_for_visualization_of_indoor_airflow.pdf


The experiment setup should look something like this:
![alt text](https://github.com/Adrian-Winter/BOS-Python-/blob/main/experiment_setup.jpg)

## Parameters & GUI 
To detect the airflow the current frame of the video stream is compared to a reference image using the __absdiff__ form the cv2 package. Then the resulting difference image needs some post processing, so that a clear visualization can be presented for different setups. To achive that a GUI is implemented to easily adjust the parameters during runtime. 

* __ALPHA__ multiplies the difference image by a factor to emphasize or diminish the global intensity. (Weaker flows need a higher ALPHA)
* __GRIDSIZE__ defines the resolution of the grid that can be used to get rid of unwanted small pixel shifts. The higher the GRIDSIZE the more computing intese!
* __THRESHWINDOWFILTER__ sets the threshold that the mean value of a grid cell needs so pass, in order to be not set to 0. 
* __THRESH__ sets the threshold of the global image that a pixel shift needs to surpass to be displayed. (To filter out unwanted noise)
* __OVERLAY__ * can be used to overlay the reference Image onto of the difference image. 
* __AUTOREFFERENCEINTERVALL__ sets how fast the next reference image shall be taken. (Useful when turbulent flow is present)
* __AutoReferenceImage__ activates the automatic update of the reference image. 


## Feedback 
* Please feel free to let me know if you have trouble getting the results you are looking for. 
* Also what features could be added? 

### Hope this little app made your project a little bit easier! ☺️



