"""
init_db.py - Inisialisasi database di production
Jalankan sekali setelah deploy: python init_db.py
"""
from app import app, db
from models import User, Category, SubCategory

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Semua tabel berhasil dibuat!")
        
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@templateverse.com',
                role='admin',
                status='active',
                membership='premium'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Akun admin berhasil dibuat! (admin / admin123)")
        else:
            print("ℹ️  Akun admin sudah ada, dilewati.")
        
        # Create default categories if empty
        if Category.query.count() == 0:
            categories_data = [
                {'name': 'Karier & Profesional', 'icon': 'fa-briefcase', 'subs': [
                    'CV / Resume', 'Surat Lamaran', 'Portfolio', 'Kartu Nama'
                ]},
                {'name': 'Pendidikan', 'icon': 'fa-graduation-cap', 'subs': [
                    'Skripsi / Thesis', 'Makalah', 'Presentasi Kelas', 'Laporan Praktikum'
                ]},
                {'name': 'Bisnis', 'icon': 'fa-chart-line', 'subs': [
                    'Invoice', 'Proposal Bisnis', 'Company Profile', 'Laporan Keuangan'
                ]},
                {'name': 'Desain', 'icon': 'fa-palette', 'subs': [
                    'Poster', 'Banner', 'Mockup', 'Social Media Kit'
                ]},
                {'name': 'Produktivitas', 'icon': 'fa-list-check', 'subs': [
                    'Planner', 'To-Do List', 'Jadwal Kegiatan', 'Notulen Rapat'
                ]},
            ]
            
            for cat_data in categories_data:
                cat = Category(name=cat_data['name'], icon=cat_data['icon'])
                db.session.add(cat)
                db.session.flush()  # Get the ID
                
                for sub_name in cat_data['subs']:
                    sub = SubCategory(category_id=cat.id, name=sub_name)
                    db.session.add(sub)
            
            db.session.commit()
            print(f"✅ {len(categories_data)} kategori default berhasil dibuat!")
        else:
            print("ℹ️  Kategori sudah ada, dilewati.")
        
        print("\n🚀 Database siap digunakan!")

if __name__ == '__main__':
    init_database()
