![UALab logo](https://github.com/LingFengZhang24/lab_gui/blob/master/UALab.png)
--------------------------------------------------------------------------------

**UALab** *is a software to assist experimenters with hardware manipulation, data acquisition and analysis in the ultracold atom laboratory.*

- [More about UALab](#more-about-UALab)
- [Installation](#installation)
  - [Binaries](#binaries)
  - [From Source](#from-source(windows))
- [Getting Started](#getting-started)
- [Releases and Contributing](#releases-and-contributing)
- [The Team](#the-team)

## More about UALab
**UALab**(*Ultracold Atom Laboratory*) is a open source software developed by undergraduate and graduate students of **SCNU**(*South China Normal University*), the purpose of the software is to assist experimenters with hardware manipulation and data acquisition and analysis in the ultracold atom laboratory.

## Installation
### From Source(windows)

If you are installing from source, you can install [Anaconda](https://www.anaconda.com/distribution/) first.
And then create a new environment
```
conda create -n UALab python=3.6
conda activate UALab
```

#### Install Dependencies

Common
```
pip install pyqtgraph pyqt5 Pillow pathlib
```

#### Get the UALab Source
[download source code](https://github.com/LingFengZhang24/lab_gui.git)

#### Get hardware SDK and python libraries
**Camera Chameleon**

  hardware SDK: [FlyCapture](https://flir.app.boxcn.net/v/Flycapture2SDK/folder/73493389920)
  
  python library for Chameleon: [PyCapture](https://flir.app.boxcn.net/v/Flycapture2SDK/folder/73504933407)

#### Initialize UALab
```
python your_file_path/startProgram.py
```


## Getting Started

You can start with:
- [Wiki](https://github.com/LingFengZhang24/lab_gui/wiki)


## Releases and Contributing
...

## The Team
...

## License
See the [LICENSE](https://github.com/LingFengZhang24/lab_gui/blob/master/LICENSE) file for license rights and limitations (MIT).

