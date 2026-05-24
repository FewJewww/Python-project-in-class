import json

# Name of the file used to store data
DATA_FILE = "finance_data.json"


# LOAD DATA FROM FILE
def load_data():

    # Load data from the JSON file.If the file does not exist, use default empty data.
    finance_data = {
        "income": 0,
        "expenses": []
    }

    try:
        with open(DATA_FILE, "r") as file:
            finance_data = json.load(file)
    except FileNotFoundError:
        pass

    return finance_data


def save_data(finance_data):

    with open(DATA_FILE, "w") as file:
        # indent=4 makes the file easier to read
        json.dump(finance_data, file, indent=4)


def add_income(finance_data, income):

    finance_data["income"] += income

    return finance_data


def add_expense(finance_data, category, amount, description):
    expense = {
        "category": category,
        "amount": amount,
        "description": description
    }

    finance_data["expenses"].append(expense)

    return finance_data


def show_balance(finance_data):
    total_expenses = 0

    for expense in finance_data["expenses"]:
        total_expenses += expense["amount"]

    balance = finance_data["income"] - total_expenses

    return balance


def show_expenses(finance_data, some_category):
    total_expenses = 0
    category_expenses = 0
    output_lines = []

    # If there are no expenses
    if len(finance_data["expenses"]) == 0:
        return "Spend Nothing! "

    for expense in finance_data["expenses"]:

        category = expense["category"]
        amount = expense["amount"]
        description = expense['description']

        total_expenses += amount

        # If category already exists
        if category == some_category:
            category_expenses += amount
            line = f"Amount: ${amount:.2f}"
            if description != '':
                line += f"   Description: {description}"
            output_lines.append(line)

    # No expenses
    if category_expenses == 0:
        return f"No {some_category} spending yet"

    # Display percentage
    percentage = (category_expenses / total_expenses) * 100
    output_lines.append(f"{some_category}: ${category_expenses:.2f} ({percentage:.1f}%)")

    return "\n".join(output_lines)
