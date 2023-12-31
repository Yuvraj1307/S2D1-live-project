# from flask import Flask, render_template, request, redirect, url_for, session
# import json

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# # Initialize menu and orders
# menu = []
# orders = []
# order_id_counter = 1


# def load_data():
#     global menu, orders, order_id_counter
#     try:
#         with open("menu.json", "r") as f:
#             menu = json.load(f)
#     except FileNotFoundError:
#         menu = []

#     try:
#         with open("orders.json", "r") as f:
#             orders = json.load(f)
#             order_id_counter = max(order["id"] for order in orders) + 1
#     except FileNotFoundError:
#         orders = []
#         order_id_counter = 1


# def save_data():
#     with open("menu.json", "w") as f:
#         json.dump(menu, f, indent=4)

#     with open("orders.json", "w") as f:
#         json.dump(orders, f, indent=4)


# @app.route("/")
# def index():
#     return render_template("index.html", menu=menu, orders=orders)


# @app.route("/place_order", methods=["POST"])
# def place_order():
#     customer_name = request.form["customer_name"]
#     dish_ids = request.form.getlist("dish_id")

#     # Check if all selected dishes are available
#     for dish_id in dish_ids:
#         dish = next((dish for dish in menu if dish["id"] == int(dish_id)), None)
#         if not dish or not dish["availability"]:
#             return render_template("index.html", menu=menu, orders=orders, error_message="Invalid dish selection")

#     # Generate a new order ID and set initial status as "received"
#     global order_id_counter
#     order_id = order_id_counter
#     order_id_counter += 1

#     order = {
#         "id": order_id,
#         "customer_name": customer_name,
#         "dish_ids": dish_ids,
#         "status": "received"
#     }
#     orders.append(order)
#     save_data()

#     return redirect(url_for("index"))


# @app.route("/update_status", methods=["POST"])
# def update_status():
#     order_id = int(request.form["order_id"])
#     status = request.form["status"]

#     # Update the status of the specified order
#     order = next((order for order in orders if order["id"] == order_id), None)
#     if order:
#         order["status"] = status
#         save_data()

#     return redirect(url_for("index"))


# count = 1


# @app.route("/add_dish", methods=["POST"])
# def add_dish():
#     global count
#     dish_name = request.form["dish_name"]
#     price = float(request.form["price"])
#     availability = "availability" in request.form

#     dish = {
#         "id": count,
#         "name": dish_name,
#         "price": price,
#         "availability": availability
#     }
#     menu.append(dish)
#     count += 1
#     save_data()

#     return redirect(url_for("index"))


# @app.route("/remove_dish", methods=["POST"])
# def remove_dish():
#     dish_id = int(request.form["dish_id"])

#     # Remove the dish from the menu
#     global menu
#     menu = [dish for dish in menu if dish["id"] != dish_id]

#     # Update dish IDs in all orders
#     for order in orders:
#         order["dish_ids"] = [dish_id for dish_id in order["dish_ids"] if dish_id != dish_id]

#     save_data()

#     return redirect(url_for("index"))


# @app.route("/update_availability", methods=["POST"])
# def update_availability():
#     dish_id = int(request.form["dish_id"])
#     availability = "availability" in request.form

#     # Update the availability of the specified dish
#     dish = next((dish for dish in menu if dish["id"] == dish_id), None)
#     if dish:
#         dish["availability"] = availability
#         save_data()

#     return redirect(url_for("index"))


# def calculate_total_price(dish_ids):
#     # Calculate the total price of an order based on the dish IDs
#     total_price = 0
#     for dish_id in dish_ids:
#         dish = next((dish for dish in menu if dish["id"] == int(dish_id)), None)
#         if dish:
#             total_price += dish["price"]
#     return total_price


# app.jinja_env.globals.update(calculate_total_price=calculate_total_price)

# if __name__ == "__main__":
#     load_data()
#     app.run(debug=True)












































from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize menu and orders
menu = []
orders = []
order_id_counter = 1


@app.route("/")
def index():
    return render_template("index.html", menu=menu, orders=orders)


@app.route("/place_order", methods=["POST"])
def place_order():
    customer_name = request.form["customer_name"]
    dish_ids = request.form.getlist("dish_id")

    # Check if all selected dishes are available
    for dish_id in dish_ids:
        dish = next((dish for dish in menu if dish["id"] == int(dish_id)), None)
        if not dish or not dish["availability"]:
            return render_template("index.html", menu=menu, orders=orders, error_message="Invalid dish selection")

    # Generate a new order ID and set initial status as "received"
    global order_id_counter
    order_id = order_id_counter
    order_id_counter += 1

    order = {
        "id": order_id,
        "customer_name": customer_name,
        "dish_ids": dish_ids,
        "status": "received"
    }
    orders.append(order)

    return redirect(url_for("index"))


@app.route("/update_status", methods=["POST"])
def update_status():
    order_id = int(request.form["order_id"])
    status = request.form["status"]

    # Update the status of the specified order
    order = next((order for order in orders if order["id"] == order_id), None)
    if order:
        order["status"] = status

    return redirect(url_for("index"))

count=1
@app.route("/add_dish", methods=["POST"])
def add_dish():
    global count
    dish_name = request.form["dish_name"]
    price = float(request.form["price"])
    availability = "availability" in request.form

    dish = {
        "id": count,
        "name": dish_name,
        "price": price,
        "availability": availability
    }
    menu.append(dish)
    count+=1

    return redirect(url_for("index"))


@app.route("/remove_dish", methods=["POST"])
def remove_dish():
    dish_id = int(request.form["dish_id"])

    # Remove the dish from the menu
    global menu
    menu = [dish for dish in menu if dish["id"] != dish_id]

    # Update dish IDs in all orders
    for order in orders:
        order["dish_ids"] = [dish_id for dish_id in order["dish_ids"] if dish_id != dish_id]

    return redirect(url_for("index"))


@app.route("/update_availability", methods=["POST"])
def update_availability():
    dish_id = int(request.form["dish_id"])
    availability = "availability" in request.form

    # Update the availability of the specified dish
    dish = next((dish for dish in menu if dish["id"] == dish_id), None)
    if dish:
        dish["availability"] = availability

    return redirect(url_for("index"))


def calculate_total_price(dish_ids):
    # Calculate the total price of an order based on the dish IDs
    total_price = 0
    for dish_id in dish_ids:
        dish = next((dish for dish in menu if dish["id"] == int(dish_id)), None)
        if dish:
            total_price += dish["price"]
    return total_price


app.jinja_env.globals.update(calculate_total_price=calculate_total_price)

if __name__ == "__main__":
    app.run(debug=True)






























 