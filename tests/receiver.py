#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import print_function

from proton.handlers import MessagingHandler
from proton.reactor import Container
import base64
import os
counter = 0

class Receiver(MessagingHandler):
    def __init__(self, url, messages_to_receive=10):
        super(Receiver, self).__init__()
        self.url = url
        self._messages_to_receive = messages_to_receive
        self._messages_actually_received = 0
        self._stopping = False

    def on_start(self, event):
        event.container.create_receiver(self.url)

    def on_message(self, event):
        global counter
        if self._stopping:
            return
        image_name="received/received_image_"+str(counter)+".jpg"
        print("Saved "+image_name)
        with open("received/received_image_"+str(counter)+".jpg", "wb") as fh:
            fh.write(base64.decodebytes(event.message.body))
        self._messages_actually_received += 1
        if self._messages_actually_received == self._messages_to_receive:
            event.connection.close()
            self._stopping = True
        counter += 1

    def on_transport_error(self, event):
        raise Exception(event.transport.condition)


if __name__ == "__main__":
    try:
        os.mkdir('received')
    except:
        pass
    try:
        Container(Receiver('amqp://5gmeta-user:5gmeta-password@127.0.0.1:5673/topic://image_anonym')).run()
    except KeyboardInterrupt:
        pass
    
