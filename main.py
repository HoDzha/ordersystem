import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    order_details TEXT NOT NULL,
    status TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


def view_orders():
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()


def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
        (customer_name_entry.get(), order_details_entry.get()))
    conn.commit()
    conn.close()
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    view_orders()


def complete_order():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")


def delete_order():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM orders WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для удаления")


# Создаем приложение
app = tk.Tk()
app.title("Система управления заказами")

# Основной фрейм
main_frame = tk.Frame(app, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Фрейм ввода данных
input_frame = tk.LabelFrame(main_frame, text="Добавление заказа", padx=10, pady=10)
input_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(input_frame, text="Имя клиента:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
customer_name_entry = tk.Entry(input_frame, width=40)
customer_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Детали заказа:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
order_details_entry = tk.Entry(input_frame, width=40)
order_details_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(input_frame, text="Добавить заказ", command=add_order)
add_button.grid(row=2, column=0, columnspan=2, pady=10)

# Фрейм кнопок управления
buttons_frame = tk.Frame(main_frame)
buttons_frame.pack(fill=tk.X, padx=10, pady=5)

complete_button = tk.Button(buttons_frame, text="Завершить заказ", command=complete_order)
complete_button.pack(side=tk.LEFT, padx=5, pady=5)

delete_button = tk.Button(buttons_frame, text="Удалить заказ", command=delete_order)
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

# Фрейм отображения заказов
table_frame = tk.LabelFrame(main_frame, text="Список заказов", padx=10, pady=10)
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
for column in columns:
    tree.heading(column, text=column)
tree.pack(fill=tk.BOTH, expand=True)

# Инициализация базы данных и загрузка данных
init_db()
view_orders()

app.mainloop()
