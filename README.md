# Eagle-Eye

Repo for 10.009 Digital World 1D IoT project

Team: F06 Group1 (International Design Centre)

Project Lead: heyuhang0  
Data Analytics Specialist: Shangzewen  
UI/UX Specialist: Jiazheng411  
IoT Specialist: ERJoseJohnson  
Computer Vision Specialist: iFission

## To run

### Raspberry Pi

requirements:

* libdw
* numpy
* pyaudio
* sklearn

#### sound meter

`python3 sound_meter.py [-r ROOMNAME]`

#### predictor

`python3 predictor.py [-r ROOMNAME]`

#### photo capturer

`cd counter; ./capture_photos.sh`

### OpenCV Server

requirements:

* jupyter
* opencv-python
* pprint
* PIL
* tqdm
* numpy

Run counter/counter.py in jupyter notebook

### App

#### To run on Windows/Mac/Linux

requirements:

* kivy
* requests
* openssl

`cd App; python main.py`

#### To build for android

```
cd App
git clone https://github.com/kivy/buildozer.git
cd buildozer
sudo python2.7 setup.py install
buildozer android debug deploy run
```