# YoutubeChatWatcher.py
# 202203~

from ast import arg
import time
import pytchat
from pythonosc import udp_client, osc_message_builder
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--videoID", default="sRbzjQTxvPE",
                    help="Youtube VideoID")
parser.add_argument("--ip", default="127.0.0.1", 
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=7000, 
                    help="The port the OSC server is listening on")
parser.add_argument("--address", default="/chat", 
                    help="OSC Address. Insert / at begin!")
args = parser.parse_args()

client = udp_client.UDPClient(args.ip, args.port)

chat = pytchat.create(video_id=args.videoID)
print("--- watching "+str(args.videoID)+" ---")
while chat.is_alive():
    for c in chat.get().sync_items():
        print(f"{c.datetime}\t[{c.author.name}]\t{c.message}")
        msg = osc_message_builder.OscMessageBuilder(args.address)
        msg.add_arg(c.datetime)
        msg.add_arg(c.author.name)
        msg.add_arg(c.message)
        m = msg.build()
        client.send(m)
        time.sleep(1)

print("fin")