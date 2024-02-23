# Examples

This document guides the integration purposes include a readme with scenario and pre-conditions, and scripts/Dockers

## Scenario

A video sensor wants to push a UDP video stream including a RTP video with H264 which has to be anonymised by the MEC platform

## Pre-Conditions

The following systems must be configured and running:

- The Message Broker (AMQP) is running and ready in the MEC infrastructure which has been previously registered in the Discovery at the Cloud EKS
- The Video Stream Broker (WebRTC Proxy) is running and ready in the MEC infrastructure
- The Kakfa Broker (KAFKA) is running and ready at Cloud EKS and pulling data through Kafka Connector and KSQLDB from AMQP
- The Video Anonymizator is running and ready in the MEC infrastructure
- The component for the Video Sensor is built but not running

## Push a UDP Source

First, we need a UDP SOURCE:

	gst-launch-1.0 filesrc location="/5GMETA/video-anonymizator/processor/res/testimg/input/RecFile_2_20220405_095958_EthCamMJPEG_1_oImageLeft_0.jpg" ! decodebin ! imagefreeze ! video/x-raw, framerate=1/1 ! videoconvert ! videoscale ! video/x-raw, width=320, height=240, framerate=2/1 ! textoverlay font-desc="Arial 40px" text="container TX" valignment=2 ! timeoverlay font-desc="Arial 60px" valignment=2 ! videoconvert ! tee name=t ! queue max-size-buffers=1 ! x264enc bitrate=2000 speed-preset=ultrafast tune=zerolatency key-int-max=5 ! video/x-h264,profile=constrained-baseline,stream-format=byte-stream ! h264parse config-interval=-1 ! rtph264pay pt=96 config-interval=-1 name=payloader ! application/x-rtp,media=video,encoding-name=H264,payload=96 ! udpsink host=127.0.0.1 port=7000 enable-last-sample=false send-duplicates=false

> use an image path already in the repository such as `"video-anonymizator/processor/res/testimg/input/RecFile_2_20220405_095958_EthCamMJPEG_1_oImageLeft_0.jpg"` \
> framerate=2/1 is set accordingly to the `"dataSampleRate": 2.0,` defined @ video_sensor.py \
> source in the free PORT 7000

Second, we need to run the Video Sensor Docker:

	docker run  --net=host --env AMQP_USER="<user>" --env AMQP_PASS="<password>" --env VIDEO_SOURCE="udp" --env VIDEO_PARAM="7000" --env VIDEO_TTL="300" 5gmeta/video_sensor

 _Remember to configure the `<user`> and `<password`> to your local environment_

> Remember to update the `video_sensor.py` code of the Docker including the employed framerate `"dataSampleRate": 2.0,` \
> Note that 7000 is the UDP source Port \
> Note that 100 is the timeout until the Video Sensor will stop sending a video stream

Third, we can play the video from the 5GMETA MEC infrastructure, checking data pipeline at the 5GMETA MEC infrastructure is processing and anonymising data, from the Local Consume of the AMQP Source

> Note that 23 is the provided ID (from the registration process)

 - change amqp2video.py code to get the target ID

	if (event.message.properties['sourceId'] == 23):

> Note that 23 should be changed to the dataflow ID identified in the logs coming from registration and WebRTC proxy logs

 - launch the player

	AMQP_USER="<user>" AMQP_PASS="<password>" AMQP_IP="<AAA.BBB.CCC.DDD>" AMQP_PORT="<port>" GST_DEBUG=3 python3 ./amqp2video.py

 _Remember to configure the `<user`>, `<password`>, `<AAA.BBB.CCC.DDD`> and `<port`> to your local environment_

> Note that _AAA.BBB.CCC.DDD_ is the IP address of the AMQP message_broker

