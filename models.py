from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.expression import null
import database
from sqlalchemy.orm import relationship


user_favorites = Table(
    "user_favorites",
    database.Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("food?id", ForeignKey("foods.id"), primary_key=True),
)
food_categories = Table(
    "food_categories",
    database.Base.metadata,
    Column("food_id", ForeignKey("foods.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class User(database.Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    favorites = relationship("Food", secondary=user_favorites, back_populates="users")
    id = Column(Integer, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Food(database.Base):
    __tablename__ = "foods"
    name = Column(String, nullable=False)
    total_time = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    fat = Column(Integer, nullable=False)
    carbs = Column(Integer, nullable=False)
    protein = Column(Integer, nullable=False)
    ingridients = relationship("FoodIngridient", back_populates="foods")
    directions = relationship("FoodDirection", back_populates="foods")
    categories = relationship(
        "Category", secondary="food_categories", back_populates="foods"
    )
    id = Column(Integer, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Category(database.Base):
    __tablename__ = "categories"
    categoryname = Column(String, nullable=False)
    foods = relationship(
        "Food", secondary="food_categories", back_populates="categories"
    )
    id = Column(Integer, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class FoodIngridient(database.Base):
    __tablename__ = "foodingridients"
    food_id = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"))
    ingridient  = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)


class FoodDirection(database.Base):
    __tablename__ = "fooddirections"
    food_id = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"))
    direction  = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
