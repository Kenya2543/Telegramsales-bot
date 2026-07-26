"""
seed_products.py
Loads your starter product catalog: 6 products across Clothing, Footwear,
Home & Kitchen, and Accessories, each with a USD price and stock quantity.

Run once with: python seed_products.py

Safe to re-run — it just adds rows, so if you run it twice you'll get
duplicate entries. Use /listproducts and /removeproduct in the bot to
clean up if that happens.
"""
import database as db

db.init_db()

# (name, description, price_usd, image_url, category, stock_quantity)
products = [
    ("Classic Cotton Shirt", "Men's short-sleeve shirt, sizes S-XL", 15.99, "", "Clothing", 40),
    ("Denim Trousers", "Slim-fit denim trousers, sizes 30-38", 24.99, "", "Clothing", 30),
    ("Ceramic Dinner Plate Set", "Set of 4 dinner plates, 10 inch", 19.99, "", "Home & Kitchen", 25),
    ("Everyday Running Shoes", "Lightweight running shoes, sizes 40-45", 34.99, "", "Footwear", 20),
    ("Straw Sun Hat", "Wide-brim straw hat, one size", 9.99, "", "Accessories", 35),
    ("Classic Baseball Cap", "Adjustable cotton baseball cap", 7.99, "", "Accessories", 50),
]

for name, description, price, image_url, category, stock in products:
    db.add_product(name, description, price, image_url, category, stock)

print(f"Seeded {len(products)} products.")
