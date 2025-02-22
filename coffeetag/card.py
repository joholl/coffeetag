import threading
import time

import smartcard
import smartcard.CardRequest

NFC_GET_UUID = bytes.fromhex('ff ca 00 00 00')


class Card(threading.Thread):
    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio

    def run(self):
        while True:
            try:
                request = smartcard.CardRequest.CardRequest(timeout=100, newcardonly=True)
                service = request.waitforcard()
                service.connection.connect()
                uuid = bytes(service.connection.transmit(list(NFC_GET_UUID))[0])
                self.socketio.emit('card_connected', data=dict(tag=uuid.hex()))
                time.sleep(2)
                service.connection.disconnect()
            except:
                continue
