from libdw import pyrebase
import argparse
import time


def get_room_arg():
    ''' Get room name 
    if program is launched with -r argument, then use that,
    otherwise promote user to enter room name

    Returns:
        A str of name name
    '''
    # prepare for arguments parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--room")
    args = vars(ap.parse_args())
    room = args.get('room')

    # check if the program started with -r
    if room:
        print(f'Room name: {room}')
        return room
    # otherwise promote user
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
        ''' Get the pyrebase node instance that room/node refers to '''
        # if node unspecified, use the instance node as default
        if node is None:
            node = self._node
        # return the node instance
        return self.db.child(self.room).child(node)

    @property
    def val(self):
        ''' getter for the node value'''
        # check permission
        if not 'r' in self.mode:
            return
        return self.node().get().val()

    @val.setter
    def val(self, new_val):
        ''' setter for the node value
        Args:
            new_val: a serializable object that will be uploaded to firebase
        '''
        # check permission
        if not 'w' in self.mode:
            return
        self.node().set(new_val)

    def append(self, data, timestamp=None):
        ''' create a new child node using timestamp as key
        Args:
            data: a serializable object
            timestamp(optional): unix time as the key for new data, current time is used as default
        '''
        # check permission
        if not 'a' in self.mode:
            return
        # set timestamp to current time if unspecified
        if timestamp is None:
            timestamp = time.time()
        self.node().child(str(int(timestamp))).set(data)
