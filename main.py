# main.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QTextEdit, QComboBox, QLabel, QLineEdit, QFormLayout
)
from client import FiveSim

API_KEY_FILE = "apikey.txt"

class FiveSimUI(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = ""
        self.countries_data = {}  # will store countries data after fetching
        self.load_api_key()  # Try to load API key from file
        # Only create a client if an API key was loaded
        self.client = FiveSim(api_key=self.api_key) if self.api_key else None
        self.initUI()

    def load_api_key(self):
        if os.path.exists(API_KEY_FILE):
            with open(API_KEY_FILE, "r") as f:
                self.api_key = f.read().strip()

    def save_api_key(self):
        self.api_key = self.api_key_edit.text().strip()
        with open(API_KEY_FILE, "w") as f:
            f.write(self.api_key)
        self.log("API Key saved.")
        # (Re)initialize the client with the new key.
        self.client = FiveSim(api_key=self.api_key)

    def initUI(self):
        self.setWindowTitle("FiveSim UI")
        self.resize(600, 800)
        main_layout = QVBoxLayout()

        ## --- API Key Section ---
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("API Key:")
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("Enter API Key")
        if self.api_key:
            self.api_key_edit.setText(self.api_key)
        btn_save_api = QPushButton("Save API Key")
        btn_save_api.clicked.connect(self.save_api_key)
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_edit)
        api_key_layout.addWidget(btn_save_api)
        main_layout.addLayout(api_key_layout)

        ## --- Logging Console ---
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        main_layout.addWidget(self.console)

        ## --- Comboboxes for Country, Operator, and Product ---
        form_layout = QFormLayout()
        self.country_combo = QComboBox()
        self.operator_combo = QComboBox()
        self.product_combo = QComboBox()
        form_layout.addRow("Country:", self.country_combo)
        form_layout.addRow("Operator:", self.operator_combo)
        form_layout.addRow("Product:", self.product_combo)
        main_layout.addLayout(form_layout)
        # When country selection changes, update operator list accordingly.
        self.country_combo.currentIndexChanged.connect(self.update_operators)

        ## --- Buttons to Fetch Countries/Operators/Products ---
        fetch_buttons_layout = QHBoxLayout()
        btn_fetch_countries = QPushButton("Fetch Countries")
        btn_fetch_countries.clicked.connect(self.get_countries)
        btn_fetch_operators = QPushButton("Fetch Operators")
        btn_fetch_operators.clicked.connect(self.get_operators)
        btn_fetch_products = QPushButton("Fetch Products")
        btn_fetch_products.clicked.connect(self.get_products)
        fetch_buttons_layout.addWidget(btn_fetch_countries)
        fetch_buttons_layout.addWidget(btn_fetch_operators)
        fetch_buttons_layout.addWidget(btn_fetch_products)
        main_layout.addLayout(fetch_buttons_layout)

        ## --- Additional Parameter Inputs ---
        form_layout2 = QFormLayout()
        self.order_id_edit = QLineEdit()
        self.order_id_edit.setPlaceholderText("Enter Order ID")
        self.phone_number_edit = QLineEdit()
        self.phone_number_edit.setPlaceholderText("Phone Number")
        self.rebuy_number_edit = QLineEdit()
        self.rebuy_number_edit.setPlaceholderText("Enter Number for Rebuy")
        # Remove currency textbox and add a balance label instead.
        self.balance_label = QLabel("Balance: N/A")
        form_layout2.addRow("Order ID:", self.order_id_edit)
        form_layout2.addRow("Phone Number:", self.phone_number_edit)
        form_layout2.addRow("Rebuy Number:", self.rebuy_number_edit)
        form_layout2.addRow("Balance:", self.balance_label)
        main_layout.addLayout(form_layout2)

        ## --- Order Management Buttons ---
        # The order is: Buy Number, Ban Order, Cancel Order, Finish Order, Check Order, Rebuy Number
        order_buttons_layout = QHBoxLayout()
        btn_buy_number = QPushButton("Buy Number")
        btn_buy_number.clicked.connect(self.buy_number)
        btn_ban_order = QPushButton("Ban Order")
        btn_ban_order.clicked.connect(self.ban_order)
        btn_cancel_order = QPushButton("Cancel Order")
        btn_cancel_order.clicked.connect(self.cancel_order)
        btn_finish_order = QPushButton("Finish Order")
        btn_finish_order.clicked.connect(self.finish_order)
        btn_check_order = QPushButton("Check Order")
        btn_check_order.clicked.connect(self.check_order)
        btn_rebuy_number = QPushButton("Rebuy Number")
        btn_rebuy_number.clicked.connect(self.rebuy_number)
        order_buttons_layout.addWidget(btn_buy_number)
        order_buttons_layout.addWidget(btn_ban_order)
        order_buttons_layout.addWidget(btn_cancel_order)
        order_buttons_layout.addWidget(btn_finish_order)
        order_buttons_layout.addWidget(btn_check_order)
        order_buttons_layout.addWidget(btn_rebuy_number)
        main_layout.addLayout(order_buttons_layout)

        ## --- Buttons for Price Requests ---
        btn_price_requests = QPushButton("Get Prices")
        btn_price_requests.clicked.connect(self.get_prices)
        btn_price_by_country = QPushButton("Get Prices by Country")
        btn_price_by_country.clicked.connect(self.get_prices_by_country)
        btn_price_by_product = QPushButton("Get Prices by Product")
        btn_price_by_product.clicked.connect(self.get_prices_by_product)
        btn_price_by_country_and_product = QPushButton("Get Prices by Country and Product")
        btn_price_by_country_and_product.clicked.connect(self.get_prices_by_country_and_product)
        main_layout.addWidget(btn_price_requests)
        main_layout.addWidget(btn_price_by_country)
        main_layout.addWidget(btn_price_by_product)
        main_layout.addWidget(btn_price_by_country_and_product)

        ## --- Balance and SMS Inbox ---
        btn_balance = QPushButton("Get Balance")
        btn_balance.clicked.connect(self.get_balance)
        main_layout.addWidget(btn_balance)
        btn_sms_inbox = QPushButton("SMS Inbox List")
        btn_sms_inbox.clicked.connect(self.sms_inbox_list)
        main_layout.addWidget(btn_sms_inbox)

        self.setLayout(main_layout)

    def log(self, message):
        self.console.append(str(message))

    def ensure_client(self):
        if not self.client:
            self.log("API Key not set. Please enter and save API Key.")
            return False
        return True

    def update_operators(self):
        """Update the operator combobox based on the currently selected country."""
        country = self.country_combo.currentText()
        if not country or not self.countries_data:
            self.operator_combo.clear()
            self.operator_combo.addItem("any")
            return
        data = self.countries_data.get(country, {})
        # Exclude known keys that are not operators.
        exclude = {"iso", "prefix", "text_en", "text_ru"}
        operators = [key for key in data.keys() if key not in exclude]
        if not operators:
            operators = ["any"]
        self.operator_combo.clear()
        self.operator_combo.addItems(operators)
        self.log(f"Operators for {country}: {operators}")

    ## --- Methods that call client.py functions ---

    def get_countries(self):
        if not self.ensure_client():
            return
        try:
            countries = self.client.get_country_list()
            self.countries_data = countries  # store data for later use
            self.country_combo.clear()
            for country in countries.keys():
                self.country_combo.addItem(country)
            self.log(f"Available Countries: {countries}")
            # Immediately update operators for the currently selected country.
            self.update_operators()
        except Exception as e:
            self.log(f"Error in get_countries: {e}")

    def get_operators(self):
        # Although operators are now updated automatically, you can also refresh manually.
        self.update_operators()

    def get_products(self):
        if not self.ensure_client():
            return
        country = self.country_combo.currentText()
        operator = self.operator_combo.currentText()
        if not country or not operator:
            self.log("Select a country and operator first.")
            return
        try:
            products = self.client.product_requests(country, operator)
            self.product_combo.clear()
            for product in products.keys():
                self.product_combo.addItem(product)
            self.log(f"Available Products for {country}/{operator}: {products}")
        except Exception as e:
            self.log(f"Error in get_products: {e}")

    def get_prices(self):
        if not self.ensure_client():
            return
        try:
            prices = self.client.price_requests()
            self.log(f"Price Requests: {prices}")
        except Exception as e:
            self.log(f"Error in get_prices: {e}")

    def get_prices_by_country(self):
        if not self.ensure_client():
            return
        country = self.country_combo.currentText()
        if not country:
            self.log("Select a country first.")
            return
        try:
            prices = self.client.price_requests_by_country(country)
            self.log(f"Prices for Country {country}: {prices}")
        except Exception as e:
            self.log(f"Error in get_prices_by_country: {e}")

    def get_prices_by_product(self):
        if not self.ensure_client():
            return
        product = self.product_combo.currentText()
        if not product:
            self.log("Select a product first.")
            return
        try:
            prices = self.client.price_requests_by_product(product)
            self.log(f"Prices for Product {product}: {prices}")
        except Exception as e:
            self.log(f"Error in get_prices_by_product: {e}")

    def get_prices_by_country_and_product(self):
        if not self.ensure_client():
            return
        country = self.country_combo.currentText()
        product = self.product_combo.currentText()
        if not country or not product:
            self.log("Select a country and product first.")
            return
        try:
            prices = self.client.price_requests_by_country_and_product(country, product)
            self.log(f"Prices for {country} and {product}: {prices}")
        except Exception as e:
            self.log(f"Error in get_prices_by_country_and_product: {e}")

    def get_balance(self):
        if not self.ensure_client():
            return
        try:
            balance = self.client.get_balance()
            self.log(f"Account Balance: {balance}")
            # Update the balance label.
            # If balance is returned as a dict, adjust as needed.
            if isinstance(balance, dict):
                # Assuming the balance value is under a key such as "balance"
                value = balance.get("balance", balance)
            else:
                value = balance
            self.balance_label.setText(f"Balance: {value}")
        except Exception as e:
            self.log(f"Error in get_balance: {e}")

    def buy_number(self):
        if not self.ensure_client():
            return
        country = self.country_combo.currentText()
        operator = self.operator_combo.currentText()
        product = self.product_combo.currentText()
        if not country or not operator or not product:
            self.log("Select country, operator, and product first.")
            return
        try:
            result = self.client.buy_number(country, operator, product)
            self.log(f"Purchased Number: {result}")
            # Update the order id textbox with the new order id (if present)
            order_id = result.get("id")
            if order_id:
                self.order_id_edit.setText(str(order_id))
            # Update the phone number textbox with the new phone number (if present)
            phone = result.get("phone")
            if phone:
                self.phone_number_edit.setText(phone)
        except Exception as e:
            self.log(f"Error in buy_number: {e}")

    def rebuy_number(self):
        if not self.ensure_client():
            return
        product = self.product_combo.currentText()
        number = self.rebuy_number_edit.text().strip()
        if not product or not number:
            self.log("Select a product and enter a number for rebuy.")
            return
        try:
            result = self.client.rebuy_number(product, number)
            self.log(f"Rebuy Number Result: {result}")
        except Exception as e:
            self.log(f"Error in rebuy_number: {e}")

    def check_order(self):
        if not self.ensure_client():
            return
        order_id = self.order_id_edit.text().strip()
        if not order_id:
            self.log("Enter Order ID.")
            return
        try:
            result = self.client.check_order(order_id)
            self.log(f"Check Order Result: {result}")
        except Exception as e:
            self.log(f"Error in check_order: {e}")

    def finish_order(self):
        if not self.ensure_client():
            return
        order_id = self.order_id_edit.text().strip()
        if not order_id:
            self.log("Enter Order ID.")
            return
        try:
            result = self.client.finish_order(order_id)
            self.log(f"Finish Order Result: {result}")
        except Exception as e:
            self.log(f"Error in finish_order: {e}")

    def cancel_order(self):
        if not self.ensure_client():
            return
        order_id = self.order_id_edit.text().strip()
        if not order_id:
            self.log("Enter Order ID.")
            return
        try:
            result = self.client.cancel_order(order_id)
            self.log(f"Cancel Order Result: {result}")
        except Exception as e:
            self.log(f"Error in cancel_order: {e}")

    def ban_order(self):
        if not self.ensure_client():
            return
        order_id = self.order_id_edit.text().strip()
        if not order_id:
            self.log("Enter Order ID.")
            return
        try:
            result = self.client.ban_order(order_id)
            self.log(f"Ban Order Result: {result}")
        except Exception as e:
            self.log(f"Error in ban_order: {e}")

    def sms_inbox_list(self):
        if not self.ensure_client():
            return
        order_id = self.order_id_edit.text().strip()
        if not order_id:
            self.log("Enter Order ID.")
            return
        try:
            result = self.client.sms_inbox_list(order_id)
            self.log(f"SMS Inbox List: {result}")
        except Exception as e:
            self.log(f"Error in sms_inbox_list: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = FiveSimUI()
    ui.show()
    sys.exit(app.exec_())
