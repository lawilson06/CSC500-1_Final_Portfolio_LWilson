from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QGridLayout, \
                             QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem,
                             QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QHeaderView, QMessageBox)
from PyQt6.QtGui import QAction, QColor, QIcon
from PyQt6.QtCore import QTimer
import sqlite3
from ItemToPurchase import ItemToPurchase


class ShoppingCart(QMainWindow):
    def __init__(self, shopping_id, user_date, shopper_name, primary_window):
        super().__init__()
        self.setWindowTitle("Shopping Cart Menu")
        self.setMinimumSize(800, 600)
        self.primary_window = primary_window

        self.payload = None
        self.cart_total = None
        self.cart_quantity = None

        self.add_shopping_item = QAction(QIcon("project_icons/add_shopping_cart.png"), "Add Item to Purchase", self)
        self.add_shopping_item.triggered.connect(self.__add_purchase_item)
        self.cart_output = QAction(QIcon("project_icons/cart_total.png"), "View Current Cart Totals", self)
        self.cart_output.triggered.connect(self.__display_cart_total)
        self.update_shopping_item = QAction(QIcon("project_icons/update_shopping_cart.png"), "Update Cart Item", self)
        self.update_shopping_item.triggered.connect(self.__update_purchase_item)
        self.remove_shopping_item =QAction(QIcon("project_icons/remove_item_shopping_cart.png"), "Remove Cart Item",
                                           self)
        self.remove_shopping_item.triggered.connect(self.__remove_purchase_item)

        self.toolbar = QToolBar()
        self.toolbar.setMovable(True)
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.cart_output)
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

    def closeEvent(self, event):
        self.primary_window.show()
        self.primary_window.secondary_window = None
        self.primary_window.shopper_name_input.clear()
        QTimer.singleShot(1, self.primary_window.load_shopping_carts.trigger)
        event.accept()

    def __populate_table(self):
        self.cart_total = 0
        self.cart_quantity = 0
        connection = sqlite3.connect("ShoppingCartDB.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, item_name, item_price, item_quantity, item_description "
                                     "FROM shoppingcart WHERE shopping_id = ?", (self.shopping_id,))
        self.payload = cursor.fetchall()
        for rec in self.payload:
            self.cart_total += (rec[2] * rec[3])
            self.cart_quantity += rec[3]
        self.table.setRowCount(0)
        for index, row_item in enumerate(self.payload):
            print(index, row_item)
            self.table.insertRow(index)
            for col_index, col_item in enumerate(row_item):
                self.table.setItem(index, col_index, QTableWidgetItem(str(col_item)))
        cursor.close()
        connection.close()

    def __add_purchase_item(self):
        item_dialog = ItemToPurchase(self.shopping_id)
        item_dialog.exec()
        self.__populate_table()

    def __item_record_clicked(self):
        self.toolbar.addAction(self.update_shopping_item)
        self.toolbar.addAction(self.remove_shopping_item)

    def __record_assign_helper(self):
        current_row = self.table.currentRow()
        print(current_row)
        item_id = self.table.item(current_row, 0).text()
        item_name = self.table.item(current_row, 1).text()
        item_price = self.table.item(current_row, 2).text()
        item_quantity = self.table.item(current_row, 3).text()
        item_description = self.table.item(current_row, 4).text()
        return item_id, item_name, item_price, item_quantity, item_description

    def __update_purchase_item(self):
        item_id, item_name, item_price, item_quantity, item_description = self.__record_assign_helper()
        update_dialog = ItemToPurchase(self.shopping_id, item_id, item_name, item_price, item_quantity,item_description)
        update_dialog.exec()
        self.__populate_table()
        self.table.clearSelection()
        self.toolbar.removeAction(self.update_shopping_item)
        self.toolbar.removeAction(self.remove_shopping_item)

    def __remove_purchase_item(self):
        item_id, item_name, item_price, item_quantity, item_description = self.__record_assign_helper()
        remove_obj = self.RemoveShoppingItem(item_id, item_name, item_quantity)
        remove_obj.exec()
        self.__populate_table()
        self.table.clearSelection()
        self.toolbar.removeAction(self.remove_shopping_item)
        self.toolbar.removeAction(self.update_shopping_item)

    def __display_cart_total(self):
        display_total = QMessageBox()
        display_total.setWindowTitle(self.shopping_id)
        display_text = "Current Cart Summary \n"
        display_text += f"Number of Items: {self.cart_quantity} \n"
        if len(self.payload) <= 0:
            display_text = "Cart is empty."
        else:
            for cart in self.payload:
                display_text += f"{cart[1]} {cart[3]} @ {cart[2]} = {(cart[2] * cart[3]):.2f} \n"
            display_text += f"Cart Total: ${self.cart_total:.2f}"
        display_total.setText(display_text)
        display_total.exec()

    class RemoveShoppingItem(QDialog):
        def __init__(self, item_id, item_name, item_quantity):
            super().__init__()
            self.setWindowTitle(f"Remove Item: {item_name}")
            self.item_id = item_id
            self.item_name = item_name
            self.item_quantity = item_quantity

            self.details_label = QLabel(f"Are you sure you wish to remove {self.item_name} | "
                                        f"Quantity: {self.item_quantity}")

            self.confirm_button = QPushButton("Confirm")
            self.confirm_button.clicked.connect(self.__remove_cart_item)
            self.decline_button = QPushButton("Decline")
            self.decline_button.clicked.connect(self.close)

            layout = QVBoxLayout()
            layout.addWidget(self.details_label)
            layout.addWidget(self.confirm_button)
            self.setLayout(layout)

        def __remove_cart_item(self):
            connection = sqlite3.connect("ShoppingCartDB.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM shoppingcart WHERE id = ?", (self.item_id,))
            connection.commit()
            cursor.close()
            connection.close()
            self.close()