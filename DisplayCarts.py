from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QGridLayout, \
                             QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem,
                             QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QHeaderView, QMessageBox)
import sqlite3

class DisplayCarts(QDialog):
    def __init__(self, shopping_id):
        super().__init__()
        self.shopping_id = shopping_id
        self.setWindowTitle(f"Displaying Cart: {self.shopping_id}")
        self.setMinimumSize(800,600)

        self.payload = None
        self.cart_total = 0
        self.cart_quantity = 0

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("Id", "Item Name", "Item Price", "Item Quantity", "Item Description"))
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.display_cost_button = QPushButton("Display Cart Totals")
        self.display_cost_button.clicked.connect(self.__display_cart_total)

        self.display_descriptions_button = QPushButton("Display Cart Descriptions")
        self.display_descriptions_button.clicked.connect(self.__display_cart_descriptions)

        layout = QVBoxLayout()

        layout.addWidget(self.table)
        layout.addWidget(self.display_cost_button)
        layout.addWidget(self.display_descriptions_button)

        self.setLayout(layout)
        self.__retrieve_cart_data()

    def __retrieve_cart_data(self):
        connection = sqlite3.connect("ShoppingCartDB.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, item_name, item_price, item_quantity, item_description FROM "
                       "shoppingcart WHERE shopping_id = ?", (self.shopping_id,))
        self.payload = cursor.fetchall()
        self.table.setRowCount(0)
        for index, row_item in enumerate(self.payload):
            print(index, row_item)
            self.table.insertRow(index)
            for col_index, col_item in enumerate(row_item):
                self.table.setItem(index, col_index, QTableWidgetItem(str(col_item)))
        connection.close()
        self.__calculate_cart_total()

    def __retrieve_user_data(self):
        connection = sqlite3.connect("ShoppingCartDB.db")
        cursor = connection.cursor()
        cursor.execute("SELECT shopper_name, shopping_date FROM shoppingdata WHERE shopping_id = ?",
                       (self.shopping_id,))
        name, cart_date = cursor.fetchall()[0]
        return name, cart_date

    def __calculate_cart_total(self):
        self.cart_total = 0
        self.cart_quantity = 0
        for cart in self.payload:
            self.cart_total += (cart[2] * cart[3])
            self.cart_quantity += cart[3]
        print(self.cart_total)

    def __display_name_date_helper(self):
        display_msg = QMessageBox()
        display_msg.setWindowTitle(self.shopping_id)
        cust_name, cart_date = self.__retrieve_user_data()
        display_text = ""
        display_text += f"{cust_name}'s Shopping Cart - {cart_date} \n"
        return display_text, display_msg

    def __display_cart_total(self):
        self.__calculate_cart_total()
        display_text, display_total = self.__display_name_date_helper()
        display_text += f"Number of Items: {self.cart_quantity} \n"
        for cart in self.payload:
            display_text += f"{cart[1]} {cart[3]} @ {cart[2]} = {(cart[2] * cart[3]):.2f} \n"
        display_text += f"Cart Total: ${self.cart_total:.2f}"
        display_total.setText(display_text)
        display_total.exec()

    def __display_cart_descriptions(self):
       display_text, display_descriptions = self.__display_name_date_helper()
       display_text += "Item Descriptions \n"
       for cart in self.payload:
           display_text += f"{cart[1]}: {cart[4]} \n"
       display_descriptions.setText(display_text)
       display_descriptions.exec()



