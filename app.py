from clams.serve import ClamsApp
from clams.restify import Restifier
from mmif.vocabulary import DocumentTypes, AnnotationTypes

# Standard PySceneDetect imports:
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager

# For content-aware scene detection:
from scenedetect.detectors.content_detector import ContentDetector

APP_VERSION = 0.1


class SceneDetection(ClamsApp):
    def setupmetadata(self):
        metadata = {"name": "Shot Detection",
                    "description": "This tool detects shots using the PySceneDetect library.",
                    "vendor": "Team CLAMS",
                    "iri": f"http://mmif.clams.ai/apps/pyscenedetect/{APP_VERSION}",
                    "requires": [DocumentTypes.VideoDocument],
                    "produces": [AnnotationTypes.TimeFrame]}
        return metadata

    def sniff(self, mmif):
        ##todo 2020-12-29 kelleylynch implement sniff method
        return True

    def annotate(self, mmif):
        scenes_output = self.run_sd(mmif) #scenes_output is a list of frame number interval tuples

        new_view = mmif.new_view()
        new_view.metadata['app'] = self.metadata["iri"]

        contain = new_view.new_contain(AnnotationTypes.TimeFrame, {"unit":"frame"})
        contain.producer =  "app-scene-detect" ##todo 2020-12-29 kelleylynch un-hardcode this

        for int_id, (start_frame, end_frame) in enumerate(scenes_output):
            annotation = new_view.new_annotation(f"sh_{int_id}", AnnotationTypes.TimeFrame)
            annotation.add_property("start", start_frame)
            annotation.add_property("end", end_frame)
        return mmif

    @staticmethod
    def run_sd(mmif):
        video_manager = VideoManager([mmif.get_document_location(DocumentTypes.VideoDocument)])
        scene_manager = SceneManager()

        scene_manager.add_detector(ContentDetector())
        ##todo 2020-12-01 kelleylynch incorporate option for threshold detector
        base_timecode = video_manager.get_base_timecode()

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

        finally:
            video_manager.release()

        return scenes

if __name__ == "__main__":
    tool = SceneDetection()
    service = Restifier(tool)
    service.run()
