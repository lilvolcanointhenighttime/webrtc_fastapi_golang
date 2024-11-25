import uuid

from fastapi import APIRouter, Request

from .schemas import OfferSchema
from .utils import (
    RTCSessionDescription, RTCPeerConnection,
    RTCPeerConnection, RTCSessionDescription,
    AudioTransformTrack, VideoTransformTrack,
    logger,
    relay,
    pc_dict,
    video_streams,
    audio_streams
    )


webrtc_router = APIRouter(
    prefix="/webrtc",
    tags=["HeadHunder"]
)

@webrtc_router.post("/offer")
async def offer(request: OfferSchema):
    data: dict = request.__dict__
    name = data["name"]
    sdp=data["sdp"]
    type=data["type"]

    offer = RTCSessionDescription(sdp=sdp, type=type)

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pc_dict[pc] = [name, pc_id]

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    if audio_streams:
        for _, track in audio_streams.items():
            track = AudioTransformTrack(relay.subscribe(track), transform=None)
            pc.addTrack(track)

    if video_streams:
        for _, track in video_streams.items():
            track = VideoTransformTrack(relay.subscribe(track), transform=None)
            pc.addTrack(track)

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])

            if isinstance(message, dict):
                ...


    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        log_info("Connection state is %s", pc.connectionState)
        if pc.connectionState == "closed" or pc.connectionState == "failed":
            await pc.close()
            if name in audio_streams.values():
                del audio_streams[name]
            if name in video_streams.values():
                del video_streams[name]
            del pc_dict[pc]
            return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type, "name": name}

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        if track.kind == "audio":
            track = AudioTransformTrack(relay.subscribe(track), transform=None)
            audio_streams.update({name: track})
            pc.addTrack(track)

        elif track.kind == "video":
            track = VideoTransformTrack(relay.subscribe(track), transform=None)
            video_streams.update({name: track})
            pc.addTrack(track)


    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type, "name": name}
