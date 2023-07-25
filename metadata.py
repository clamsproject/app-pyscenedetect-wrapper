"""
The purpose of this file is to define the metadata of the app with minimal imports. 

DO NOT CHANGE the name of the file
"""
import re

from mmif import DocumentTypes, AnnotationTypes

from clams.app import ClamsApp
from clams.appmetadata import AppMetadata


# DO NOT CHANGE the function name 
def appmetadata() -> AppMetadata:
    
    metadata = AppMetadata(
        name="Pyscenedetect Wrapper",
        description="CLAMS app wraps PySceneDetect and performs shot boundary detection on input videos",
        app_license="Apache2",
        identifier="pyscenedetect-wrapper",
        url="https://github.com/clamsproject/app-pyscenedetect-wrapper",
        analyzer_version=[l.strip().rsplit('==')[-1] for l in open('requirements.txt').readlines() if re.match(r'^scenedetect.*==', l)][0],
        analyzer_license="BSD-3",
    )
    metadata.add_input(DocumentTypes.VideoDocument)
    metadata.add_output(AnnotationTypes.TimeFrame, frameType='shot', timeUnit='frame')
    
    metadata.add_parameter(
        name='mode', 
        description='pick a scene detector algorithm, see http://scenedetect.com/projects/Manual/en/latest/cli/detectors.html',
        type='string',
        choices=['content', 'threshold', 'adaptive'],
        default='content'
    )
    metadata.add_parameter(
        name='threshold',
        description='threshold value to use in the detection algorithm. Note that the meaning of this numerical value differs for different detector algorithms.',
        type='number', 
        default=27.0,
    )
    return metadata


# DO NOT CHANGE the main block
if __name__ == '__main__':
    import sys
    metadata = appmetadata()
    for param in ClamsApp.universal_parameters:
        metadata.add_parameter(**param)
    sys.stdout.write(metadata.jsonify(pretty=True))
