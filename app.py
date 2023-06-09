import argparse

import mmif.serialize.model
from clams.app import ClamsApp
from clams.restify import Restifier
from mmif.vocabulary import DocumentTypes, AnnotationTypes
# For content-aware scene detection:
from scenedetect.detectors.content_detector import ContentDetector
from scenedetect.scene_manager import SceneManager
# Standard PySceneDetect imports:
from scenedetect.video_manager import VideoManager


class PyscenedetectWrapper(ClamsApp):
    def _appmetadata(self):
        pass

    def _annotate(self, mmif, **kwargs):
        config = self.get_configuration(**kwargs)
        for vd in mmif.get_documents_by_type(DocumentTypes.VideoDocument):
            scenes_output = self.run_sd(vd)  # scenes_output is a list of frame number interval tuples
            new_view = mmif.new_view()
            self.sign_view(new_view, config)

            contain = new_view.new_contain(AnnotationTypes.TimeFrame)
            contain.set_additional_property("timeUnit", "frame")
            for int_id, (start_frame, end_frame) in enumerate(scenes_output):
                annotation = new_view.new_annotation(AnnotationTypes.TimeFrame)
                annotation.add_property("start", start_frame)
                annotation.add_property("end", end_frame)
                annotation.add_property("frameType", "shot")
        return mmif

    @staticmethod
    def run_sd(video_document: mmif.serialize.Document):
        video_manager = VideoManager([video_document.location_path()])
        scene_manager = SceneManager()

        scene_manager.add_detector(ContentDetector())
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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", action="store", default="5000", help="set port to listen"
    )
    parser.add_argument("--production", action="store_true", help="run gunicorn server")
    # more arguments as needed
    # parser.add_argument(more_arg...)

    parsed_args = parser.parse_args()

    # create the app instance
    app = PyscenedetectWrapper()

    http_app = Restifier(app, port=int(parsed_args.port)
                         )
    if parsed_args.production:
        http_app.serve_production()
    else:
        http_app.run()
