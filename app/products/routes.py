from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.products.models import Category, Product
from app.products.schemas import CategoryCreate, ProductCreate, CategoryResponse, ProductResponse
from app.utils.security import get_current_user

products_router = APIRouter()

# ✅ CREATE CATEGORY
@products_router.post("/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    category_exists = db.query(Category).filter(
        Category.name == category.name, Category.user_id == current_user.id
    ).first()
    if category_exists:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category.name, user_id=current_user.id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# ✅ GET ALL CATEGORIES
@products_router.get("/categories", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    return db.query(Category).filter(Category.user_id == current_user.id).all()

# ✅ UPDATE CATEGORY
@products_router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    existing_category = db.query(Category).filter(
        Category.id == category_id, Category.user_id == current_user.id
    ).first()

    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    existing_category.name = category.name
    db.commit()
    db.refresh(existing_category)
    return existing_category

# ✅ DELETE CATEGORY
@products_router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    category = db.query(Category).filter(
        Category.id == category_id, Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"msg": "Category deleted successfully"}

# ✅ CREATE PRODUCT
@products_router.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    category = db.query(Category).filter(
        Category.id == product.category_id, Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=400, detail="Category not found")

    new_product = Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id,
        user_id=current_user.id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# ✅ GET ALL PRODUCTS
@products_router.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    return db.query(Product).filter(Product.user_id == current_user.id).all()

# ✅ UPDATE PRODUCT
@products_router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    existing_product = db.query(Product).filter(
        Product.id == product_id, Product.user_id == current_user.id
    ).first()

    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.quantity = product.quantity
    existing_product.category_id = product.category_id

    db.commit()
    db.refresh(existing_product)
    return existing_product

# ✅ DELETE PRODUCT
@products_router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    product = db.query(Product).filter(
        Product.id == product_id, Product.user_id == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"msg": "Product deleted successfully"}
