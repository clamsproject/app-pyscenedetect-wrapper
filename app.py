import argparse

import mmif.serialize.model
import logging
from clams.app import ClamsApp
from clams.restify import Restifier
from mmif.vocabulary import DocumentTypes, AnnotationTypes
# detection algorithms
from scenedetect.detectors.content_detector import ContentDetector
from scenedetect.detectors.threshold_detector import ThresholdDetector
from scenedetect.detectors.adaptive_detector import AdaptiveDetector
from scenedetect.scene_manager import SceneManager
# Standard PySceneDetect imports:
from scenedetect import open_video


class PyscenedetectWrapper(ClamsApp):

    def __init__(self):
        super().__init__()
        
    def _appmetadata(self):
        pass

    def _annotate(self, mmif, **kwargs):
        config = self.get_configuration(**kwargs)
        for vd in mmif.get_documents_by_type(DocumentTypes.VideoDocument):
            # scenes_output is a list of frame number interval tuples
            scenes_output = self.run_sd(vd, config['mode'], config['threshold'])
            new_view = mmif.new_view()
            self.sign_view(new_view, kwargs)

            contain = new_view.new_contain(AnnotationTypes.TimeFrame)
            contain.set_additional_property("timeUnit", "frame")
            for int_id, (start_frame, end_frame) in enumerate(scenes_output):
                annotation = new_view.new_annotation(AnnotationTypes.TimeFrame)
                annotation.add_property("start", start_frame)
                annotation.add_property("end", end_frame)
                annotation.add_property("frameType", "shot")
        return mmif

    @staticmethod
    def run_sd(video_document: mmif.serialize.Document, mode: str, threshold: float):
        video = open_video(video_document.location_path())
        scene_manager = SceneManager()
        if mode.lower() == 'content':
            scene_manager.add_detector(ContentDetector(threshold=threshold))
        elif mode.lower() == 'threshold':
            scene_manager.add_detector(ThresholdDetector(threshold=threshold))
        elif mode.lower() == 'adaptive':
            scene_manager.add_detector(AdaptiveDetector(adaptive_threshold=threshold))

        scene_manager.detect_scenes(video=video, show_progress=True)
        scene_list = scene_manager.get_scene_list()
        scenes = map(lambda x: (x[0].get_frames(), x[1].get_frames()), scene_list)
        return scenes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", action="store", default="5000", help="set port to listen")
    parser.add_argument("--production", action="store_true", help="run gunicorn server")

    parsed_args = parser.parse_args()

    # create the app instance
    app = PyscenedetectWrapper()

    http_app = Restifier(app, port=int(parsed_args.port))
    # for running the application in production mode
    if parsed_args.production:
        http_app.serve_production()
    # development mode
    else:
        app.logger.setLevel(logging.DEBUG)
        http_app.run()
