import unittest
import unittest.mock as mock
import os, sys
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import models


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_RESPONSE = 'response'

KEY_ANSWER = 'answer'
KEY_QUESTION = 'question'
KEY_ROOM = 'room'
KEY_DATA = 'data'

KEY_CURRENT_CONNECTIONS_DB = 'curr_con'
KEY_SID = 'request_sid'
KEY_NUM_ADDITIONS =  'times_in_database'

KEY_EMIT_ID = 'emit_id'
KEY_EMIT_ROOM = 'room'

class MockedFlashCards:
    answer = ''
    question = ''
    room = ''
    def __init__(self, question, answer, room):
        self.answer = answer
        self.question = question
        self.room = room
        
class testEmitFlashCards(unittest.TestCase):
     def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 
                    {
                    KEY_EMIT_ID: 'cards',
                    KEY_DATA: [{'question' : 'question', 'answer': 'answer'}],
                    KEY_SID: '123456789ABCDEF'
                    },
                KEY_EXPECTED: ('2+2', 4, '123456789ABCDEF') 
                },
        ]
 
        self.hold = ''
            
     def mock_emit(self, sid, data, room='default'):
        self.hold = {KEY_EMIT_ID: sid, KEY_DATA: data, KEY_EMIT_ROOM: room}
    
     def mocked_cards(self):
         return [MockedFlashCards('question', 'answer', '123456789ABCDEF')]
     @mock.patch('app.flask')
     def test_emit_cards_success(self, mock_flash):
        session = UnifiedAlchemyMagicMock()
        for test in self.success_test_params:
            mock_flash.request.sid = test[KEY_INPUT][KEY_SID]
            
            with mock.patch("models.DB.session", session):
                session.query(models.Flashcards).all.return_value = self.mocked_cards()
                with mock.patch("flask_socketio.SocketIO.emit", self.mock_emit):
                    print(app.emit_flashcards(test[KEY_INPUT][KEY_DATA]))
        
               

    
if __name__ == "__main__":
    unittest.main()