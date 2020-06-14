# 20³ <img align="left" width="50" height="50" src="https://i.ibb.co/L1Q5t4w/output-onlinepngtools.png">

A System Tray app that provides a reminder to follow the 20/20/20 rule.

## Description
It's recommended to abide by the 20/20/20 rule when looking at a screen | or in other words: 

Every **20 minutes** take a break for **20 seconds** to look at something **20 feet** away. 
[More info here.](https://www.healthline.com/health/eye-health/20-20-20-rule)

When using similar apps I found I would frequently not notice the notification or sometimes just ignore it altogether. In an attempt to strike a balance between being annoying enough to grab the users attention and not blocking any functionality, when it's time to look away and let your eyes rest 20³ will fade the users screen in and out for the entire duration.

## Installation

```PowerShell
> git clone https://github.com/Tbruno25/twenty_cubed
# cd into the twenty_cubed directory 
> pip install -r requirements.txt
```

## Usage

Double click 20³.pyw or execute
```Powershell
> python 20³.pyw
```
The app should now be launched in your System Tray. 

**Left clicking** the app icon will toggle it's current state:

![##009b2f](https://via.placeholder.com/15/009b2f/000000?text=+) Green is ***active***

![##9c0404](https://via.placeholder.com/15/9c0404/000000?text=+) Red is ***paused***

While active every 20 minutes the screen will alternate fading as a reminder to look away.

<p align="center">
<img src="https://i.ibb.co/g6wFnVz/demo.gif">
</p

**Right clicking** will bring up a menu to exit the app.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
