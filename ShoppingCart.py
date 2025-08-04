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
        self.update_shopping_item = QAction(QIcon("project_icons/update_shopping_cart.png"), "Update Cart Item", self)
        self.update_shopping_item.triggered.connect(self.__update_purchase_item)
        self.remove_shopping_item =QAction(QIcon("project_icons/remove_item_shopping_cart.png"), "Remove Cart Item",
                                           self)
        self.remove_shopping_item.triggered.connect(self.__remove_purchase_item)

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

        self.table.cellClicked.connect(self.__item_record_clicked)

        print(self.table.currentRow())
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

    def __item_record_clicked(self):
        self.toolbar.addAction(self.update_shopping_item)
        self.toolbar.addAction(self.remove_shopping_item)

    def __update_purchase_item(self):
        current_row = self.table.currentRow()
        print(current_row)
        item_id = self.table.item(current_row, 0).text()
        item_name = self.table.item(current_row, 1).text()
        item_price = self.table.item(current_row, 2).text()
        item_quantity = self.table.item(current_row, 3).text()
        item_description = self.table.item(current_row, 4).text()

        update_dialog = ItemToPurchase(self.shopping_id, item_id, item_name, item_price, item_quantity,item_description)
        update_dialog.exec()
        self.__populate_table()
        self.table.clearSelection()
        self.toolbar.removeAction(self.update_shopping_item)

    def __remove_purchase_item(self):
        pass

