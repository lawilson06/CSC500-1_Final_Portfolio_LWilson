from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QGridLayout, \
                             QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem,
                             QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QHeaderView, QMessageBox)
from PyQt6.QtGui import QAction, QColor, QIcon
import sys
import sqlite3

class ItemToPurchase(QDialog):
    def __init__(self, shopping_id):
        super().__init__()
        self.setWindowTitle("Item To Purchase")

        self.shopping_id = shopping_id

        self.item_name_label = QLabel("Enter the item's name: ")
        self.__item_name = QLineEdit()

        self.item_price_label = QLabel("Enter the item's price: ")
        self.__item_price = QLineEdit()

        self.item_quantity_label = QLabel("Enter the item's quantity: ")
        self.__item_quantity = QLineEdit()

        self.item_description_label = QLabel("Enter the item's description: ")
        self.__item_description = QLineEdit()

        self.add_item_button = QPushButton("Add Item(s)")
        self.add_item_button.clicked.connect(self.__insert_shopping_item)

        layout = QGridLayout()

        layout.addWidget(self.item_name_label, 0, 0)
        layout.addWidget(self.__item_name, 0, 1)

        layout.addWidget(self.item_price_label, 1, 0)
        layout.addWidget(self.__item_price, 1, 1)

        layout.addWidget(self.item_quantity_label, 2, 0)
        layout.addWidget(self.__item_quantity, 2, 1)

        layout.addWidget(self.item_description_label, 3, 0)
        layout.addWidget(self.__item_description, 3, 1)

        layout.addWidget(self.add_item_button, 4, 0, 1, 2)


        self.setLayout(layout)

    def __check_user_input(self):
        error_widget = QMessageBox()
        error_widget.setWindowTitle("Error")
        print("Hello")
        item_quantity = -1
        item_price = 0
        valid_entries = False

        try:
            item_quantity = int(self.__item_quantity.text())
            print(item_quantity)
            item_price = round(float(self.__item_price.text()), 2)
            print(item_price)
            valid_entries = True
        except Exception as e:
            print(e)
            error_widget.setText("Enter a valid values for price/quantity.")
            error_widget.exec()

        if len(self.__item_name.text()) <= 0:
            valid_entries = False
            error_widget.setText("Enter a valid name.")
            error_widget.exec()

        if len(self.__item_description.text()) <= 0:
            valid_entries = False
            error_widget.setText("Enter a valid description.")
            error_widget.exec()

        return valid_entries, item_quantity, item_price

    def __insert_shopping_item(self):
        valid_entries, item_quantity, item_price = self.__check_user_input()
        print(item_quantity, item_price)
        if valid_entries:
            connection = sqlite3.connect("ShoppingCartDB.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO shoppingcart (item_name, item_price, item_quantity, item_description, "
                           "shopping_id) VALUES (?, ?, ?, ?, ?)", (self.__item_name.text(), item_price,
                                                                   item_quantity, self.__item_description.text(),
                                                                   self.shopping_id))
            connection.commit()
            cursor.close()
            connection.close()
            self.close()
