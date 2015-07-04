# Pyverter
A simple, fast and lightweight Python Audio Converter for Windows, OS X and Linux.

# Build Instructions
Dependencies
============
Pyverter relies on:
- Python 3.X (Python 2.X will **not** work)
- PyDub
- Tkinter
- FFMPEG *or* AVCONV (FFMPEG is preferred if both are installed)

Keep in mind that you may choose between FFMPEG and AVCONV inside of the converter if you'd prefer to use one instead of the other.

Linux
=====
Debian-Based (Ubuntu)
------
On Debian-Based Linux Distrobutions, such as Ubuntu Linux, the following line will install all of the dependencies required to run the converter for you: `sudo apt-get install python3 python3-pip ffmpeg libav-tools python-tk && sudo pip3 install pydub`

If your distrobution also has `apt-get` installed, then the command will work also. I also recommend running `sudo apt-get update` to make sure all your installed packages are up to date.
Other
-----
On Other Linux distrobutions, you could try and install all the packages yourself through your own package manager. However, if you wish to build without the use of a package manager, please see the 'Compiling Yourself' section for links to all the packages, and pages on how to build them.

OS X
====
All dependencies apart from FFPMEG and AVCONV should be install for you on OS X.
Homebrew
--------
[Homebrew] (http://brew.sh) is a package manager for OS X. The following command will install FFMPEG: `brew install ffmpeg`. I'm unsure of  how to install AVCONV on OS X from Homebrew, however you could try running `brew install libav-tools`.

Manual
------
See the 'Compiling Yourself' section.

Windows
=======
To my knowledge, all packages have to be downloaded and install manually on Windows. Please see the 'Compiling Yourself' section.

Compiling Yourself
==================
If you wish to compile/install all packages yourself, or if you're running on Windows, download all the packages listed here:
- [Python 3] (https://www.python.org/downloads/) (Be sure to select the 3.X.X release)
- Pip ships with Python 2.7.9 and 3.4.X, However if you're running on a version < 3.4.X, see [this StackOverflow question] (http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows) for instructions
- Tkinter should ship with Python.
- [FFMPEG] (https://www.ffmpeg.org/download.html)
- [AVCONV] (https://libav.org/download.html)
