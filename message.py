import json
import time

class Message(object):
    """
    @param:type:join,leave,msg
    """

    def __init__(self, type, content, sender, datetime=""):
        self.type = type
        self.content = content
        self.sender = sender
        if datetime == "":
            self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            self.time = datetime

    def serialize(self):
        msg = {"type": self.type, "content": self.content, "sender": self.sender, "time": self.time}
        return json.dumps(msg)

    @staticmethod
    def deserialize(msg):
        msg = json.loads(msg)
        return Message(msg['type'], msg['content'], msg['sender'], msg['time'])
