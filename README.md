# PySceneDetect Wrapper 

## Description
This CLAMS app wraps [PySceneDetect](https://pyscenedetect.readthedocs.io/en/latest/) and performs shot boundary detection on input videos.

A shot boundary is a place where one camera shot ends and another begins. The app detects shot boundaries and outputs a list of timestamps where the shot boundaries occur.

## User instruction

General user instruction for CLAMS apps is available at [CLAMS Apps documentation](https://apps.clams.ai/clamsapp).

### System requirments

* [OpenCV](https://opencv.org/)
    * To install OpenCV on your system, please refer to the [official documentation](https://docs.opencv.org/4.x/df/d65/tutorial_table_of_content_introduction.html).

### Configurable runtime parameter

Although all CLAMS apps are supposed to run as *stateless* HTTP servers, some apps can configured at request time using [URL query strings](https://en.wikipedia.org/wiki/Query_string). For runtime parameter supported by this app, please visit [CLAMS App Directory](https://apps.clams.ai) and look for the app name and version. 
