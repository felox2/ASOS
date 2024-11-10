# seed.py
import uuid
from sqlmodel import Session, SQLModel, create_engine
from datetime import datetime
from models.category import Category, AssociationProductCategory
from models.product import Product, Photo
from models.brand import Brand
from config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URL)


def create_seed_data():
    with Session(engine) as session:
        brand1 = Brand(
            id=uuid.uuid4(),
            name="TechBrand",
            description="A leading brand in technology",
            photo="https://via.placeholder.com/150/0000FF/808080?text=TechBrand",
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        brand2 = Brand(
            id=uuid.uuid4(),
            name="HomeBrand",
            description="A trusted brand for home appliances",
            photo="https://via.placeholder.com/150/FF0000/FFFFFF?text=HomeBrand",
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        category3 = Category(
            id=uuid.uuid4(),
            name="Electronics",
            description="Various electronic devices",
            photo="https://via.placeholder.com/150/00FF00/000000?text=Electronics",
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        category4 = Category(
            id=uuid.uuid4(),
            name="Home Appliances",
            description="Appliances for home use",
            photo="https://via.placeholder.com/150/FFFF00/000000?text=Home+Appliances",
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        # Create products
        product4 = Product(
            id=uuid.uuid4(),
            name="Tablet",
            description="Latest model tablet",
            price=499.99,
            stock_quantity=75,
            photo="https://via.placeholder.com/150/0000FF/808080?text=Tablet",
            brand_id=brand1.id,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        product5 = Product(
            id=uuid.uuid4(),
            name="Smartwatch",
            description="Smartwatch with various features",
            price=199.99,
            stock_quantity=150,
            photo="https://via.placeholder.com/150/FF0000/FFFFFF?text=Smartwatch",
            brand_id=brand1.id,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        product6 = Product(
            id=uuid.uuid4(),
            name="Refrigerator",
            description="Energy-efficient refrigerator",
            price=899.99,
            stock_quantity=20,
            photo="https://via.placeholder.com/150/00FF00/000000?text=Refrigerator",
            brand_id=brand2.id,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        product7 = Product(
            id=uuid.uuid4(),
            name="Microwave Oven",
            description="High-power microwave oven",
            price=149.99,
            stock_quantity=40,
            photo="https://via.placeholder.com/150/FFFF00/000000?text=Microwave+Oven",
            brand_id=brand2.id,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        photos = [
            Photo(url="https://via.placeholder.com/150/0000FF/808080?text=Tablet+Side", product_id=product4.id),
            Photo(url="https://via.placeholder.com/150/0000FF/808080?text=Tablet+Back", product_id=product4.id),
            Photo(url="https://via.placeholder.com/150/FF0000/FFFFFF?text=Smartwatch+Side", product_id=product5.id),
            Photo(url="https://via.placeholder.com/150/FF0000/FFFFFF?text=Smartwatch+Back", product_id=product5.id),
            Photo(url="https://via.placeholder.com/150/00FF00/000000?text=Refrigerator+Side", product_id=product6.id),
            Photo(url="https://via.placeholder.com/150/00FF00/000000?text=Refrigerator+Inside", product_id=product6.id),
            Photo(url="https://via.placeholder.com/150/FFFF00/000000?text=Microwave+Side", product_id=product7.id),
            Photo(url="https://via.placeholder.com/150/FFFF00/000000?text=Microwave+Inside", product_id=product7.id)
        ]

        association4 = AssociationProductCategory(
            product_id=product4.id,
            category_id=category3.id
        )
        association5 = AssociationProductCategory(
            product_id=product5.id,
            category_id=category3.id
        )
        association6 = AssociationProductCategory(
            product_id=product6.id,
            category_id=category4.id
        )
        association7 = AssociationProductCategory(
            product_id=product7.id,
            category_id=category4.id
        )

        session.add_all([brand1, brand2, category3, category4, product4, product5, product6, product7] + photos + [association4, association5, association6, association7])
        session.commit()

create_seed_data()