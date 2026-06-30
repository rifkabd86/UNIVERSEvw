from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='user')  # 'user' or 'admin'
    status = db.Column(db.String(50), default='active')  # 'active' or 'inactive'
    membership = db.Column(db.String(50), default='free')  # 'free' or 'premium'
    phone = db.Column(db.String(20), nullable=True)
    photo_url = db.Column(db.String(256), nullable=True, default='/static/images/default-profile.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cart_items = db.relationship('Cart', backref='user', lazy=True, cascade="all, delete-orphan")
    wishlist_items = db.relationship('Wishlist', backref='user', lazy=True, cascade="all, delete-orphan")
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(100), nullable=True, default='fa-folder')  # FontAwesome class
    
    # Relationships
    subcategories = db.relationship('SubCategory', backref='category', lazy=True, cascade="all, delete-orphan")


class SubCategory(db.Model):
    __tablename__ = 'subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # Relationships
    templates = db.relationship('Template', backref='subcategory', lazy=True)


class Template(db.Model):
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text, nullable=True)
    file_format = db.Column(db.String(100), nullable=False, default='DOCX, PDF')
    thumbnail_url = db.Column(db.String(256), nullable=True, default='/static/images/default-thumbnail.jpg')
    file_url = db.Column(db.String(256), nullable=True)  # Path to the downloadable template file
    rating_avg = db.Column(db.Float, default=5.0)
    sales_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='active')  # 'active' or 'inactive'
    is_best_seller = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cart_entries = db.relationship('Cart', backref='template', lazy=True, cascade="all, delete")
    wishlist_entries = db.relationship('Wishlist', backref='template', lazy=True, cascade="all, delete")
    transaction_details = db.relationship('TransactionDetail', backref='template', lazy=True)
    reviews = db.relationship('Review', backref='template', lazy=True, cascade="all, delete-orphan")


class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), default='pending')  # 'pending', 'completed', 'failed'
    payment_proof = db.Column(db.String(256), nullable=True)  # File path to transfer slip image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    details = db.relationship('TransactionDetail', backref='transaction', lazy=True, cascade="all, delete-orphan")


class TransactionDetail(db.Model):
    __tablename__ = 'transaction_details'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
