import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, g
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Category, SubCategory, Template, Cart, Wishlist, Transaction, TransactionDetail, Review

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Initialize Cloudinary (if configured)
if app.config.get('USE_CLOUDINARY'):
    import cloudinary
    import cloudinary.uploader
    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET'],
        secure=True
    )

# Helper function to check allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'xlsx', 'pptx', 'zip', 'rar'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file, folder='general'):
    """Upload file to Cloudinary (production) or local disk (development).
    Returns the public URL string for storing in database."""
    if not file or not allowed_file(file.filename):
        return None
    
    filename = f"{folder}_{int(datetime.utcnow().timestamp())}_{secure_filename(file.filename)}"
    
    if app.config.get('USE_CLOUDINARY'):
        # Upload to Cloudinary
        try:
            result = cloudinary.uploader.upload(
                file,
                folder=f"templateverse/{folder}",
                public_id=filename.rsplit('.', 1)[0],
                resource_type='auto'
            )
            return result.get('secure_url')
        except Exception as e:
            app.logger.error(f"Cloudinary upload error: {e}")
            return None
    else:
        # Save to local disk
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(upload_dir, exist_ok=True)
        file.save(os.path.join(upload_dir, filename))
        return f"/static/uploads/{folder}/{filename}"

# Custom Authentication Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan masuk terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan masuk sebagai admin.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Akses ditolak. Anda tidak memiliki izin untuk halaman ini.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Stale Session Check before any request
@app.before_request
def check_stale_session():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()

# Context Processor to expose global data to templates
@app.context_processor
def inject_global_data():
    categories_global = Category.query.order_by(Category.name).all()
    current_user = None
    cart_count_global = 0
    wishlist_count_global = 0
    user_wishlist_ids = []

    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])
        if current_user and current_user.role == 'user':
            cart_count_global = Cart.query.filter_by(user_id=current_user.id).count()
            wishlist_count_global = Wishlist.query.filter_by(user_id=current_user.id).count()
            user_wishlist_ids = [w.template_id for w in Wishlist.query.filter_by(user_id=current_user.id).all()]

    return dict(
        categories_global=categories_global,
        current_user=current_user,
        cart_count_global=cart_count_global,
        wishlist_count_global=wishlist_count_global,
        user_wishlist_ids=user_wishlist_ids
    )

# ----------------- CLIENT ROUTES -----------------

@app.route('/')
def index():
    q = request.args.get('q', '')
    cat_id = request.args.get('category', type=int)
    subcat_id = request.args.get('subcategory', type=int)
    
    query = Template.query.filter_by(status='active')
    
    if q:
        query = query.filter(Template.name.like(f"%{q}%") | Template.description.like(f"%{q}%"))
    
    if subcat_id:
        query = query.filter_by(subcategory_id=subcat_id)
    elif cat_id:
        # Get all subcategories in the category
        subcat_ids = [sub.id for sub in SubCategory.query.filter_by(category_id=cat_id).all()]
        query = query.filter(Template.subcategory_id.in_(subcat_ids))

    templates = query.order_by(Template.sales_count.desc()).all()
    categories = Category.query.all()
    
    current_category_obj = Category.query.get(cat_id) if cat_id else None
    
    return render_template(
        'index.html',
        templates=templates,
        categories=categories,
        selected_category=cat_id,
        selected_subcategory=subcat_id,
        current_category_obj=current_category_obj
    )

@app.route('/membership')
def membership():
    return render_template('membership.html')

@app.route('/product/<int:template_id>')
def product_detail(template_id):
    template = Template.query.get_or_404(template_id)
    reviews = Review.query.filter_by(template_id=template_id).order_by(Review.created_at.desc()).all()
    
    has_purchased = False
    has_reviewed = False
    if 'user_id' in session:
        user_id = session['user_id']
        # Check if user has a completed transaction with this template
        has_purchased = db.session.query(TransactionDetail).join(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.payment_status == 'completed',
            TransactionDetail.template_id == template_id
        ).first() is not None
        
        # Or if the user has a premium membership or is admin
        user = User.query.get(user_id)
        if user and (user.membership == 'premium' or user.role == 'admin'):
            has_purchased = True
            
        has_reviewed = Review.query.filter_by(user_id=user_id, template_id=template_id).first() is not None
        
    return render_template(
        'detail.html',
        template=template,
        reviews=reviews,
        has_purchased=has_purchased,
        has_reviewed=has_reviewed
    )

@app.route('/product/<int:template_id>/review', methods=['POST'])
@login_required
def submit_review(template_id):
    user_id = session['user_id']
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '')
    
    # Verify purchase
    has_purchased = db.session.query(TransactionDetail).join(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.payment_status == 'completed',
        TransactionDetail.template_id == template_id
    ).first() is not None
    
    user = User.query.get(user_id)
    if user and user.membership == 'premium':
        has_purchased = True

    if not has_purchased:
        flash('Anda harus membeli template ini terlebih dahulu sebelum memberikan ulasan.', 'danger')
        return redirect(url_for('product_detail', template_id=template_id))
        
    existing_review = Review.query.filter_by(user_id=user_id, template_id=template_id).first()
    if existing_review:
        flash('Anda sudah memberikan ulasan untuk template ini.', 'warning')
        return redirect(url_for('product_detail', template_id=template_id))

    new_review = Review(
        user_id=user_id,
        template_id=template_id,
        rating=rating,
        comment=comment
    )
    db.session.add(new_review)
    db.session.commit()
    
    # Recalculate average rating
    all_reviews = Review.query.filter_by(template_id=template_id).all()
    avg_rating = sum([r.rating for r in all_reviews]) / len(all_reviews)
    template = Template.query.get(template_id)
    template.rating_avg = round(avg_rating, 1)
    db.session.commit()
    
    flash('Ulasan Anda berhasil dikirim!', 'success')
    return redirect(url_for('product_detail', template_id=template_id))

# ----------------- AUTH ROUTES -----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        
        if user and user.check_password(password):
            if user.status != 'active':
                flash('Akun Anda dinonaktifkan. Silakan hubungi admin.', 'danger')
                return redirect(url_for('login'))
                
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f"Selamat datang kembali, {user.username}!", "success")
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah.', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        # Check duplicate
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar.', 'danger')
            return redirect(url_for('register'))
            
        new_user = User(
            username=username,
            email=email,
            phone=phone,
            role='user',
            status='active',
            membership='free'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Pendaftaran berhasil! Silakan masuk.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah keluar dari akun.', 'success')
    return redirect(url_for('index'))

# ----------------- SHOPPING FLOW -----------------

@app.route('/cart/add/<int:template_id>', methods=['POST'])
@login_required
def add_to_cart(template_id):
    user_id = session['user_id']
    
    # Check if template is already bought
    has_purchased = db.session.query(TransactionDetail).join(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.payment_status == 'completed',
        TransactionDetail.template_id == template_id
    ).first() is not None
    
    if has_purchased:
        flash('Anda sudah memiliki template ini.', 'warning')
        return redirect(url_for('product_detail', template_id=template_id))
        
    # Check duplicate in cart
    if Cart.query.filter_by(user_id=user_id, template_id=template_id).first():
        flash('Template sudah ada di keranjang belanja.', 'info')
    else:
        new_cart = Cart(user_id=user_id, template_id=template_id)
        db.session.add(new_cart)
        db.session.commit()
        flash('Berhasil ditambahkan ke keranjang belanja!', 'success')
        
    return redirect(url_for('user_cart'))

@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != session['user_id']:
        flash('Aksi tidak sah.', 'danger')
        return redirect(url_for('index'))
        
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item dihapus dari keranjang belanja.', 'success')
    return redirect(url_for('user_cart'))

@app.route('/cart')
@login_required
def user_cart():
    user_id = session['user_id']
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total_price = sum([item.template.price for item in cart_items])
    return render_template('dashboard/cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/cart/instant/<int:template_id>', methods=['POST'])
@login_required
def instant_checkout(template_id):
    user_id = session['user_id']
    
    # Add to cart first if not exists
    if not Cart.query.filter_by(user_id=user_id, template_id=template_id).first():
        new_cart = Cart(user_id=user_id, template_id=template_id)
        db.session.add(new_cart)
        db.session.commit()
        
    return redirect(url_for('user_cart'))

@app.route('/cart/checkout', methods=['POST'])
@login_required
def checkout_cart():
    user_id = session['user_id']
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    
    if not cart_items:
        flash('Keranjang belanja Anda kosong.', 'warning')
        return redirect(url_for('index'))
        
    total_price = sum([item.template.price for item in cart_items])
    
    # Upload payment proof (only if total_price > 0)
    proof_path = None
    if total_price > 0:
        file = request.files.get('payment_proof')
        proof_path = upload_file(file, 'payment_proofs')
        if not proof_path:
            flash('Bukti pembayaran tidak valid.', 'danger')
            return redirect(url_for('user_cart'))

    # Create Transaction
    invoice = f"INV{int(datetime.utcnow().timestamp())}"
    new_tx = Transaction(
        invoice_number=invoice,
        user_id=user_id,
        total_price=total_price,
        payment_status='completed' if total_price == 0 else 'pending',
        payment_proof=proof_path
    )
    db.session.add(new_tx)
    db.session.commit()
    
    # Create Transaction Details
    for item in cart_items:
        detail = TransactionDetail(
            transaction_id=new_tx.id,
            template_id=item.template_id,
            price=item.template.price
        )
        db.session.add(detail)
        
        # If free transaction, increment template sales_count immediately
        if total_price == 0:
            item.template.sales_count += 1
            
        # Delete from cart
        db.session.delete(item)
        
    db.session.commit()
    
    if total_price == 0:
        flash('Transaksi berhasil diselesaikan! Anda dapat mengunduh template sekarang.', 'success')
        return redirect(url_for('user_templates'))
    else:
        flash('Pembayaran Anda berhasil dikirim! Silakan tunggu konfirmasi verifikasi dari Admin.', 'success')
        return redirect(url_for('user_history'))

@app.route('/membership/upgrade', methods=['POST'])
@login_required
def upgrade_membership():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user.membership == 'premium':
        flash('Anda sudah menjadi premium member.', 'warning')
        return redirect(url_for('membership'))
        
    file = request.files.get('payment_proof')
    proof_path = upload_file(file, 'payment_proofs')
    if not proof_path:
        flash('Bukti transfer tidak valid.', 'danger')
        return redirect(url_for('membership'))
        
    # Create a special pending transaction for membership upgrade
    invoice = f"MBR{int(datetime.utcnow().timestamp())}"
    new_tx = Transaction(
        invoice_number=invoice,
        user_id=user_id,
        total_price=49000,
        payment_status='pending',
        payment_proof=proof_path
    )
    db.session.add(new_tx)
    db.session.commit()
    
    flash('Bukti transfer peningkatan keanggotaan berhasil diunggah! Hubungi admin untuk verifikasi cepat.', 'success')
    return redirect(url_for('user_history'))

@app.route('/download/<int:template_id>')
@login_required
def download_template(template_id):
    user_id = session['user_id']
    user = User.query.get(user_id)
    template = Template.query.get_or_404(template_id)
    
    # Check if purchased
    has_purchased = db.session.query(TransactionDetail).join(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.payment_status == 'completed',
        TransactionDetail.template_id == template_id
    ).first() is not None
    
    # Or premium user / admin
    if user and (user.membership == 'premium' or user.role == 'admin'):
        has_purchased = True
        
    if not has_purchased:
        flash('Anda tidak memiliki izin untuk mengunduh template ini.', 'danger')
        return redirect(url_for('product_detail', template_id=template_id))
        
    if not template.file_url:
        flash('File template belum diunggah oleh admin.', 'warning')
        return redirect(url_for('product_detail', template_id=template_id))
        
    # Send file from directory
    filename = os.path.basename(template.file_url)
    directory = os.path.join(app.root_path, 'static', 'uploads', 'templates')
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/wishlist/toggle/<int:template_id>', methods=['POST'])
@login_required
def toggle_wishlist(template_id):
    user_id = session['user_id']
    existing = Wishlist.query.filter_by(user_id=user_id, template_id=template_id).first()
    
    if existing:
        db.session.delete(existing)
        flash('Dihapus dari wishlist.', 'success')
    else:
        new_wishlist = Wishlist(user_id=user_id, template_id=template_id)
        db.session.add(new_wishlist)
        flash('Ditambahkan ke wishlist!', 'success')
        
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

# ----------------- USER DASHBOARD ROUTES -----------------

@app.route('/dashboard')
@login_required
def user_dashboard():
    user_id = session['user_id']
    purchased_count = db.session.query(TransactionDetail).join(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.payment_status == 'completed'
    ).count()
    
    user = User.query.get(user_id)
    if user.membership == 'premium':
        # Premium can download all templates, so display total active templates count
        purchased_count = Template.query.filter_by(status='active').count()

    wishlist_count = Wishlist.query.filter_by(user_id=user_id).count()
    
    # Fetch recent purchased templates
    recent_txs = Transaction.query.filter_by(user_id=user_id, payment_status='completed').order_by(Transaction.created_at.desc()).limit(5).all()
    recent_templates = []
    for tx in recent_txs:
        for detail in tx.details:
            if detail.template not in recent_templates:
                recent_templates.append(detail.template)
                
    if user.membership == 'premium':
        # Add some featured templates for easy download
        recent_templates = Template.query.filter_by(status='active').limit(4).all()

    return render_template(
        'dashboard/index.html',
        purchased_count=purchased_count,
        wishlist_count=wishlist_count,
        recent_templates=recent_templates
    )

@app.route('/dashboard/templates')
@login_required
def user_templates():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if user.membership == 'premium':
        templates = Template.query.filter_by(status='active').all()
    else:
        txs = Transaction.query.filter_by(user_id=user_id, payment_status='completed').all()
        templates = []
        for tx in txs:
            for detail in tx.details:
                if detail.template not in templates:
                    templates.append(detail.template)
                    
    return render_template('dashboard/templates.html', templates=templates)

@app.route('/dashboard/wishlist')
@login_required
def user_wishlist():
    user_id = session['user_id']
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
    return render_template('dashboard/wishlist.html', wishlist_items=wishlist_items)

@app.route('/dashboard/history')
@login_required
def user_history():
    user_id = session['user_id']
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
    return render_template('dashboard/history.html', transactions=transactions)

@app.route('/dashboard/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            user.username = request.form.get('username')
            user.email = request.form.get('email')
            user.phone = request.form.get('phone')
            
            # Handle photo profile upload
            photo = request.files.get('photo')
            if photo and photo.filename:
                photo_url = upload_file(photo, 'profiles')
                if photo_url:
                    user.photo_url = photo_url
                
            db.session.commit()
            flash('Profil Anda berhasil diperbarui.', 'success')
            
        elif action == 'update_password':
            curr_pass = request.form.get('current_password')
            new_pass = request.form.get('new_password')
            conf_pass = request.form.get('confirm_password')
            
            if not user.check_password(curr_pass):
                flash('Password sekarang salah.', 'danger')
            elif new_pass != conf_pass:
                flash('Konfirmasi password tidak cocok.', 'danger')
            else:
                user.set_password(new_pass)
                db.session.commit()
                flash('Password berhasil diperbarui!', 'success')
                
        return redirect(url_for('user_profile'))
        
    return render_template('dashboard/profile.html')

# ----------------- ADMIN DASHBOARD ROUTES -----------------

@app.route('/admin')
@admin_required
def admin_dashboard():
    total_templates = Template.query.count()
    total_users = User.query.filter_by(role='user').count()
    total_transactions = Transaction.query.count()
    
    # Calculate revenue
    completed_txs = Transaction.query.filter_by(payment_status='completed').all()
    total_revenue = sum([tx.total_price for tx in completed_txs])
    
    top_templates = Template.query.order_by(Template.sales_count.desc()).limit(5).all()
    
    # Generate data for sales chart of last 7 days
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    labels = []
    revenue_data = []
    sales_count_data = []
    
    day_names_ind = {
        'Monday': 'Senin',
        'Tuesday': 'Selasa',
        'Wednesday': 'Rabu',
        'Thursday': 'Kamis',
        'Friday': 'Jumat',
        'Saturday': 'Sabtu',
        'Sunday': 'Minggu'
    }
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        day_name = date.strftime('%A')
        ind_day_name = day_names_ind.get(day_name, day_name)
        labels.append(f"{date.day} {date.strftime('%b')}") # e.g. "25 Jun"
        
        day_start = datetime.combine(date, datetime.min.time())
        day_end = datetime.combine(date, datetime.max.time())
        txs_today = Transaction.query.filter(
            Transaction.payment_status == 'completed',
            Transaction.created_at >= day_start,
            Transaction.created_at <= day_end
        ).all()
        
        revenue_today = sum([tx.total_price for tx in txs_today])
        revenue_data.append(revenue_today)
        
        sales_today = 0
        for tx in txs_today:
            sales_today += len(tx.details) if not tx.invoice_number.startswith('MBR') else 1
        sales_count_data.append(sales_today)
        
    # Get category distribution for category chart
    categories = Category.query.all()
    cat_labels = []
    cat_data = []
    for cat in categories:
        cat_labels.append(cat.name)
        sales_sum = db.session.query(db.func.sum(Template.sales_count)).join(SubCategory).filter(SubCategory.category_id == cat.id).scalar() or 0
        cat_data.append(sales_sum)
        
    return render_template(
        'admin/index.html',
        total_templates=total_templates,
        total_users=total_users,
        total_transactions=total_transactions,
        total_revenue=total_revenue,
        top_templates=top_templates,
        chart_labels=labels,
        chart_revenue=revenue_data,
        chart_sales=sales_count_data,
        cat_labels=cat_labels,
        cat_data=cat_data
    )

@app.route('/admin/upload', methods=['GET', 'POST'])
@admin_required
def admin_upload():
    categories = Category.query.all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        subcategory_id = request.form.get('subcategory')
        price = request.form.get('price', type=float)
        file_format = request.form.get('file_format')
        description = request.form.get('description')
        
        # Save files
        thumb_file = request.files.get('thumbnail')
        template_file = request.files.get('template_file')
        
        thumb_path = upload_file(thumb_file, 'thumbnails')
        temp_path = upload_file(template_file, 'templates')

        if not thumb_path or not temp_path:
            flash('Gagal mengunggah file. Pastikan format file didukung.', 'danger')
            return redirect(url_for('admin_upload'))
            
        new_template = Template(
            subcategory_id=subcategory_id,
            name=name,
            price=price,
            description=description,
            file_format=file_format,
            thumbnail_url=thumb_path,
            file_url=temp_path,
            status='active'
        )
        db.session.add(new_template)
        db.session.commit()
        
        flash('Template baru berhasil dipublikasikan!', 'success')
        return redirect(url_for('admin_products'))
        
    return render_template('admin/upload.html', categories=categories)

@app.route('/admin/products')
@admin_required
def admin_products():
    search = request.args.get('search', '')
    query = Template.query
    if search:
        query = query.filter(Template.name.like(f"%{search}%"))
        
    templates = query.all()
    return render_template('admin/products.html', templates=templates)

@app.route('/admin/products/edit/<int:template_id>', methods=['POST'])
@admin_required
def admin_edit_product(template_id):
    template = Template.query.get_or_404(template_id)
    template.name = request.form.get('name')
    template.price = request.form.get('price', type=float)
    template.status = request.form.get('status')
    template.description = request.form.get('description')
    
    db.session.commit()
    flash('Data template berhasil diperbarui.', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/delete/<int:template_id>', methods=['POST'])
@admin_required
def admin_delete_product(template_id):
    template = Template.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    flash('Template berhasil dihapus dari sistem.', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/categories')
@admin_required
def admin_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['POST'])
@admin_required
def admin_add_category():
    name = request.form.get('name')
    icon = request.form.get('icon') or 'fa-folder'
    
    if Category.query.filter_by(name=name).first():
        flash('Kategori sudah ada.', 'danger')
    else:
        new_cat = Category(name=name, icon=icon)
        db.session.add(new_cat)
        db.session.commit()
        flash('Kategori baru berhasil ditambahkan.', 'success')
        
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/subcategory/add', methods=['POST'])
@admin_required
def admin_add_subcategory():
    category_id = request.form.get('category_id')
    name = request.form.get('name')
    
    new_sub = SubCategory(category_id=category_id, name=name)
    db.session.add(new_sub)
    db.session.commit()
    
    flash('Subkategori baru berhasil ditambahkan.', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@admin_required
def admin_delete_category(category_id):
    cat = Category.query.get_or_404(category_id)
    db.session.delete(cat)
    db.session.commit()
    flash('Kategori berhasil dihapus.', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/subcategory/delete/<int:subcategory_id>', methods=['POST'])
@admin_required
def admin_delete_subcategory(subcategory_id):
    sub = SubCategory.query.get_or_404(subcategory_id)
    db.session.delete(sub)
    db.session.commit()
    flash('Subkategori berhasil dihapus.', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/users')
@admin_required
def admin_users():
    search = request.args.get('search', '')
    query = User.query
    if search:
        query = query.filter((User.username.like(f"%{search}%")) | (User.email.like(f"%{search}%")))
        
    users = query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/toggle/<int:user_id>', methods=['POST'])
@admin_required
def admin_toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.status == 'active':
        user.status = 'inactive'
        flash(f"Akun user {user.username} telah dinonaktifkan.", 'success')
    else:
        user.status = 'active'
        flash(f"Akun user {user.username} berhasil diaktifkan kembali.", 'success')
        
    db.session.commit()
    return redirect(url_for('admin_users'))

@app.route('/admin/transactions')
@admin_required
def admin_transactions():
    search = request.args.get('search', '')
    query = Transaction.query
    if search:
        query = query.join(User).filter((Transaction.invoice_number.like(f"%{search}%")) | (User.username.like(f"%{search}%")))
        
    transactions = query.order_by(Transaction.created_at.desc()).all()
    return render_template('admin/transactions.html', transactions=transactions)

@app.route('/admin/transactions/verify/<int:tx_id>/<string:action>', methods=['POST'])
@admin_required
def admin_verify_transaction(tx_id, action):
    tx = Transaction.query.get_or_404(tx_id)
    
    if action == 'approve':
        tx.payment_status = 'completed'
        
        # If it is a membership upgrade transaction (invoiced with prefix MBR)
        if tx.invoice_number.startswith('MBR'):
            user = User.query.get(tx.user_id)
            user.membership = 'premium'
            flash(f"Peningkatan Membership user {user.username} disetujui!", 'success')
        else:
            # Increment templates sales count
            for detail in tx.details:
                template = Template.query.get(detail.template_id)
                if template:
                    template.sales_count += 1
            flash(f"Transaksi {tx.invoice_number} berhasil disetujui!", 'success')
    else:
        tx.payment_status = 'failed'
        flash(f"Transaksi {tx.invoice_number} ditolak.", 'warning')
        
    db.session.commit()
    return redirect(url_for('admin_transactions'))

@app.route('/admin/reports')
@admin_required
def admin_reports():
    completed_txs = Transaction.query.filter_by(payment_status='completed').order_by(Transaction.created_at.desc()).all()
    total_revenue = sum([tx.total_price for tx in completed_txs])
    platform_fee = total_revenue * 0.15
    net_revenue = total_revenue - platform_fee
    
    # Generate data for sales chart of last 7 days
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    labels = []
    daily_revenue = []
    
    day_names_ind = {
        'Monday': 'Senin',
        'Tuesday': 'Selasa',
        'Wednesday': 'Rabu',
        'Thursday': 'Kamis',
        'Friday': 'Jumat',
        'Saturday': 'Sabtu',
        'Sunday': 'Minggu'
    }
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        day_name = date.strftime('%A')
        ind_day_name = day_names_ind.get(day_name, day_name)
        labels.append(ind_day_name)
        
        day_start = datetime.combine(date, datetime.min.time())
        day_end = datetime.combine(date, datetime.max.time())
        txs_today = Transaction.query.filter(
            Transaction.payment_status == 'completed',
            Transaction.created_at >= day_start,
            Transaction.created_at <= day_end
        ).all()
        daily_revenue.append(sum([tx.total_price for tx in txs_today]))
        
    return render_template(
        'admin/reports.html',
        completed_txs=completed_txs,
        total_revenue=total_revenue,
        platform_fee=platform_fee,
        net_revenue=net_revenue,
        chart_labels=labels,
        chart_data=daily_revenue
    )

@app.route('/admin/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            user.username = request.form.get('username')
            user.email = request.form.get('email')
            user.phone = request.form.get('phone')
            db.session.commit()
            flash('Profil Anda berhasil diperbarui.', 'success')
            
        elif action == 'update_password':
            curr_pass = request.form.get('current_password')
            new_pass = request.form.get('new_password')
            conf_pass = request.form.get('confirm_password')
            
            if not user.check_password(curr_pass):
                flash('Password sekarang salah.', 'danger')
            elif new_pass != conf_pass:
                flash('Konfirmasi password tidak cocok.', 'danger')
            else:
                user.set_password(new_pass)
                db.session.commit()
                flash('Password admin berhasil diperbarui!', 'success')
                
        return redirect(url_for('admin_profile'))
        
    return render_template('admin/profile.html')

# ----------------- ERROR HANDLERS -----------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error_code=404, error_message='Halaman tidak ditemukan'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', error_code=500, error_message='Terjadi kesalahan server'), 500

# ----------------- SERVER START -----------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=app.config.get('DEBUG', False))
