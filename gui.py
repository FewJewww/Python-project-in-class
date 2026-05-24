import tkinter as tk
import finance
from wishlist import *
from tkinter import ttk, messagebox


def start_gui():
    # Create the main window. Set window title and size
    window = tk.Tk()
    window.title("Where is My Money")
    window.geometry("1000x1000")

    # GET DATA
    finance_data = finance.load_data()
    wishlist = load_wishlist()
    screen_show = []

    # ADD EXPENSE FUNCTION
    def add_expense():
        category = category_entry.get()
        amount = amount_entry.get()
        description = description_entry.get()

        # Check if input is empty and Convert amount into float
        if category == "" or amount == "":
            result_label.config(
                text="Please fill category and amount.",
                fg="red",
                font=("Arial", 18, "bold")
            )
            return
        amount = float(amount)

        # Add expense to list
        finance.add_expense(finance_data, category, amount, description)
        finance.save_data(finance_data)
        balance = finance.show_balance(finance_data)
        screen_show.append(
            f"{category} - "
            f"${amount:.2f} "
            f"{description}"
        )
        try:
            remove_item(wishlist, description)
        except:
            pass

        # Show result
        result_label.config(
            text=f"Enjoy Your {category}! 💖",
            fg="red",
            font=("Arial", 18, "bold")
        )
        list_result = get_items(wishlist)
        special_label.config(text=f"Wishlist: {list_result}")
        update_balance_display(balance_label, balance)
        # Update expense display
        update_show_list()
        # Clear input boxes
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)

    # ADD INCOME FUNCTION
    def add_income():
        # Get input
        income = income_entry.get()

        # Check if input is empty and Convert income into float
        if income == "":
            result_label.config(
                text="Please fill income.",
                fg="red",
                font=("Arial", 18, "bold")
            )
            return
        income = float(income)

        # Add income
        finance.add_income(finance_data, income)
        finance.save_data(finance_data)
        balance = finance.show_balance(finance_data)
        screen_show.append(f"Income add ${income}")

        # Show result
        result_label.config(
            text=f"Good saver! 👍",
            fg="red",
            font=("Arial", 18, "bold")
        )
        update_balance_display(balance_label, balance)
        # Update expense display
        update_show_list()
        # Clear input boxes
        income_entry.delete(0, tk.END)

    def add_wish_item():
        name = name_entry.get()
        price = price_entry.get()

        # Validation
        if name == "" or price == "":
            result_label.config(
                text="Please fill name and price.",
                fg="red",
                font=("Arial", 18, "bold")
            )
            return

        try:
            price = float(price)
        except:
            result_label.config(text="Price should be float", fg="red", font=("Arial", 18, "bold"))
            return
        # Add item
        add_item(wishlist, name, price)
        screen_show.append(f"Add {name} into wishlist")

        list_result = get_items(wishlist)

        # Refresh display
        result_label.config(text=f"Go for {name}", fg="red", font=("Arial", 18, "bold"))
        special_label.config(text=f"Wishlist: {list_result}")
        update_show_list()
        # Clear input boxes
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

    # SHOW EXPENSES FUNCTION
    def show_expenses():
        # Get input
        category = category_entry.get()

        # Check if input is empty
        if category == "":
            result_label.config(text="Please fill category.", fg="red", font=("Arial", 18, "bold"))
            return

        # Add income
        output = finance.show_expenses(finance_data, category)
        balance = finance.show_balance(finance_data)
        screen_show.append(output)

        # Show result
        result_label.config(
            text=f"Let's see your {category}'s expenses",
            fg="red",
            font=("Arial", 18, "bold")
        )
        update_balance_display(balance_label, balance)
        # Update expense display
        update_show_list()
        # Clear input boxes
        category_entry.delete(0, tk.END)

    def update_balance_display(balance_label, balance):
        if balance < 0:
            color = "red"
            emoji = "💀"
        elif balance < 100:
            color = "orange"
            emoji = "😰"
        elif balance < 500:
            color = "blue"
            emoji = "😊"
        else:
            color = "green"
            emoji = "🎉"
            # status = "Rich"

        balance_label.config(
            text=f"Balance: ${balance:.2f} {emoji}",
            fg=color
        )

    # UPDATE EXPENSE DISPLAY
    def update_show_list():

        # Clear old text
        show_listbox.delete(0, tk.END)

        # Display all expenses
        for inform in screen_show:
            for line in inform.split('\n'):
                if line:  # 只插入非空行
                    show_listbox.insert(tk.END, line)

    # 配置主窗口的grid权重
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=0)
    window.grid_columnconfigure(2, weight=1)

    window.grid_rowconfigure(0, weight=0)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=0)

    # ============ 顶部：Balance和Wishlist（居中，水平排列）============
    top_frame = tk.Frame(window)
    top_frame.grid(row=0, column=1, pady=20)
    # 创建两个子框架用于放置Balance和Wishlist
    balance_frame = tk.Frame(top_frame, relief="groove", bd=2, padx=20, pady=10)
    balance_frame.pack(side="left", padx=20)
    wishlist_frame = tk.Frame(top_frame, relief="groove", bd=2, padx=20, pady=10)
    wishlist_frame.pack(side="left", padx=20)

    balance_label = tk.Label(
        balance_frame,
        text="Balance:"
    )
    balance_label.pack()
    balance = finance.show_balance(finance_data)
    update_balance_display(balance_label, balance)

    special_label = tk.Label(
        wishlist_frame,
        text="Special Wishlist:"
    )
    special_label.pack()
    list_result = get_items(wishlist)
    special_label.config(text=f"Wishlist: {list_result}")

    # ============ 中间部分：左右两列 ============
    middle_frame = tk.Frame(window)
    middle_frame.grid(row=1, column=1, sticky="nsew", pady=20)
    # 配置中间框架的grid权重
    middle_frame.grid_columnconfigure(0, weight=1)  # 左列
    middle_frame.grid_columnconfigure(1, weight=1)  # 右列
    middle_frame.grid_rowconfigure(0, weight=1)
    # 左侧框架（收入和支出）
    left_frame = tk.LabelFrame(middle_frame, text="📊 Finance Management", font=("Arial", 12, "bold"), padx=20, pady=10)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10)
    # 右侧框架（心愿单管理）
    right_frame = tk.LabelFrame(middle_frame, text="✨ Wishlist Management", font=("Arial", 12, "bold"), padx=20, pady=10)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10)
    # 配置左右框架内部的grid权重
    left_frame.grid_columnconfigure(0, weight=0)  # 标签列
    left_frame.grid_columnconfigure(1, weight=1)  # 输入框列
    right_frame.grid_columnconfigure(0, weight=0)
    right_frame.grid_columnconfigure(1, weight=1)

    left_row = 0

    income_title = tk.Label(
        left_frame,
        text="👏 Your income",
        font=("Arial", 18, "bold")
    )
    income_title.grid(row=left_row, column=0, columnspan=2, pady=10, sticky="w")
    left_row += 1

    # INCOME INPUT
    income_label = tk.Label(
        left_frame,
        text="income:"
    )
    income_label.grid(row=left_row, column=0, padx=(0, 10), pady=5, sticky="e")
    income_entry = tk.Entry(left_frame, width=25)
    income_entry.grid(row=left_row, column=1, pady=5, sticky="ew")
    left_row += 1

    add_button = tk.Button(
        left_frame,
        text="Add Income",
        command=add_income
    )
    add_button.grid(row=left_row, column=0, columnspan=2, pady=10)
    left_row += 1

    # 分隔线
    tk.Frame(left_frame, height=2, bg="gray").grid(row=left_row, column=0, columnspan=2, sticky="ew", pady=10)
    left_row += 1

    expense_title = tk.Label(
        left_frame,
        text="😈 Things you buy",
        font=("Arial", 18, "bold")
    )
    expense_title.grid(row=left_row, column=0, columnspan=2, pady=10, sticky="w")
    left_row += 1

    # CATEGORY INPUT
    category_label = tk.Label(
        left_frame,
        text="Category:"
    )
    category_label.grid(row=left_row, column=0, padx=(0, 10), pady=5, sticky="e")
    category_entry = tk.Entry(left_frame)
    category_entry.grid(row=left_row, column=1, pady=5, sticky="ew")
    left_row += 1

    # AMOUNT INPUT
    amount_label = tk.Label(
        left_frame,
        text="Amount:"
    )
    amount_label.grid(row=left_row, column=0, padx=(0, 10), pady=5, sticky="e")
    amount_entry = tk.Entry(left_frame)
    amount_entry.grid(row=left_row, column=1, pady=5, sticky="ew")
    left_row += 1

    # DESCRIPTION INPUT
    description_label = tk.Label(
        left_frame,
        text="Description:"
    )
    description_label.grid(row=left_row, column=0, padx=(0, 10), pady=5, sticky="e")
    description_entry = tk.Entry(left_frame)
    description_entry.grid(row=left_row, column=1, pady=5, sticky="ew")
    left_row += 1

    # ADD BUTTON
    add_button = tk.Button(
        left_frame,
        text="Add Expense",
        command=add_expense
    )
    add_button.grid(row=left_row, column=0, columnspan=2, pady=10)
    left_row += 1

    add_button = tk.Button(
        left_frame,
        text="Show Expenses",
        command=show_expenses
    )
    add_button.grid(row=left_row, column=0, columnspan=2, pady=5)
    left_row += 1

    # ============ 右侧框架内容 ============
    right_row = 0

    add_wish_title = tk.Label(
        right_frame,
        text="⭐ Special Wishlist",
        font=("Arial", 18, "bold")
    )
    add_wish_title.grid(row=right_row, column=0, columnspan=2, pady=10, sticky="w")
    right_row += 1

    name_label = tk.Label(
        right_frame,
        text="Item Name"
    )
    name_label.grid(row=right_row, column=0, padx=(0, 10), pady=5, sticky="e")
    name_entry = tk.Entry(right_frame, width=25)
    name_entry.grid(row=right_row, column=1, pady=5, sticky="ew")
    right_row += 1

    price_label = tk.Label(right_frame, text="Price:")
    price_label.grid(row=right_row, column=0, padx=(0, 10), pady=5, sticky="e")
    price_entry = tk.Entry(right_frame, width=25)
    price_entry.grid(row=right_row, column=1, pady=5, sticky="ew")
    right_row += 1

    add_button = tk.Button(
        right_frame,
        text="Add Wish Item",
        command=add_wish_item,
        bg="lightblue",
        width=20
    )
    add_button.grid(row=right_row, column=0, columnspan=2, pady=15)
    right_row += 1

    # ============ 底部：Listbox（居中显示）============
    bottom_frame = tk.Frame(window)
    bottom_frame.grid(row=2, column=1, pady=20)

    # RESULT AND BALANCE LABEL
    result_label = tk.Label(
        bottom_frame,
        text=""
    )
    result_label.pack()

    # Listbox标题
    listbox_title = tk.Label(bottom_frame, text="📋 Recent Record", font=("Arial", 12, "bold"))
    listbox_title.pack()

    # 创建带滚动条的Listbox
    listbox_frame = tk.Frame(bottom_frame)
    listbox_frame.pack(pady=10)

    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side="right", fill="y")

    show_listbox = tk.Listbox(
        listbox_frame,
        width=80,
        height=8,
        yscrollcommand=scrollbar.set,
        font=("Arial", 10)
    )
    show_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=show_listbox.yview)

    # START GUI
    window.mainloop()
