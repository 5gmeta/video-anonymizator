# Testing image-anonymizator locally

This repository will guide the testing of the image anonymizator.

## Overview
This folder provides the guidelines to test functionality, performance and concurrency of the solution.

The different steps in terms of testing to accomplish are:

 1. Built the Docker of anonymization
 2. Run the AMQP message-broker to deliver signalling messages
 3. Run the sender application to send images to appropriate image topic
 5. Consume images from the **`image_anonym`** _topic_ from the message-broker


## Deployment

### Follow the steps for basic test

1. run the message-broker docker:

```
git clone git@github.com:5gmetadmin/message-data-broker.git
```
go to message-data-broker/src and
```
sudo docker-compose up -d
```

2. Deploy image anonymization docker

go to src/
```
$ docker build -t image-anonymizator .
```
run docker with environment variables AMQP_IP=YOUR_LOCAL_IP :
```
docker run -e AMQP_USER=5gmeta-user -e AMQP_PASS=5gmeta-password -e  AMQP_IP=192.168.10.9 -e AMQP_PORT=5673 -e TOPIC_READ=image -e TOPIC_WRITE=image_anonym -e INSTANCE_TYPE=small -ti image-anonymizator
```
3. push images to local message-broker

Images from sample_images are pushed to the image anoymizator

```
$ pip3 install -r requirements.txt
$ python3 simple_sender.py
```

3. Read anonymized images from message-broker (image_anonym topic)
```
$ python3 receiver.py
```
Images are saved to received folder



## Authors

* Josu Pérez ([jperez@vicomtech.org](mailto:jperez@vicomtech.org))
* Felipe Mogollón ([fmogollon@vicomtech.org](mailto:fmogollon@vicomtech.org))

## License

Copyright : Copyright 2022 VICOMTECH

License : Apache 2.0 ([http://www.apache.org/licenses/LICENSE-2.0.txt](http://www.apache.org/licenses/LICENSE-2.0.txt))

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


