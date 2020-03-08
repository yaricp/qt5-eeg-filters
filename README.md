# qt5-eeg-filters

GUI for eeg-filters based on Qt5.

## Requirements

Program require python >= 3.6, python3-venv, and Qt5.
Tested on Ubuntu 18.04.

The following pip packages are required (see Installation):

* eeg-filters
* pyQt5
* pyqtgraph

Note: Make sure you have Qt5 installed on your system.

## Installation



```
$ git clone https://github.com/yaricp/qt5-eeg-filters.git
$ cd qt5-eeg-filters/
$ ./install.sh
```

`install.sh` will download and set up necessary packages in a venv.

## Usage

To start the program, run:

```
$ ./start.sh
```

After that you will see the main window of program.

You can open a file with EEG signals data.
This file you can get from NeuroExplorer4.4 by exporting data to ASCII format.

When curves are showed on the main plot you can apply a filter by choosing bandwith in the list of bandwidths.

You can move regions with mouse for searching extremums. Also you can change boundaries of these regions by means of text fields over the main graph.

You can save any stage of your reseach in a folder of your selection.


## Settings

Main settings are set in `settings.py` in the program folder.

You can set default list of bandwiths and boundaries for regions of search for extremums.

Important values are ORDER and RP, for Chebyshev filter.

By changing these values you can control the work of filter.
