import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from loguru import logger


class DraggablePoint(pg.GraphItem):
    def __init__(self, *args, **kwargs):
        self.dragPoint = None
        self.dragOffset = None
        self.curve = []
        if "curve" in kwargs and kwargs["curve"]:
            self.curve = kwargs["curve"]

        pg.GraphItem.__init__(self, *args, **kwargs)

    def setData(self, **kwds):
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['adj'] = np.column_stack((np.arange(0, npts-1), np.arange(1, npts)))
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.updateGraph()

    def updateGraph(self):
        if 'pos' in self.data:
            logger.debug(self.data['pos'][0])
        pg.GraphItem.setData(self, **self.data)

    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            logger.debug('mouse button')
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
            self.dragOffset = self.data['pos'][ind][1] - pos[1]
            logger.debug('isStart')
        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return

        ind = self.dragPoint.data()[0]
        self.data['pos'] = np.array([[ev.pos()[0] + self.dragOffset, 0.0]])

        logger.debug(type(self.data['pos']))
        logger.debug(ev.pos()[0] + self.dragOffset)
        self.updateGraph()
        ev.accept()
