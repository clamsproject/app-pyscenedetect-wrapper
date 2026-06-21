# PySceneDetect Wrapper 

## Description
This CLAMS app wraps [PySceneDetect](https://pyscenedetect.readthedocs.io/en/latest/) and performs shot boundary detection on input videos.

A shot boundary is a place where one camera shot ends and another begins. The app detects shot boundaries and outputs a list of timestamps where the shot boundaries occur.

## User instruction

General user instruction for CLAMS apps is available at [CLAMS Apps documentation](https://apps.clams.ai/clamsapp).

### System requirements

The Python dependencies are installed from `requirements.txt`.
OpenCV (`cv2`) is pulled in automatically as a dependency of PySceneDetect (`opencv-python`), so you do not install OpenCV yourself.

The `opencv-python` wheel does, however, link against two OS-level shared libraries that it does not bundle, so they must be present on the host:

* `libGL.so.1` (OpenGL) -- on Debian/Ubuntu, `apt-get install -y libgl1`
* `libgthread-2.0.so.0` (GLib) -- on Debian/Ubuntu, `apt-get install -y libglib2.0-0`

The provided `Containerfile` already installs both, so this only matters when running the app outside the container (e.g. bare-metal development).

### Configurable runtime parameter

Although all CLAMS apps are supposed to run as *stateless* HTTP servers, some apps can configured at request time using [URL query strings](https://en.wikipedia.org/wiki/Query_string). For runtime parameter supported by this app, please visit [CLAMS App Directory](https://apps.clams.ai) and look for the app name and version. 
