#!/bin/bash

DATE=$(date +"%Y-%m-%d-%H$%M")

fswebcam -r 1280x720 --no-banner ~/photos/$DATE.jpg

rsync --archive ~/photos/ ubuntu@10.1.5.72:~/Eagle-Eye/counter/images/photos/