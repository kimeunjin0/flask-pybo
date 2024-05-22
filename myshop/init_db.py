from app import app, db
from models import Product

with app.app_context():
    # 데이터베이스 초기화
    db.create_all()

    # 예제 상품 데이터 추가
    products = [
        {"name": "Cotton Shirt", "description": "Comfortable cotton shirt for everyday wear.", "price": 29.99,
         "image": "cotton_shirt.jpg", "category": "Shirts"},
        {"name": "Denim Jeans", "description": "Classic denim jeans with a modern fit.", "price": 49.99,
         "image": "denim_jeans.jpg", "category": "Pants"},
        {"name": "Summer Dress", "description": "Light and breezy dress perfect for summer.", "price": 39.99,
         "image": "summer_dress.jpg", "category": "Dresses"},
        {"name": "Leather Jacket", "description": "Stylish leather jacket for a cool look.", "price": 89.99,
         "image": "leather_jacket.jpg", "category": "Jackets"},
        {"name": "Sneakers", "description": "Comfortable and trendy sneakers.", "price": 59.99, "image": "sneakers.jpg",
         "category": "Shoes"},
        {"name": "Wool Coat", "description": "Warm wool coat for winter.", "price": 120.00, "image": "wool_coat.jpg",
         "category": "Coats"},
        {"name": "Casual Trousers", "description": "Casual trousers for a relaxed fit.", "price": 35.00,
         "image": "casual_trousers.jpg", "category": "Pants"},
        {"name": "Silk Scarf", "description": "Elegant silk scarf with a smooth texture.", "price": 25.00,
         "image": "silk_scarf.jpg", "category": "Accessories"},
        {"name": "Linen Shorts", "description": "Light and comfortable linen shorts.", "price": 30.00,
         "image": "linen_shorts.jpg", "category": "Shorts"},
        {"name": "Baseball Cap", "description": "Classic baseball cap with adjustable strap.", "price": 20.00,
         "image": "baseball_cap.jpg", "category": "Accessories"}
    ]

    for product in products:
        new_product = Product(
            name=product["name"],
            description=product["description"],
            price=product["price"],
            image=product["image"],
            category=product["category"]
        )
        db.session.add(new_product)

    db.session.commit()
    print("Database has been initialized with example products.")
