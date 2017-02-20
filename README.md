# QuickCRS

A QGIS plugin to set the CRS of the current project to your favourite CRS and enable OTF reprojection with just one click. It's very easy to set your default CRS in the Plugin Settings Menu.

**You can install this plugin, but be aware that it is experimental. It may still have some bugs.  Please [report them](https://github.com/mstuyts/QuickCRS/issues).**


**If you installed QuickCRS version 0.2 or older, you have to perform the following Python Script before installing a newer version. If you only installed version 0.3 or newer, you can ignore this message**
```python
from PyQt4.QtCore import *
s = QSettings()
s.remove("quickcrs/crs")
```

