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
# 192.168.15.181

import os
username=os.environ['AMQP_USER']
password=os.environ['AMQP_PASS']
server=os.environ['AMQP_IP']
port=os.environ['AMQP_PORT']
input_topic=os.environ['TOPIC_READ']

url='amqp://'+username+':'+password+'@'+server+':'+port+'/topic://'+input_topic
