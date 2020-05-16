import json


class Message(object):
    """
    @param:type:join,leave,msg
    """

    def __init__(self, type, content, sender):
        self.type = type
        self.content = content
        self.sender = sender

    def serialize(self):
        msg = {"type": self.type, "content": self.content, "sender": self.sender}
        return json.dumps(msg)

    @staticmethod
    def deserialize(msg):
        msg = json.loads(msg)
        return Message(msg['type'], msg['content'], msg['sender'])
