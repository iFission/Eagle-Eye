#!/bin/bash

DATE=$(date +%s)
let DATE=$DATE/60*60

fswebcam -r 1280x720 --no-banner ~/photos/$DATE.jpg

rsync --archive -e "ssh -i ~/.ssh/ALEX-HERMES" ~/photos/ ubuntu@10.1.5.72:~/Eagle-Eye/counter/images/photos/