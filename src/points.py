import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt5 import QtCore
from loguru import logger


class DraggablePoint(pg.GraphItem):

    def __init__(self, **kwargs):
        self.dragPoint = None
        self.dragOffset = None
        self.curve = None
        self.data = None
        self.controller = None
        self.model_params = None

        pg.GraphItem.__init__(self, **kwargs)

    def set_curve(self, x, y):
        self.curve = pd.DataFrame(pd.Series(y, index=x, name="Y"))

    def setData(self, **kwds):
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['adj'] = np.column_stack((np.arange(0, npts-1), np.arange(1, npts)))
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.update_graph()

    def update_graph(self):
        pg.GraphItem.setData(self, **self.data)

    def mouseDragEvent(self, ev):
        """Hook of mouse drag event"""
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return

        if ev.isStart():
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind][0] - pos[0]

        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return

        new_x = round(ev.pos()[0] + self.dragOffset, 4)
        ind = self.curve.index[self.curve.index.get_loc(new_x, method="nearest")]
        new_y = self.curve.loc[ind].to_list()[0]
        self.data['pos'] = np.array([[ind, new_y]])
        self.controller.change_extremum_data(new_x, new_y, *self.model_params)
        self.update_graph()
        ev.accept()
