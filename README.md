# TrackBot

TrackBot is an automated camera operator that is capable of tracking QR codes, human faces, upper and full human body in video streams. As soon as these features are detected in the video frames using OpenCV, the robot will start tracking them by moving its stepper motors accordingly, turning it into a real automatic cameraman, which can be used for several purposes.

### Features

  - Automatic camera tracking for QR codes, human faces, upper and full human bodies
  - On-demand video recording

### Software Requirements

  - Python 2.7.x
  - OpenCV 3.0 for Python

##### Python Dependencies:

  - [ZBar] (0.10)
  - [Pillow] (4.2.1)
  - [Flask] (0.12.2)
  - [Flask-SocketIO] (2.9.0)
  - [NumPy] (1.13.1)

##### OpenCV 3.0 for Python Installation:
  - [macOS Sierra: Install OpenCV 3.0 for Python]
  - [Ubuntu 16.04: Install OpenCV 3.0 for Python]

##### ZBar Installation:

   - Ubuntu 16.04: 
```sh
$ pip install zbar
```
   - macOS Sierra:
```sh
$ brew install zbar
$ LDFLAGS=-L/usr/local/lib/ CPATH=/usr/local/include/ pip install git+https://github.com/npinchot/zbar.git
```

### Hardware Requirements

   - NodeMCU ESP8266 with [MicroPython firmware]
   - One 4-wire stepper motor (two motors support is currently in development)
   - 3D printed TrackBot arm and case
   - 5V - 9V PSU/battery
   - Android phone

### Setup

   - Deploy files from folder [trackbot_mpy/](trackbot_mpy/) to your NodeMCU ESP8266
   - Setup your wifi ESP8266 AP interface (change ESSID and password) and reset the device
   - Connect your stepper motor (or motor driver) to NodeMCU pins: `[GPIO14, GPIO12, GPIO13, GPIO15]`
   - Connect your computer the ESP8266 AP network
   - Using a web browser open your ESP8266 gateway address (default: `192.168.4.1`)
   - Follow the instructions on the page
     - To execute the **TrackBot Server**:
        ```sh
        $ cd TrackBot-Robotics/
        $ FLASK_APP=main.py flask run
        ```

### License

See the [LICENSE](LICENSE.md) file for license rights and limitations (Apache License 2.0).

[//]: #
   [ZBar]: <https://pypi.python.org/pypi/zbar/0.10>
   [Pillow]: <https://pypi.python.org/pypi/Pillow/4.2.1>
   [Flask]: <https://pypi.python.org/pypi/Flask/0.12.2>
   [Flask-SocketIO]: <https://pypi.python.org/pypi/Flask-SocketIO/2.9.0>
   [NumPy]: <https://pypi.python.org/pypi/numpy/1.13.1>
   [macOS Sierra: Install OpenCV 3.0 for Python]: <http://www.pyimagesearch.com/2016/11/28/macos-install-opencv-3-and-python-2-7/>
   [Ubuntu 16.04: Install OpenCV 3.0 for Python]: <http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/>
   [MicroPython firmware]: <https://docs.micropython.org/en/latest/esp8266/index.html>
