import cv2
import pickle

from clams.serve import ClamApp
from clams.serialize import *
from clams.vocab import AnnotationTypes
from clams.vocab import MediaTypes
from clams.restify import Restifier

# Standard PySceneDetect imports:
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager

# For content-aware scene detection:
from scenedetect.detectors.content_detector import ContentDetector


class SceneDetection(ClamApp):

    def appmetadata(self):
        metadata = {"name": "Scene Detection",
                    "description": "This tool detects scenes using the pySceneDetect library.",
                    "vendor": "Team CLAMS",
                    "requires": [MediaTypes.V],
                    "produces": [AnnotationTypes.SCD]}
        return metadata

    def sniff(self, mmif):
        # this mock-up method always returns true
        return True

    def annotate(self, mmif):
        if type(mmif) is not Mmif:
            mmif = Mmif(mmif)
        video_filename = mmif.get_medium_location(MediaTypes.V)
        print (video_filename)
        scenes_output = self.run_sd(video_filename) #scenes_output is a list of frame number interval tuples

        new_view = mmif.new_view()
        contain = new_view.new_contain(AnnotationTypes.SCD)
        contain.producer = self.__class__

        for int_id, (start_frame, end_frame) in enumerate(scenes_output):
            annotation = new_view.new_annotation(int_id)
            annotation.start = str(start_frame)
            annotation.end = str(end_frame)
            annotation.attype = AnnotationTypes.SCD

        for contain in new_view.contains.keys():
            mmif.contains.update({contain: new_view.id})
        return mmif

    @staticmethod
    def run_sd(video_filename):
        # detect scenes
        ##type: (str) -> List[Tuple[FrameTimecode, FrameTimecode]]
        video_manager = VideoManager([video_filename])
        scene_manager = SceneManager()

        # Add ContentDetector algorithm (each detector's constructor
        # takes detector options, e.g. threshold).
        scene_manager.add_detector(ContentDetector())
        base_timecode = video_manager.get_base_timecode()

        scene_list = []
        try:
            # Set downscale factor to improve processing speed.
            video_manager.set_downscale_factor()

            # Start video_manager.
            video_manager.start()

            # Perform scene detection on video_manager.
            scene_manager.detect_scenes(frame_source=video_manager)

            # Obtain list of detected scenes.
            scene_list = scene_manager.get_scene_list(base_timecode)
            # Each scene is a tuple of (start, end) FrameTimecodes.
            scenes = map(lambda x: (x[0].get_frames(), x[1].get_frames()), scene_list)
            print (scenes)

        finally:
            video_manager.release()

        return scenes

if __name__ == "__main__":
    scd_tool = SceneDetection()
    scd_service = Restifier(scd_tool)
    scd_service.run()

