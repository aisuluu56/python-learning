"""
Этап 07. Оформление заказа

Цель: создать экран оформления заказа с формой покупателя, проверкой данных,
промокодом и созданием заказа через backend-сервис.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import importlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ===== ИМПОРТ ИЗ ЗАДАНИЯ 17 =====
domain = importlib.import_module("17_clothing_store_project.01_domain_models.tasks")
repos = importlib.import_module("17_clothing_store_project.03_repositories.tasks")
cart_mod = importlib.import_module("17_clothing_store_project.05_cart.tasks")
order_mod = importlib.import_module("17_clothing_store_project.06_orders.tasks")
discount_mod = importlib.import_module("17_clothing_store_project.07_users_discounts.tasks")
db = importlib.import_module("17_clothing_store_project.02_postgresql_storage.tasks")

Customer = domain.Customer
CategoryRepository = repos.CategoryRepository
ProductRepository = repos.ProductRepository
StockRepository = repos.StockRepository
CustomerRepository = repos.CustomerRepository
OrderRepository = order_mod.OrderRepository
CartService = cart_mod.CartService
ExtendedOrderService = discount_mod.ExtendedOrderService
DiscountService = discount_mod.DiscountService
PromocodeRepository = discount_mod.PromocodeRepository
get_connection = db.get_connection


# Задание 1
# Создайте CheckoutFrame.
# Он должен получать корзину, сервис заказов и сервис скидок через __init__.
# TODO: создать экран оформления заказа

class CheckoutFrame(ttk.Frame):
    def __init__(self, parent, services):
        super().__init__(parent)
        self.services = services
        self.total = 0
        self.customer_id = 1          # временно, должен существовать в БД

        self.create_form()
        self.create_summary()
        self.create_buttons()
        self.refresh()

    # Задание 2
    # Добавьте форму покупателя:
    # имя, телефон или email, город, улица, дом, квартира.
    # TODO: добавить форму покупателя и адреса

    def create_form(self):
        form = ttk.LabelFrame(self, text="Данные покупателя", padding=10)
        form.pack(fill="x", padx=10, pady=5)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Имя:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form, text="Телефон:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.phone_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.phone_var, width=30).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form, text="Город:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.city_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.city_var, width=30).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(form, text="Улица:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.street_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.street_var, width=30).grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(form, text="Дом:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.house_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.house_var, width=15).grid(row=4, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(form, text="Квартира:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.apartment_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.apartment_var, width=15).grid(row=5, column=1, sticky="w", padx=5, pady=2)

        # Задание 3
        # Добавьте поле промокода и кнопку "Применить".
        # Результат применения скидки показывайте в интерфейсе.
        # TODO: добавить промокод

        ttk.Label(form, text="Промокод:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.promo_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.promo_var, width=20).grid(row=6, column=1, sticky="w", padx=5, pady=2)
        ttk.Button(form, text="Применить", command=self.apply_promo).grid(row=6, column=1, sticky="e", padx=5)

        self.promo_result_var = tk.StringVar()
        ttk.Label(form, textvariable=self.promo_result_var, foreground="green").grid(row=7, column=0, columnspan=2, pady=5)

    # Задание 4
    # Добавьте блок с кратким составом заказа и итоговой суммой.
    # Он должен обновляться при переходе на экран оформления.
    # TODO: добавить сводку заказа

    def create_summary(self):
        summary = ttk.LabelFrame(self, text="Состав заказа", padding=10)
        summary.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("name", "size", "quantity", "price")
        self.tree = ttk.Treeview(summary, columns=columns, show="headings", height=5)
        for c in columns:
            self.tree.heading(c, text=c.capitalize())
        self.tree.column("name", width=180)
        self.tree.column("size", width=60, anchor="center")
        self.tree.column("quantity", width=60, anchor="center")
        self.tree.column("price", width=80, anchor="center")

        scroll = ttk.Scrollbar(summary, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.total_var = tk.StringVar(value="Итого: 0 ₽")
        ttk.Label(summary, textvariable=self.total_var, font=("Arial", 12, "bold")).pack(pady=5)

    # Задание 4
    # TODO: добавить сводку заказа

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        items = self.services["cart_service"].get_cart().get_items()
        total = 0
        for item in items:
            self.tree.insert("", "end", values=(
                item.product.name,
                item.size,
                item.quantity,
                item.get_total()
            ))
            total += item.get_total()

        self.total = total
        self.total_var.set(f"Итого: {total} ₽")

    # Задание 3
    # TODO: добавить промокод

    def apply_promo(self):
        promo = self.promo_var.get().strip()
        if not promo:
            self.promo_result_var.set("Введите промокод")
            self.promo_result_var.config(foreground="red")
            return

        try:
            new_total = self.services["discount_service"].apply_promocode(self.total, promo)
            self.total_var.set(f"Итого: {new_total} ₽ (скидка {self.total - new_total} ₽)")
            self.promo_result_var.set(f"Промокод применен! Скидка: {self.total - new_total} ₽")
            self.promo_result_var.config(foreground="green")
        except ValueError as e:
            self.promo_result_var.set(str(e))
            self.promo_result_var.config(foreground="red")

    # Задание 5
    # Добавьте простую проверку формы на уровне GUI.
    # Например, имя и контакт не должны быть пустыми.
    # TODO: добавить проверку полей формы

    def validate_form(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Ошибка", "Введите имя")
            return False
        if not self.phone_var.get().strip():
            messagebox.showerror("Ошибка", "Введите телефон")
            return False
        if not self.city_var.get().strip():
            messagebox.showerror("Ошибка", "Введите город")
            return False
        if not self.street_var.get().strip():
            messagebox.showerror("Ошибка", "Введите улицу")
            return False
        return True

    def create_buttons(self):
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=5)

        # Задание 6
        # Добавьте кнопку "Оформить заказ".
        # Она должна вызвать backend-сервис оформления заказа.
        # TODO: добавить создание заказа

        ttk.Button(bottom, text="Оформить заказ", command=self.create_order).pack(side="right", padx=5)
        ttk.Button(bottom, text="Назад в корзину", command=self.go_back).pack(side="right", padx=5)

    # Задание 6
    # TODO: добавить создание заказа

    def create_order(self):
        # Задание 8: пустая корзина
        if not self.services["cart_service"].get_cart().get_items():
            messagebox.showerror("Ошибка", "Корзина пуста")
            return

        # Задание 5: проверка формы
        if not self.validate_form():
            return

        promo = self.promo_var.get().strip() or None

        # Задание 7
        # После успешного оформления покажите номер заказа,
        # очистите корзину и верните пользователя в каталог или на экран подтверждения.
        # TODO: добавить успешное завершение заказа

        try:
            order_id = self.services["order_service"].create_order(
                self.services["cart_service"].get_cart(),
                self.customer_id,
                promo
            )
            self.services["cart_service"].clear_cart()
            messagebox.showinfo("Успешно!", f"Заказ #{order_id} оформлен!")
            if hasattr(self.master, 'screen_manager'):
                self.master.screen_manager.show_frame("catalog")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def go_back(self):
        if hasattr(self.master, 'screen_manager'):
            self.master.screen_manager.show_frame("cart")


# Задание 8
# Проверьте ошибки:
# пустая корзина, пустые поля, неверный промокод, нехватка товара.
# TODO: проверить оформление заказа

if __name__ == "__main__":
    conn = get_connection()
    cat_repo = CategoryRepository(conn)
    prod_repo = ProductRepository(conn)
    stock_repo = StockRepository(conn)
    cust_repo = CustomerRepository(conn)
    order_repo = OrderRepository(conn)
    promo_repo = PromocodeRepository(conn)

    catalog = importlib.import_module("17_clothing_store_project.04_catalog_service.tasks").CatalogService(
        prod_repo, cat_repo, stock_repo
    )
    cart_service = CartService(catalog, stock_repo)
    discount_service = DiscountService(promo_repo)
    order_service = ExtendedOrderService(stock_repo, cust_repo, order_repo, conn, discount_service)

    services = {
        "cart_service": cart_service,
        "order_service": order_service,
        "discount_service": discount_service,
        "customer_repo": cust_repo,
    }

    # Добавляем тестовые товары (если есть в БД)
    try:
        p1 = prod_repo.get_by_id(1)
        p2 = prod_repo.get_by_id(2)
        if p1:
            cart_service.add_to_cart(p1, "M", 2)
        if p2:
            cart_service.add_to_cart(p2, "L", 1)
    except:
        pass

    root = tk.Tk()
    root.title("Оформление заказа")
    root.geometry("700x500")
    frame = CheckoutFrame(root, services)
    frame.pack(fill="both", expand=True)
    root.mainloop()
    conn.close()