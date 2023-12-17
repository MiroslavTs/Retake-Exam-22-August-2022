from project.client import Client

from project.meals.meal import Meal

from project.meals.starter import Starter

from project.meals.main_dish import MainDish

from project.meals.dessert import Dessert


class FoodOrdersApp:
    def __init__(self):
        self.menu = [] # An empty list that will contain all the meals (objects)
        self.clients_list = [] #An empty list that will contain all the clients (objects)

    def register_client(self, client_phone_number: str):
        for client in self.clients_list:
            if client.phone_number == client_phone_number:
                raise Exception("The client has already been registered!")

        client = Client(client_phone_number)
        self.clients_list.append(client)
        return f"Client {client_phone_number} registered successfully."

    def add_meals_to_menu(self, *meals: Meal):
        for meal in meals:
            if isinstance(meal, (Starter, MainDish, Dessert)):
                self.menu.append(meal)

    def show_menu(self):
        if len(self.menu) < 5:
            raise Exception("The menu is not ready!")
        result = "Menu:\n"
        for meal in self.menu:
            result += meal.details() + "\n"
        return result

    def add_meals_to_shopping_cart(self, client_phone_number: str, **meal_names_and_quantities):
        if len(self.menu) < 5:
            raise Exception("The menu is not ready!")

        client = [client for client in self.clients_list if client.phone_number == client_phone_number]
        if not client:
            client = Client(client_phone_number)
            self.clients_list.append(client)
        else:
            client = client[0]

        meals_added = []
        total_bill = 0

        for meal_name, quantity in meal_names_and_quantities.items():
            meal = [meal for meal in self.menu if meal.name == meal_name]
            if not meal:
                raise Exception(f"{meal_name} is not on the menu!")
            meal = meal[0]

            if meal.quantity < quantity:
                raise Exception(f"Not enough quantity of {meal.type}: {meal_name}!")

            client.shopping_cart.append(meal)
            meals_added.append(meal.name)
            total_bill += meal.price * quantity
            meal.quantity -= quantity

        bill_formatted = "{:.2f}".format(total_bill)
        meal_names_str = ", ".join(meals_added)

        return f"Client {client_phone_number} successfully ordered {meal_names_str} for {bill_formatted}lv."

    def cancel_order(self, client_phone_number: str):
        client = [client for client in self.clients_list if client.phone_number == client_phone_number]
        if not client:
            raise Exception(f"Order not found!")
        client = client[0]
        if not client.shopping_cart:
            raise Exception(f"There are no ordered meals!")

        for meal in client.shopping_cart:
            self.menu[meal] += 1

        client.shopping_cart = []
        client.bill = 0
        return f"Client {client_phone_number} successfully canceled his order."

    def finish_order(self, client_phone_number: str):
        client = [client for client in self.clients_list if client.phone_number == client_phone_number]
        if not client:
            raise Exception(f"Order not found!")
        client = client[0]
        if not client.shopping_cart:
            raise Exception(f"There are no ordered meals!")

        receipt_id = len(self.clients_list) + 1
        total_paid_money = "{:.2f}".format(client.bill)

        self.clients_list.remove(client)

        return f"Receipt #{receipt_id} with total amount of {total_paid_money} was " \
               f"successfully paid for {client_phone_number}."

    def __str__(self):
        return f"Food Orders App has {len(self.menu)} meals on the menu and {len(self.clients_list)} clients."
