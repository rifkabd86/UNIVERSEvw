from app import app
from models import db, User, Category, SubCategory, Template, Transaction, TransactionDetail, Review
from datetime import datetime, timedelta

def seed_data():
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()

        print("Seeding Categories & Subcategories...")
        # Categories
        cat_karier = Category(name="Karier & Profesional", icon="fa-briefcase")
        cat_pendidikan = Category(name="Pendidikan", icon="fa-graduation-cap")
        cat_bisnis = Category(name="Bisnis", icon="fa-chart-line")
        cat_desain = Category(name="Desain", icon="fa-palette")
        cat_produktivitas = Category(name="Produktivitas", icon="fa-check-double")

        db.session.add_all([cat_karier, cat_pendidikan, cat_bisnis, cat_desain, cat_produktivitas])
        db.session.commit()

        # Subcategories
        subcats = {
            cat_karier.id: [
                "CV ATS Friendly", "CV Kreatif", "Resume Internasional", 
                "Cover Letter", "Portofolio Kerja", "LinkedIn Profile"
            ],
            cat_pendidikan.id: [
                "Makalah", "Skripsi", "Proposal Penelitian", 
                "PPT Seminar", "Laporan PKL", "Jurnal"
            ],
            cat_bisnis.id: [
                "Invoice", "Proposal Bisnis", "Business Plan", 
                "Surat Penawaran", "Laporan Keuangan"
            ],
            cat_desain.id: [
                "Canva", "Poster", "Brosur", "Banner", "Feed Instagram"
            ],
            cat_produktivitas.id: [
                "Planner Harian", "To-Do List", "Budget Planner", 
                "Habit Tracker", "Kalender Digital"
            ]
        }

        subcategory_objects = {}
        for cat_id, names in subcats.items():
            subcategory_objects[cat_id] = []
            for name in names:
                sub = SubCategory(category_id=cat_id, name=name)
                db.session.add(sub)
                subcategory_objects[cat_id].append(sub)
        
        db.session.commit()

        # Get subcategories for reference
        sub_cv_ats = SubCategory.query.filter_by(name="CV ATS Friendly").first()
        sub_cv_kreatif = SubCategory.query.filter_by(name="CV Kreatif").first()
        sub_skripsi = SubCategory.query.filter_by(name="Skripsi").first()
        sub_invoice = SubCategory.query.filter_by(name="Invoice").first()
        sub_portfolio = SubCategory.query.filter_by(name="Portofolio Kerja").first()
        sub_ppt = SubCategory.query.filter_by(name="PPT Seminar").first()
        sub_budget = SubCategory.query.filter_by(name="Budget Planner").first()

        print("Seeding Users...")
        # Admin
        admin = User(
            username="admin", 
            email="admin@templateverse.com", 
            role="admin", 
            phone="08123456789",
            status="active"
        )
        admin.set_password("admin")
        
        # User Rifki
        user_rifki = User(
            username="Rifki", 
            email="rifki@email.com", 
            role="user", 
            phone="08987654321",
            status="active",
            membership="free"
        )
        user_rifki.set_password("user123")

        # More Users
        user_dinda = User(username="Dinda Ayu", email="dindaayu@email.com", role="user", phone="0822112233", status="active", membership="premium")
        user_dinda.set_password("user123")
        user_rizky = User(username="Rizky Pratama", email="rizky@email.com", role="user", phone="0833112233", status="active", membership="free")
        user_rizky.set_password("user123")
        user_amelia = User(username="Amelia Putri", email="amelia@email.com", role="user", phone="0844112233", status="active", membership="premium")
        user_amelia.set_password("user123")
        user_budi = User(username="Budi Santoso", email="budi@email.com", role="user", phone="0855112233", status="inactive", membership="free")
        user_budi.set_password("user123")
        user_siti = User(username="Siti Rahma", email="siti@email.com", role="user", phone="0866112233", status="active", membership="free")
        user_siti.set_password("user123")

        db.session.add_all([admin, user_rifki, user_dinda, user_rizky, user_amelia, user_budi, user_siti])
        db.session.commit()

        print("Seeding Templates...")
        # Main templates from images
        t1 = Template(
            subcategory_id=sub_cv_ats.id,
            name="CV ATS Friendly Professional",
            price=29000,
            description="Template CV ATS Friendly standar industri global. Sangat mudah dibaca oleh software recruiter (ATS) dan meningkatkan peluang wawancara kerja Anda.",
            file_format="DOCX, PDF",
            thumbnail_url="/static/uploads/thumbnails/cv_ats_friendly.png",
            file_url="/static/uploads/templates/cv_ats_friendly.docx",
            rating_avg=4.9,
            sales_count=1234,
            is_best_seller=True
        )

        t2 = Template(
            subcategory_id=sub_skripsi.id,
            name="Template Skripsi Minimalis",
            price=25000,
            description="Format skripsi lengkap dengan pengaturan bab, daftar isi otomatis, daftar gambar otomatis, serta layout halaman yang formal sesuai standar universitas.",
            file_format="DOCX, PDF, ZIP",
            thumbnail_url="/static/uploads/thumbnails/template_skripsi.png",
            file_url="/static/uploads/templates/skripsi.zip",
            rating_avg=4.8,
            sales_count=982,
            is_best_seller=True
        )

        t3 = Template(
            subcategory_id=sub_invoice.id,
            name="Invoice Profesional",
            price=15000,
            description="Template invoice modern dengan kalkulasi otomatis untuk bisnis, UMKM, dan freelancer. Desain minimalis dan bersih.",
            file_format="XLSX, PDF",
            thumbnail_url="/static/uploads/thumbnails/invoice_professional.png",
            file_url="/static/uploads/templates/invoice.xlsx",
            rating_avg=4.9,
            sales_count=874,
            is_best_seller=True
        )

        t4 = Template(
            subcategory_id=sub_portfolio.id,
            name="Portofolio UI/UX Designer",
            price=35000,
            description="Portofolio digital premium untuk memamerkan proyek UI/UX, studi kasus, mockup visual, serta riset pengguna dengan gaya modern.",
            file_format="FIGMA, ZIP",
            thumbnail_url="/static/uploads/thumbnails/portfolio_designer.png",
            file_url="/static/uploads/templates/portfolio_job.zip",
            rating_avg=4.9,
            sales_count=765,
            is_best_seller=True
        )

        t5 = Template(
            subcategory_id=sub_ppt.id,
            name="Template PPT Seminar",
            price=20000,
            description="Template slide presentasi yang memukau untuk seminar, proposal penelitian, sidang skripsi, atau kebutuhan akademik lainnya.",
            file_format="PPTX",
            thumbnail_url="/static/uploads/thumbnails/ppt_seminar.png",
            file_url="/static/uploads/templates/ppt_seminar.pptx",
            rating_avg=4.8,
            sales_count=642,
            is_best_seller=True
        )

        # Additional templates to populate categories
        t6 = Template(
            subcategory_id=sub_cv_kreatif.id,
            name="Creative CV Modern",
            price=25000,
            description="Template CV dengan desain kreatif, warna menarik, dan tata letak modern. Cocok untuk industri kreatif, agensi, dan media.",
            file_format="DOCX, PSD",
            thumbnail_url="/static/uploads/thumbnails/cv_ats_friendly.png", # reuse
            file_url="/static/uploads/templates/cv_creative.docx",
            rating_avg=4.7,
            sales_count=312,
            is_best_seller=False
        )

        t7 = Template(
            subcategory_id=sub_budget.id,
            name="Budget Planner Spreadsheet",
            price=19000,
            description="Lembar kerja Excel/Google Sheets untuk mengelola keuangan pribadi atau bisnis kecil secara rapi dan otomatis.",
            file_format="XLSX, PDF",
            thumbnail_url="/static/uploads/thumbnails/invoice_professional.png", # reuse
            file_url="/static/uploads/templates/budget_planner.xlsx",
            rating_avg=4.6,
            sales_count=198,
            is_best_seller=False
        )

        db.session.add_all([t1, t2, t3, t4, t5, t6, t7])
        db.session.commit()

        print("Seeding Transactions...")
        # Create some historical transactions
        # INV001 - Rifki bought CV ATS
        tx1 = Transaction(
            invoice_number="INV001",
            user_id=user_rifki.id,
            total_price=29000,
            payment_status="completed",
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        db.session.add(tx1)
        db.session.commit()
        
        td1 = TransactionDetail(transaction_id=tx1.id, template_id=t1.id, price=29000)
        db.session.add(td1)
        
        # INV002 - Rizky bought Skripsi Template
        tx2 = Transaction(
            invoice_number="INV002",
            user_id=user_rizky.id,
            total_price=25000,
            payment_status="completed",
            created_at=datetime.utcnow() - timedelta(days=1)
        )
        db.session.add(tx2)
        db.session.commit()
        
        td2 = TransactionDetail(transaction_id=tx2.id, template_id=t2.id, price=25000)
        db.session.add(td2)

        # INV003 - Amelia bought Invoice and PPT Seminar
        tx3 = Transaction(
            invoice_number="INV003",
            user_id=user_amelia.id,
            total_price=35000, # 15000 + 20000
            payment_status="pending",
            created_at=datetime.utcnow(),
            payment_proof="/static/uploads/payment_proofs/sample_proof.jpg"
        )
        db.session.add(tx3)
        db.session.commit()
        
        td3_1 = TransactionDetail(transaction_id=tx3.id, template_id=t3.id, price=15000)
        td3_2 = TransactionDetail(transaction_id=tx3.id, template_id=t5.id, price=20000)
        db.session.add_all([td3_1, td3_2])

        db.session.commit()

        print("Seeding Reviews...")
        rev1 = Review(user_id=user_rifki.id, template_id=t1.id, rating=5, comment="Sangat membantu! CV saya langsung lolos screening ATS.")
        rev2 = Review(user_id=user_rizky.id, template_id=t2.id, rating=4, comment="Struktur bab sangat rapi, dosen pembimbing langsung menyukai formatnya.")
        
        db.session.add_all([rev1, rev2])
        db.session.commit()

        print("Database Seeding Finished Successfully!")

if __name__ == "__main__":
    seed_data()
