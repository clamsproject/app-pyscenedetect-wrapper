import argparse

import mmif.serialize.model
import logging
from clams.app import ClamsApp
from clams.restify import Restifier
from mmif.vocabulary import DocumentTypes, AnnotationTypes
from mmif.utils import video_document_helper as vdh
from scenedetect import (
    open_video,
    SceneManager,
    ContentDetector,
    ThresholdDetector,
    AdaptiveDetector,
)


class PyscenedetectWrapper(ClamsApp):

    def __init__(self):
        super().__init__()
        
    def _appmetadata(self):
        pass

    def _annotate(self, mmif, **kwargs):
        config = self.get_configuration(**kwargs)
        for vd in mmif.get_documents_by_type(DocumentTypes.VideoDocument):
            # scenes_output is a list of (start_ms, end_ms) interval tuples
            scenes_output = self.run_sd(vd, config['mode'], config['threshold'])
            new_view = mmif.new_view()
            self.sign_view(new_view, kwargs)

            new_view.new_contain(AnnotationTypes.TimeFrame, timeUnit="milliseconds", document=vd.id)
            for int_id, (start_ms, end_ms) in enumerate(scenes_output):
                annotation = new_view.new_annotation(AnnotationTypes.TimeFrame)
                annotation.add_property("start", start_ms)
                annotation.add_property("end", end_ms)
                annotation.add_property("label", "shot")
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
        # used to use get_frames (in SD 0.6 era). 0.7 provide better PTS-accurate
        # timecode as canonical timestamps, so we're just uing them
        fps = vdh.get_framerate(video_document)
        scenes = map(
            lambda x: (vdh.convert(x[0].seconds, 's', 'ms', fps),
                       vdh.convert(x[1].seconds, 's', 'ms', fps)),
            scene_list)
        return scenes


def get_app():
    return PyscenedetectWrapper()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", action="store", default="5000", help="set port to listen")
    parser.add_argument("--production", action="store_true", help="run gunicorn server")

    parsed_args = parser.parse_args()

    app = get_app()

    http_app = Restifier(app, port=int(parsed_args.port))
    if parsed_args.production:
        http_app.serve_production()
    else:
        app.logger.setLevel(logging.DEBUG)
        http_app.run()
