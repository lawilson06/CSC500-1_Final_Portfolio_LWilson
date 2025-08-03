from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QGridLayout, \
                             QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem,
                             QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QHeaderView, QMessageBox)
from PyQt6.QtGui import QAction, QColor, QIcon
import sys
import sqlite3
from ShoppingCart import ShoppingCart
from datetime import datetime
from uuid import uuid4

class PrimaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main User Menu")
        self.setMinimumSize(400,100)
        self.setStyleSheet("QMainWindow {background-color: #f0e9dd}")

        self.current_date = datetime.now().strftime('%m/%d/%Y')

        # Secondary window access - Add shopping cart
        self.secondary_window = None

        self.add_shopping_cart = QAction(QIcon("project_icons/add_shopping_cart.png"), "Add Cart", self)
        self.add_shopping_cart.triggered.connect(self.__secondary_window_make_visible)

        self.load_shopping_carts = QAction(QIcon("project_icons/load_shopping_carts.png"), "Load Carts", self)
        self.load_shopping_carts.triggered.connect(self.__load_shopping_carts)

        self.cart_combobox = QComboBox()
        # self.cart_combobox.addItems(["SELECT"])
        # self.cart_combobox.setHidden(True)

        self.toolbar = QToolBar()
        self.toolbar.setMovable(True)
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.add_shopping_cart)
        self.toolbar.addAction(self.load_shopping_carts)
        # self.toolbar.addWidget(self.cart_combobox)

        self.shopper_name_label = QLabel("Shopper Name: ")
        self.shopper_name_input = QLineEdit()

        self.shopping_cart_date = QLabel("Shopping Cart Date: ")
        self.shopping_cart_date_input = QLineEdit(self.current_date)

        container = QWidget()
        layout = QGridLayout()

        layout.addWidget(self.shopper_name_label, 0, 0)
        layout.addWidget(self.shopper_name_input, 0, 1)
        layout.addWidget(self.shopping_cart_date, 1, 0)
        layout.addWidget(self.shopping_cart_date_input, 1, 1)

        container.setLayout(layout)

        self.setCentralWidget(container)

    def __secondary_window_make_visible(self):
        shopping_id = str(uuid4())
        data_check, cart_date = self.__secondary_window_preliminary_data_check()
        if self.secondary_window is None and data_check:
            self.__insert_shopping_data(shopping_id, cart_date)
            self.secondary_window = ShoppingCart(shopping_id, cart_date, self.shopper_name_input.text())
            self.secondary_window.show()
            primary_obj.hide()

    def __secondary_window_preliminary_data_check(self):
        error_widget = QMessageBox()
        error_widget.setWindowTitle("Error")
        valid_entries = False
        cart_date = ''
        try:
            cart_date = datetime.strptime(self.shopping_cart_date_input.text(), "%m/%d/%Y")
            cart_date = cart_date.strftime("%m/%d/%Y")
            print(cart_date)
            valid_entries = True
        except Exception as e:
            print(e)
            error_widget.setText("Must enter a valid date in MM/DD/YYYY format.")
            error_widget.exec()
        if len(self.shopper_name_input.text()) <= 0:
            valid_entries = False
            error_widget.setText("Must enter a name")
            error_widget.exec()
        return valid_entries, cart_date

    def __insert_shopping_data(self, shopping_id, cart_date):
        connection = sqlite3.connect('ShoppingCartDB.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO shoppingdata (shopping_id, shopper_name, shopping_date) VALUES (?, ?, ?)",
                       (shopping_id, self.shopper_name_input.text(), cart_date))
        connection.commit()
        cursor.close()
        connection.close()

    def __load_shopping_carts(self):

        cart_list = ['Select']
        cart_data = self.__fetch_shopping_cart_ids()
        for cart in cart_data:
            cart_list.append(cart[0])
        print(cart_list)
        # self.cart_combobox.clear()
        self.cart_combobox.addItems(cart_list)
        self.toolbar.addWidget(self.cart_combobox)
        # self.cart_combobox.addItems(cart_list)
        # self.cart_combobox.setVisible(True)


    @staticmethod
    def __fetch_shopping_cart_ids():
        connection = sqlite3.connect("ShoppingCartDB.db")
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT shopping_id FROM shoppingcart")
        shop_ids = cursor.fetchall()
        return [shop_id for shop_id in shop_ids]

app = QApplication(sys.argv)
primary_obj = PrimaryWindow()
primary_obj.show()
sys.exit(app.exec())