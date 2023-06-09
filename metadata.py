"""
The purpose of this file is to define the metadata of the app with minimal imports. 

DO NOT CHANGE the name of the file
"""
import re

from mmif import DocumentTypes, AnnotationTypes

from clams.appmetadata import AppMetadata


# DO NOT CHANGE the function name 
def appmetadata() -> AppMetadata:
    
    metadata = AppMetadata(
        name="Pyscenedetect Wrapper",
        description="",
        app_license="Apache2",
        identifier="pyscenedetect-wrapper",
        url="https://github.com/clamsproject/app-pyscenedetect-wrapper",
        analyzer_version=[l.strip().rsplit('==')[-1] for l in open('requirements.txt').readlines() if re.match(r'^scenedetect.*==', l)][0],
        analyzer_license="BSD-3",
    )
    metadata.add_input(DocumentTypes.VideoDocument)
    metadata.add_output(AnnotationTypes.TimeFrame, frameType='shot', timeUnit='frame')
    
    #todo 2020-12-01 kelleylynch incorporate option for threshold detector
    # metadata.add_parameter(name='a_param', description='example parameter description',
    #                        type='boolean', default='false')
    return metadata


# DO NOT CHANGE the main block
if __name__ == '__main__':
    import sys
    sys.stdout.write(appmetadata().jsonify(pretty=True))
