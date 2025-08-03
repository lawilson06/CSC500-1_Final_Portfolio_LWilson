from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QGridLayout, \
                             QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem,
                             QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QHeaderView, QMessageBox)
from PyQt6.QtGui import QAction, QColor, QIcon
import sys
import sqlite3
from ItemToPurchase import ItemToPurchase


class ShoppingCart(QMainWindow):
    def __init__(self, shopping_id, user_date, shopper_name):
        super().__init__()
        self.setWindowTitle("Shopping Cart Menu")
        self.setMinimumSize(800, 600)

        self.add_shopping_item = QAction(QIcon("project_icons/add_shopping_cart.png"), "Add Item to Purchase", self)
        self.add_shopping_item.triggered.connect(self.__add_purchase_item)
        self.toolbar = QToolBar()
        self.toolbar.setMovable(True)
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.add_shopping_item)

        self.shopping_id = shopping_id
        self.cart_date = user_date
        self.shopper_name = shopper_name

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("Id", "Item Name", "Item Price", "Item Quantity", "Item Description"))
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setCentralWidget(self.table)

        self.shopper_label = QLabel(f"Name: {self.shopper_name} Date: {self.cart_date} Shopping ID: {self.shopping_id}")
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.addWidget(self.shopper_label)

        self.__populate_table()

    def __populate_table(self):
        connection = sqlite3.connect("ShoppingCartDB.db")
        payload = connection.execute("SELECT id, item_name, item_price, item_quantity, item_description "
                                     "FROM shoppingcart WHERE shopping_id = ?", (self.shopping_id,))
        self.table.setRowCount(0)
        for index, row_item in enumerate(payload):
            print(index, row_item)
            self.table.insertRow(index)
            for col_index, col_item in enumerate(row_item):
                self.table.setItem(index, col_index, QTableWidgetItem(str(col_item)))
        connection.close()

    def __add_purchase_item(self):
        item_dialog = ItemToPurchase(self.shopping_id)
        item_dialog.exec()
        self.__populate_table()