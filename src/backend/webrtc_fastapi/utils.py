import logging
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaRecorder, MediaRelay

logger = logging.getLogger("pc")
pc_dict = dict()
relay = MediaRelay()
video_streams = {}
audio_streams = {}

class AudioTransformTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self, track, transform=None):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        return frame

class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, transform=None):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        return frame
