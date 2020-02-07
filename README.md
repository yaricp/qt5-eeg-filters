# qt5-eeg-filters

GUI for eeg-filters ( https://github.com/yaricp/eeg-filters ) based on Qt5.

## Requirements

Program require python >= 3.6

Also:

* eeg-filters
* pyQt5
* pyqtgraph

Note: You must have installed Qt5  on your PC.

## Installation



```
$ git clone https://github.com/yaricp/qt5-eeg-filters.git
$ cd qt5-eeg-filters/
$ ./install.sh
```

## Usage

For start program just:

```
$ ./start.sh
```

After that you can to see a main window of program:

You can open a file with EEG signals data.
This file you can get from NeuroExplorer4.4 by exporting data to ASCII format.

When curves will be showed on main plot you can make a filter it by choosing bandwith in list of bandwidths.

You can move regions for searching extremums. Also you can change boundaries of this regions by text filds over main graphic.

The any stage of your reseach you can save in a folder what you want.


## Settings

Main setting of program are in file settings.py in project folder.

You can set a default list of bandwiths, begin and end for regions for searching extremums.

Important values are ORDER and RP for Chebyshev filter.

By changing this values you can mange work of filter.
