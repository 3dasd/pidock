# 3dasd Raspbian image builder

This was forked from [pidock](https://github.com/eringr/pidock). See the original readme there.

## Usage

> See the original readme for prerequisites: https://github.com/eringr/pidock

Download a base Raspbian image from https://www.raspberrypi.org/software/
and place it into the root of the repo as `raspbian.img`.

Run the following replacing `YOUR-DEVICE` with your SD card's device:

```sh
./pidock.py all --dev /dev/YOUR-DEVICE
```

## Advanced usage

The "official" image doesn't include any Wifi settings but you could bake
your network details into the image with:

```sh
./pidock.py all --dev /dev/YOUR-DEVICE --wpa-ssid YOUR-SSID --wpa-pass YOUR-PASSWORD
```

> Warning! These will also show up in the standard output of the pidock process, be
careful if you're saving that log!