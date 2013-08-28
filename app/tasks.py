from __future__ import absolute_import
from app.celery import celery
from app.libs.audio.play import Play
from app.libs.rtp.rx import RTPreceiver
from app.libs.rtp.tx import RTPtransmitter
from gi.repository import Gst
import redis
import urllib3

http = urllib3.PoolManager()

@celery.task
def add(x, y):
    return x + y


@celery.task
def sync_peers():
    return True


@celery.task
def rtp_tx():
    transmitter = RTPtransmitter(audio_device="hw:2", ipv6=False, receiver_address='127.0.0.1')
    transmitter.run()
    while True:
        Gst.Bus.poll(transmitter.pipeline.get_bus(), 0, 1)
        time.sleep(1)
    return True


@celery.task
def rtp_rx():
    caps = "application/x-rtp,media=(string)audio,clock-rate=(int)48000,encoding-name=(string)X-GST-OPUS-DRAFT-SPITTKA-00"
    receiver = RTPreceiver(caps=caps, audio_device='hw:2', ipv6=False)
    receiver.run()
    while True:
        Gst.Bus.poll(receiver.pipeline.get_bus(), 0, 1)
        time.sleep(1)
    return True


@celery.task
def play_audio():
    store = redis.Redis('127.0.0.1')
    store.setex('lock_play_audio', 'true', '30')
    player = Play()
    player.run()
    player.loop()
    store.setex('lock_play_audio', 'false', '30')
    return True


@celery.task
def api_peer_status(host):
    requests.get('http://['+host+']/api1/peer_status')
    return True


@celery.task
def api_peer_invite(host):
    r = http.request('GET', 'http://['+host+']:5000/api1/peer_status')
    return True
