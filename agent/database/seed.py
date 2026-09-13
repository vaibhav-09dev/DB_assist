from sqlalchemy import text
from db import engine 


customers = [
    ("Alice", "alice@example.com", "Delhi", "2026-01-10"),
    ("Bob", "bob@example.com", "Mumbai", "2026-01-15"),
    ("Charlie", "charlie@example.com", "Delhi", "2026-02-01"),
    ("David", "david@example.com", "Bangalore", "2026-02-10"),
    ("Eva", "eva@example.com", "Mumbai", "2026-02-20"),
]

products = [
    ("Laptop", "Electronics", 75000),
    ("Phone", "Electronics", 50000),
    ("Headphones", "Accessories", 5000),
    ("Keyboard", "Accessories", 3000),
    ("Monitor", "Electronics", 25000),
]

orders = [
    (1, 1, 1, 75000, "2026-01-12"),
    (1, 3, 2, 10000, "2026-01-20"),
    (2, 2, 1, 50000, "2026-01-25"),
    (3, 1, 1, 75000, "2026-02-05"),
    (3, 4, 2, 6000, "2026-02-10"),
    (4, 5, 1, 25000, "2026-02-15"),
    (5, 2, 2, 100000, "2026-02-20"),
]


with engine.begin() as conn:
    for name, email, city, created_at in customers:
        conn.execute(
            text(
                """
                INSERT INTO customers
                (name, email, city, created_at)
                VALUES (:name, :email, :city, :created_at)

"""
            ),
             {
                "name": name,
                "email": email,
                "city": city,
                "created_at": created_at
            }
        )

    for name, category, price in products:

        conn.execute(
            text("""
                INSERT INTO products
                (name, category, price)
                VALUES (:name, :category, :price)
            """),
            {
                "name": name,
                "category": category,
                "price": price
            }
        )
    for customer_id, product_id, quantity, amount, order_date in orders:

        conn.execute(
            text("""
                INSERT INTO orders
                (customer_id, product_id, quantity, amount, order_date)
                VALUES (
                    :customer_id,
                    :product_id,
                    :quantity,
                    :amount,
                    :order_date
                )
            """),
            {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity,
                "amount": amount,
                "order_date": order_date
            }
        )
print("Database seeded successfully.")