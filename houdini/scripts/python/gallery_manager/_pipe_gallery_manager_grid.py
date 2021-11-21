from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import math
import hou


class GalleryItem(QPushButton):

    size = QSize(100,100)

    def __init__(self):
        super(GalleryItem, self).__init__()
        self.setFixedSize(self.size)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)



class ItemGrid(QWidget):
    def __init__(self, parent):
        super(ItemGrid, self).__init__(parent)
        self.container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.grid_layout.setAlignment(Qt.AlignTop)
        self.container.setLayout(self.grid_layout)
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)

        main_vertical_lay = QVBoxLayout()
        main_vertical_lay.addWidget(self.scroll)
        self.setLayout(main_vertical_lay)

        self.items = []
        self.num_cols = 5

    def add_item(self, gallery_item):
        row = math.ceil(len(self.items)/self.num_cols)
        col = len(self.items) % self.num_cols + 1

        gallery_item.setParent(self.container)
        self.grid_layout.addWidget(gallery_item, row, col)
        self.items.append(gallery_item)


class GalleryPanel(QFrame):
    def __init__(self):
        super(GalleryPanel, self).__init__()
        self.items_grid = ItemGrid(self)
        self.setAcceptDrops(True)
        main_vert_layout = QVBoxLayout()
        main_vert_layout.addWidget(self.items_grid)

        self.setLayout(main_vert_layout)


    def dragEnterEvent(self, event):
        event.accept()


    def dropEvent(self, event):
        path = event.mimeData().text()
        node = hou.node(path)
        if not node:
            return False

        item = GalleryItem()
        self.items_grid.add_item(item)


   



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GalleryPanel()
    window.show()
    app.exec_()

