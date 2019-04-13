from libdw import pyrebase
import argparse
import time


def get_room_arg():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--room")
    args = vars(ap.parse_args())
    room = args.get('room')

    if room:
        print(f'Room name: {room}')
        return room

    return input('Room name: ')


class FireBaseNode():
    # unique token used for authentication
    API_KEY = 'AIzaSyCNUpvYKV3VvBqQxdzGhRDfmPemHK8MYxY'
    # URL to Firebase database
    DATABASE_URL = 'https://eagle-eye-c1e58.firebaseio.com/'

    def __init__(self, node, room=None, mode='rw'):
        # Get room name if unspecified
        if not room:
            room = get_room_arg()

        # Connect to database
        self.db = pyrebase.initialize_app({
            "apiKey": self.API_KEY,
            "databaseURL": self.DATABASE_URL
        }).database()

        # Save arguments
        self._node = node
        self.room = room
        self.mode = mode

        # Check if room exists
        if not self.node('Name').get().val():
            print('Room does not exist')
            exit(-1)

    def node(self, node=None):
        if node is None:
            node = self._node
        return self.db.child(self.room).child(node)

    @property
    def val(self):
        if not 'r' in self.mode:
            return
        return self.node().get().val()

    @val.setter
    def val(self, new_val):
        if not 'w' in self.mode:
            return
        self.node().set(new_val)

    def append(self, data, timestamp=None):
        if not 'a' in self.mode:
            return
        if timestamp is None:
            timestamp = time.time()
        self.node().child(str(int(timestamp))).set(data)
