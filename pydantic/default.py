from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    

product_one = Product(name="Mouse", price=5.00, in_stock=False)
print(product_one)

# Not throw error because in_stock has default value
product_two = Product(name="Keyboard", price=10.00)
print(product_two)