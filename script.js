// ==========================================
// TemplateVerse Static Hosting Script
// ==========================================

// Seed Data
const categories = [
    { id: 1, name: "Karier & Profesional", icon: "fa-briefcase" },
    { id: 2, name: "Pendidikan", icon: "fa-graduation-cap" },
    { id: 3, name: "Bisnis", icon: "fa-chart-line" },
    { id: 4, name: "Desain", icon: "fa-palette" },
    { id: 5, name: "Produktivitas", icon: "fa-check-double" }
];

const subcategories = {
    1: ["CV ATS Friendly", "CV Kreatif", "Resume Internasional", "Cover Letter", "Portofolio Kerja", "LinkedIn Profile"],
    2: ["Makalah", "Skripsi", "Proposal Penelitian", "PPT Seminar", "Laporan PKL", "Jurnal"],
    3: ["Invoice", "Proposal Bisnis", "Business Plan", "Surat Penawaran", "Laporan Keuangan"],
    4: ["Canva", "Poster", "Brosur", "Banner", "Feed Instagram"],
    5: ["Planner Harian", "To-Do List", "Budget Planner", "Habit Tracker", "Kalender Digital"]
};

// Initial Seed Templates
const initialTemplates = [
    {
        id: 1,
        categoryId: 1,
        subcategory: "CV ATS Friendly",
        name: "CV ATS Friendly Professional",
        price: 29000,
        description: "Template CV ATS Friendly standar industri global. Sangat mudah dibaca oleh software recruiter (ATS) dan meningkatkan peluang wawancara kerja Anda. Desain bersih, layout modular, dan dilengkapi petunjuk penulisan detail.",
        fileFormat: "DOCX, PDF",
        fileName: "cv_ats_friendly.docx",
        thumbnail: "assets/cv_ats_friendly.png",
        ratingAvg: 4.9,
        salesCount: 1234,
        isBestSeller: true
    },
    {
        id: 2,
        categoryId: 2,
        subcategory: "Skripsi",
        name: "Template Skripsi Minimalis",
        price: 25000,
        description: "Format skripsi lengkap dengan pengaturan bab, daftar isi otomatis, daftar gambar otomatis, serta layout halaman yang formal sesuai standar kebanyakan universitas di Indonesia.",
        fileFormat: "DOCX, PDF, ZIP",
        fileName: "skripsi.zip",
        thumbnail: "assets/template_skripsi.png",
        ratingAvg: 4.8,
        salesCount: 982,
        isBestSeller: true
    },
    {
        id: 3,
        categoryId: 3,
        subcategory: "Invoice",
        name: "Invoice Profesional",
        price: 15000,
        description: "Template invoice modern dengan kalkulasi otomatis untuk bisnis, UMKM, dan freelancer. Dilengkapi formula rumus PPN, diskon, dan total bersih otomatis di Excel.",
        fileFormat: "XLSX, PDF",
        fileName: "invoice.xlsx",
        thumbnail: "assets/invoice_professional.png",
        ratingAvg: 4.9,
        salesCount: 874,
        isBestSeller: true
    },
    {
        id: 4,
        categoryId: 4,
        subcategory: "Portofolio Kerja",
        name: "Portofolio UI/UX Designer",
        price: 35000,
        description: "Portofolio digital premium untuk memamerkan proyek UI/UX, studi kasus, mockup visual, serta riset pengguna dengan gaya modern dan profesional. Siap diimpor ke Figma.",
        fileFormat: "FIGMA, ZIP",
        fileName: "portfolio_job.zip",
        thumbnail: "assets/portfolio_designer.png",
        ratingAvg: 4.9,
        salesCount: 765,
        isBestSeller: true
    },
    {
        id: 5,
        categoryId: 2,
        subcategory: "PPT Seminar",
        name: "Template PPT Seminar",
        price: 20000,
        description: "Template slide presentasi yang memukau untuk seminar, proposal penelitian, sidang skripsi, atau kebutuhan akademik lainnya. Animasi transisi smooth dan mudah diubah warnanya.",
        fileFormat: "PPTX",
        fileName: "ppt_seminar.pptx",
        thumbnail: "assets/ppt_seminar.png",
        ratingAvg: 4.8,
        salesCount: 642,
        isBestSeller: true
    },
    {
        id: 6,
        categoryId: 1,
        subcategory: "CV Kreatif",
        name: "Creative CV Modern",
        price: 25000,
        description: "Template CV dengan desain kreatif, infografis menarik, dan tata letak modern. Sangat cocok untuk mendaftar di industri kreatif, startup agensi, dan media digital.",
        fileFormat: "DOCX, PSD",
        fileName: "cv_creative.docx",
        thumbnail: "assets/cv_ats_friendly.png", // Reused
        ratingAvg: 4.7,
        salesCount: 312,
        isBestSeller: false
    },
    {
        id: 7,
        categoryId: 5,
        subcategory: "Budget Planner",
        name: "Budget Planner Spreadsheet",
        price: 19000,
        description: "Lembar kerja Excel/Google Sheets untuk mengelola keuangan pribadi, pencatatan pemasukan, pengeluaran, tabungan, dan kalkulator investasi bulanan secara rapi.",
        fileFormat: "XLSX, PDF",
        fileName: "budget_planner.xlsx",
        thumbnail: "assets/invoice_professional.png", // Reused
        ratingAvg: 4.6,
        salesCount: 198,
        isBestSeller: false
    }
];

// Initial Reviews Seed
const initialReviews = [
    { templateId: 1, user: "Budi Santoso", rating: 5, comment: "Sangat membantu! Format CV-nya langsung terbaca di sistem ATS portal kerja. Sangat direkomendasikan.", date: "2026-06-15" },
    { templateId: 1, user: "Rizky Pratama", rating: 4, comment: "Bagus dan gampang diedit di MS Word. Keren!", date: "2026-06-20" },
    { templateId: 2, user: "Dinda Ayu", rating: 5, comment: "Format skripsi minimalis sangat membantu menghemat waktu penyusunan bab. Dosen pembimbing langsung ACC layoutnya.", date: "2026-06-25" },
    { templateId: 3, user: "Amelia Putri", rating: 5, comment: "Invoice bisnis dan laporan keuangan Excel sangat praktis. Dilengkapi fungsi rumus otomatis.", date: "2026-06-28" }
];

// State Initialization (LocalStorage checking)
let templates = JSON.parse(localStorage.getItem('tv_templates')) || initialTemplates;
let reviews = JSON.parse(localStorage.getItem('tv_reviews')) || initialReviews;
let wishlist = JSON.parse(localStorage.getItem('tv_wishlist')) || [];
let cart = JSON.parse(localStorage.getItem('tv_cart')) || [];
let ownedTemplates = JSON.parse(localStorage.getItem('tv_owned')) || [];
let activeUser = JSON.parse(localStorage.getItem('tv_user')) || {
    username: "Rifki",
    role: "user",
    membership: "free"
};

// Search and Filter State
let currentCategory = null;
let currentSubcategory = null;
let searchQuery = "";
let currentSort = "popular";

// Save State Helper
function saveState() {
    localStorage.setItem('tv_templates', JSON.stringify(templates));
    localStorage.setItem('tv_reviews', JSON.stringify(reviews));
    localStorage.setItem('tv_wishlist', JSON.stringify(wishlist));
    localStorage.setItem('tv_cart', JSON.stringify(cart));
    localStorage.setItem('tv_owned', JSON.stringify(ownedTemplates));
    localStorage.setItem('tv_user', JSON.stringify(activeUser));
}

// Format Currency
function formatRupiah(number) {
    return "Rp " + number.toLocaleString('id-ID');
}

// Document Ready
document.addEventListener("DOMContentLoaded", () => {
    initUI();
    renderCategories();
    renderTemplates();
    updateCartCount();
    updateWishlistCount();
    checkActiveUserNavbar();
});

// UI Event Listeners & Setup
function initUI() {
    // Search Bar Main Header Form
    const navbarSearchForm = document.getElementById("navbarSearchForm");
    if (navbarSearchForm) {
        navbarSearchForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const q = navbarSearchForm.querySelector("input").value;
            searchQuery = q;
            document.getElementById("heroSearchInput").value = q;
            renderTemplates();
            // Scroll to templates
            document.getElementById("templates-section").scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Hero Banner Search Form
    const heroSearchForm = document.getElementById("heroSearchForm");
    if (heroSearchForm) {
        heroSearchForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const q = document.getElementById("heroSearchInput").value;
            searchQuery = q;
            renderTemplates();
            document.getElementById("templates-section").scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Sort Dropdown Selector
    const sortSelector = document.getElementById("sortSelector");
    if (sortSelector) {
        sortSelector.addEventListener("change", (e) => {
            currentSort = e.target.value;
            renderTemplates();
        });
    }

    // Newsletter Button Submit
    const newsletterSubmit = document.getElementById("newsletterSubmit");
    if (newsletterSubmit) {
        newsletterSubmit.addEventListener("click", () => {
            const emailInput = document.querySelector(".newsletter-form input");
            if (emailInput && emailInput.value) {
                alert(`Terima kasih! Email ${emailInput.value} telah terdaftar untuk menerima update template terbaru.`);
                emailInput.value = "";
            } else {
                alert("Masukkan alamat email yang valid.");
            }
        });
    }
}

// Update Active User State in navbar UI
function checkActiveUserNavbar() {
    const userMenuContainer = document.getElementById("userMenuContainer");
    if (!userMenuContainer) return;

    if (activeUser) {
        let adminItem = "";
        let dashboardPath = "#";
        if (activeUser.role === 'admin') {
            adminItem = `<li><a class="dropdown-item py-2" href="#" onclick="alert('Admin Dashboard Simulator Open')"><i class="fa-solid fa-gauge me-2 text-primary"></i> Admin Dashboard</a></li>`;
        }

        userMenuContainer.innerHTML = `
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle d-flex align-items-center gap-2" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <img src="assets/default-profile.png" alt="avatar" class="rounded-circle" style="width: 32px; height: 32px; object-fit: cover; border: 1.5px solid var(--primary);">
                    <span>${activeUser.username} <span class="badge ${activeUser.membership === 'premium' ? 'bg-warning text-dark' : 'bg-secondary'}" style="font-size:9px;">${activeUser.membership.toUpperCase()}</span></span>
                </a>
                <ul class="dropdown-menu dropdown-menu-end border-0 shadow-sm mt-2">
                    ${adminItem}
                    <li><a class="dropdown-item py-2" href="#" onclick="openUserDashboardModal()"><i class="fa-solid fa-user me-2 text-primary"></i> Dashboard Saya</a></li>
                    <li><a class="dropdown-item py-2" href="#" onclick="toggleMembership()"><i class="fa-solid fa-star me-2 text-warning"></i> Ubah Membership</a></li>
                    <li><a class="dropdown-item py-2" href="#" onclick="openOwnedModal()"><i class="fa-solid fa-download me-2 text-primary"></i> Template Saya</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item py-2 text-danger" href="#" onclick="simulateLogout()"><i class="fa-solid fa-right-from-bracket me-2"></i> Logout</a></li>
                </ul>
            </li>
        `;
    } else {
        userMenuContainer.innerHTML = `
            <li class="nav-item ms-lg-2">
                <a class="btn btn-link nav-link text-decoration-none px-3" href="#" onclick="simulateLogin()">Login</a>
            </li>
            <li class="nav-item">
                <a class="btn btn-primary-grad px-4" href="#" onclick="simulateRegister()">Register</a>
            </li>
        `;
    }
}

// Simulate Login
function simulateLogin() {
    activeUser = {
        username: "Rifki",
        role: "user",
        membership: "free"
    };
    saveState();
    checkActiveUserNavbar();
    alert("Berhasil masuk sebagai Rifki! Status Membership: FREE.");
    location.reload();
}

// Simulate Logout
function simulateLogout() {
    activeUser = null;
    saveState();
    checkActiveUserNavbar();
    alert("Berhasil keluar dari akun.");
    location.reload();
}

// Simulate Register
function simulateRegister() {
    activeUser = {
        username: "NewUser",
        role: "user",
        membership: "free"
    };
    saveState();
    checkActiveUserNavbar();
    alert("Registrasi berhasil! Anda telah masuk otomatis.");
}

// Toggle Premium Membership State
function toggleMembership() {
    if (!activeUser) {
        alert("Silakan Login terlebih dahulu untuk berlangganan.");
        return;
    }
    if (activeUser.membership === 'free') {
        activeUser.membership = 'premium';
        alert("Selamat! Anda sekarang menjadi Premium Member TemplateVerse. Akses semua template gratis!");
    } else {
        activeUser.membership = 'free';
        alert("Membership Anda dikembalikan ke paket FREE.");
    }
    saveState();
    checkActiveUserNavbar();
    renderTemplates();
}

// Render Category List & Dropdowns
function renderCategories() {
    // Render dropdown categories inside Header navbar
    const headerCategoryMenu = document.getElementById("headerCategoryMenu");
    if (headerCategoryMenu) {
        headerCategoryMenu.innerHTML = categories.map(cat => `
            <li><a class="dropdown-item py-2" href="#templates-section" onclick="filterByCategory(${cat.id})"><i class="fa-solid ${cat.icon} text-primary me-2"></i> ${cat.name}</a></li>
        `).join('') + `<li><hr class="dropdown-divider"></li><li><a class="dropdown-item py-2" href="#" onclick="filterByCategory(null)">Lihat Semua Kategori</a></li>`;
    }

    // Render chips category list under Hero section
    const categoryChipsList = document.getElementById("categoryChipsList");
    if (categoryChipsList) {
        categoryChipsList.innerHTML = categories.map(cat => `
            <a href="#templates-section" onclick="filterByCategory(${cat.id})" class="cat-chip ${currentCategory === cat.id ? 'active' : ''}">
                <div class="cat-chip-icon">
                    <i class="fa-solid ${cat.icon}"></i>
                </div>
                <span>${cat.name}</span>
            </a>
        `).join('') + `
            <a href="#templates-section" onclick="filterByCategory(null)" class="cat-chip ${currentCategory === null ? 'active' : ''}">
                <div class="cat-chip-icon">
                    <i class="fa-solid fa-ellipsis"></i>
                </div>
                <span>Semua</span>
            </a>
        `;
    }

    // Render left sidebar Category links
    const sidebarCategoryLinks = document.getElementById("sidebarCategoryLinks");
    if (sidebarCategoryLinks) {
        sidebarCategoryLinks.innerHTML = `
            <a href="#" onclick="filterByCategory(null)" class="sidebar-nav-item ${currentCategory === null ? 'active' : ''}">
                <i class="fa-solid fa-house"></i> Beranda
            </a>
        ` + categories.map(cat => `
            <a href="#templates-section" onclick="filterByCategory(${cat.id})" class="sidebar-nav-item ${currentCategory === cat.id ? 'active' : ''}">
                <i class="fa-solid ${cat.icon}"></i> ${cat.name}
            </a>
        `).join('');
    }
}

// Filter Actions
function filterByCategory(categoryId) {
    currentCategory = categoryId;
    currentSubcategory = null; // Reset subcategory when category changes
    renderCategories();
    renderTemplates();
    
    // Update active category info on sidebar/filters card
    renderFilterSidebar();
}

function filterBySubcategory(subcatName) {
    currentSubcategory = subcatName;
    renderTemplates();
    renderFilterSidebar();
}

// Render dynamic subcategory filter card when category is selected
function renderFilterSidebar() {
    const filterCardContainer = document.getElementById("filterCardContainer");
    if (!filterCardContainer) return;

    if (currentCategory || searchQuery) {
        let subcatHtml = "";
        let catName = "Pencarian";
        let catIcon = "fa-sliders";

        if (currentCategory) {
            const catObj = categories.find(c => c.id === currentCategory);
            catName = catObj.name;
            catIcon = catObj.icon;
            const subcats = subcategories[currentCategory] || [];

            subcatHtml = `
                <div class="mb-4">
                    <div class="text-muted fw-bold text-uppercase mb-2" style="font-size:10.5px; letter-spacing:1px;">Subkategori</div>
                    <div class="d-flex flex-column gap-1" style="font-size:13.5px;">
                        <a href="#templates-section" onclick="filterBySubcategory(null)"
                           class="d-flex justify-content-between align-items-center px-3 py-2 rounded-3 text-decoration-none ${currentSubcategory === null ? 'fw-bold bg-primary-light text-primary' : 'text-secondary'}"
                           style="color: ${currentSubcategory === null ? 'var(--primary)' : 'var(--gray-600)'};">
                            <span>Semua Subkategori</span>
                        </a>
                        ${subcats.map(sub => {
                            const count = templates.filter(t => t.categoryId === currentCategory && t.subcategory === sub).length;
                            return `
                                <a href="#templates-section" onclick="filterBySubcategory('${sub}')"
                                   class="d-flex justify-content-between align-items-center px-3 py-2 rounded-3 text-decoration-none ${currentSubcategory === sub ? 'fw-bold bg-primary-light text-primary' : 'text-secondary'}"
                                   style="color: ${currentSubcategory === sub ? 'var(--primary)' : 'var(--gray-600)'};">
                                    <span>${sub}</span>
                                    <span class="badge rounded-pill bg-light text-secondary border" style="font-size:11px;">${count}</span>
                                </a>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        }

        filterCardContainer.innerHTML = `
            <div class="filter-card">
                <div class="filter-title">
                    <i class="fa-solid ${catIcon}"></i> ${currentCategory ? 'Filter Kategori' : 'Filter Pencarian'}
                </div>
                ${currentCategory ? `
                <div class="mb-4">
                    <div class="text-muted fw-bold text-uppercase mb-2" style="font-size:10px; letter-spacing:1px;">Kategori Terpilih</div>
                    <div class="d-flex justify-content-between align-items-center bg-light rounded-3 p-2 px-3" style="font-size:13.5px;">
                        <span><i class="fa-solid ${catIcon} text-primary me-2"></i>${catName}</span>
                        <a href="#" onclick="filterByCategory(null)" class="text-danger text-decoration-none" title="Hapus">
                            <i class="fa-solid fa-circle-xmark"></i>
                        </a>
                    </div>
                </div>
                ` : ''}
                
                ${subcatHtml}

                <div>
                    <div class="text-muted fw-bold text-uppercase mb-2" style="font-size:10px; letter-spacing:1px;">Tipe Pembelian</div>
                    <div class="form-check mb-2">
                        <input class="form-check-input" type="checkbox" value="" id="buyFree" checked disabled>
                        <label class="form-check-label small" for="buyFree">Sekali Beli (Selamanya)</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="buyPremium" checked disabled>
                        <label class="form-check-label small" for="buyPremium">Akses Premium Membership</label>
                    </div>
                </div>
            </div>
        `;
        document.getElementById("filterSidebarCol").style.display = "block";
        document.getElementById("templatesListCol").className = "col-lg-9";
    } else {
        filterCardContainer.innerHTML = "";
        document.getElementById("filterSidebarCol").style.display = "none";
        document.getElementById("templatesListCol").className = "col-12";
    }
}

// Render Templates List
function renderTemplates() {
    const templatesGrid = document.getElementById("templatesGrid");
    if (!templatesGrid) return;

    // Filter Logic
    let filtered = [...templates];

    if (currentCategory !== null) {
        filtered = filtered.filter(t => t.categoryId === currentCategory);
    }
    if (currentSubcategory !== null) {
        filtered = filtered.filter(t => t.subcategory === currentSubcategory);
    }
    if (searchQuery.trim() !== "") {
        const q = searchQuery.toLowerCase().trim();
        filtered = filtered.filter(t => t.name.toLowerCase().includes(q) || t.description.toLowerCase().includes(q) || t.subcategory.toLowerCase().includes(q));
    }

    // Sort Logic
    if (currentSort === "popular") {
        filtered.sort((a, b) => b.salesCount - a.salesCount);
    } else if (currentSort === "price-asc") {
        filtered.sort((a, b) => a.price - b.price);
    } else if (currentSort === "price-desc") {
        filtered.sort((a, b) => b.price - a.price);
    } else if (currentSort === "rating") {
        filtered.sort((a, b) => b.ratingAvg - a.ratingAvg);
    }

    // Update section titles dynamically
    const sectionTitleText = document.getElementById("sectionTitleText");
    if (sectionTitleText) {
        if (currentCategory) {
            const cat = categories.find(c => c.id === currentCategory);
            sectionTitleText.innerHTML = `<i class="fa-solid ${cat.icon} me-2" style="color:var(--primary);"></i> ${cat.name}`;
        } else if (searchQuery) {
            sectionTitleText.innerHTML = `Hasil Pencarian: "${searchQuery}"`;
        } else {
            sectionTitleText.innerHTML = "Semua Template Terlaris";
        }
    }

    const templateResultCount = document.getElementById("templateResultCount");
    if (templateResultCount) {
        templateResultCount.innerText = `Menampilkan ${filtered.length} template berkualitas tinggi`;
    }

    if (filtered.length === 0) {
        templatesGrid.innerHTML = `
            <div class="col-12">
                <div class="tv-empty-state">
                    <i class="fa-solid fa-face-frown display-4"></i>
                    <h4 class="mt-3">Template Tidak Ditemukan</h4>
                    <p class="text-muted">Maaf, kami tidak dapat menemukan template yang cocok dengan kriteria pencarian Anda.</p>
                    <button class="btn btn-primary-grad mt-3" onclick="resetFilters()">Tampilkan Semua</button>
                </div>
            </div>
        `;
        return;
    }

    // Build Cards HTML
    templatesGrid.innerHTML = filtered.map(t => {
        const isBestsellerBadge = t.isBestSeller ? `<span class="tv-badge-bestseller"><i class="fa-solid fa-star me-1"></i>Best Seller</span>` : '';
        const inWishlist = wishlist.includes(t.id);
        const owned = ownedTemplates.includes(t.id) || (activeUser && activeUser.membership === 'premium');

        return `
            <div class="col-sm-6 col-md-6 ${currentCategory || searchQuery ? 'col-lg-4' : 'col-lg-3'}">
                <div class="tv-template-card">
                    <div class="tv-template-img-wrap">
                        <img src="${t.thumbnail}" alt="${t.name}">
                        ${isBestsellerBadge}
                        <button class="tv-wishlist-btn ${inWishlist ? 'active' : ''}" onclick="toggleWishlist(${t.id})" title="Wishlist">
                            <i class="${inWishlist ? 'fa-solid' : 'fa-regular'} fa-heart"></i>
                        </button>
                    </div>
                    <div class="tv-card-body">
                        <div class="tv-card-subcat">${t.subcategory}</div>
                        <a href="#" onclick="openDetailModal(${t.id}); return false;" class="tv-card-title">${t.name}</a>
                        <div class="tv-card-rating">
                            <span class="tv-stars">
                                ${renderStarRating(t.ratingAvg)}
                            </span>
                            <span>${t.ratingAvg} (${t.salesCount} Terjual)</span>
                        </div>
                        <div class="tv-card-footer">
                            <div class="tv-price">${t.price === 0 ? 'Gratis' : formatRupiah(t.price)}</div>
                            <div class="tv-card-actions">
                                <button class="tv-btn-cart" onclick="addToCart(${t.id})" title="Tambah ke Keranjang">
                                    <i class="fa-solid fa-cart-plus"></i>
                                </button>
                                <button class="tv-btn-detail" onclick="openDetailModal(${t.id})">Detail</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    renderFilterSidebar();
}

// Render Star Icons from floating ratings value
function renderStarRating(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating - fullStars >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;
    
    let html = "";
    for (let i = 0; i < fullStars; i++) {
        html += '<i class="fa-solid fa-star"></i>';
    }
    if (halfStar) {
        html += '<i class="fa-solid fa-star-half-stroke"></i>';
    }
    for (let i = 0; i < emptyStars; i++) {
        html += '<i class="fa-regular fa-star"></i>';
    }
    return html;
}

// Reset Filter state
function resetFilters() {
    currentCategory = null;
    currentSubcategory = null;
    searchQuery = "";
    document.getElementById("heroSearchInput").value = "";
    const navInput = document.querySelector("#navbarSearchForm input");
    if (navInput) navInput.value = "";
    renderCategories();
    renderTemplates();
}

// Cart Management
function addToCart(templateId) {
    if (!activeUser) {
        alert("Silakan login terlebih dahulu untuk menambah barang ke keranjang.");
        return;
    }

    if (ownedTemplates.includes(templateId)) {
        alert("Anda sudah memiliki template ini.");
        return;
    }

    if (cart.includes(templateId)) {
        alert("Template sudah ada di keranjang Anda.");
        return;
    }

    // Free membership check
    if (activeUser.membership === 'premium') {
        alert("Anda memiliki Premium Membership. Semua template bisa langsung didownload secara gratis!");
        openDetailModal(templateId);
        return;
    }

    cart.push(templateId);
    saveState();
    updateCartCount();
    alert("Template berhasil ditambahkan ke keranjang belanja!");
}

function removeFromCart(templateId) {
    cart = cart.filter(id => id !== templateId);
    saveState();
    updateCartCount();
    openCartModal(); // Refresh cart modal if open
}

function updateCartCount() {
    const badge = document.getElementById("cartCountBadge");
    if (badge) {
        badge.innerText = cart.length;
        badge.style.display = cart.length > 0 ? "inline-block" : "none";
    }
}

// Wishlist Management
function toggleWishlist(templateId) {
    if (!activeUser) {
        alert("Silakan login terlebih dahulu untuk menyimpan wishlist.");
        return;
    }

    const idx = wishlist.indexOf(templateId);
    if (idx > -1) {
        wishlist.splice(idx, 1);
        alert("Dihapus dari Wishlist!");
    } else {
        wishlist.push(templateId);
        alert("Ditambahkan ke Wishlist!");
    }
    saveState();
    updateWishlistCount();
    renderTemplates();
}

function updateWishlistCount() {
    const badge = document.getElementById("wishlistCountBadge");
    if (badge) {
        badge.innerText = wishlist.length;
        badge.style.display = wishlist.length > 0 ? "inline-block" : "none";
    }
}

// Modal View: Product Detail
let activeModalTemplateId = null;
function openDetailModal(templateId) {
    const t = templates.find(temp => temp.id === templateId);
    if (!t) return;
    activeModalTemplateId = templateId;

    const modalTitle = document.getElementById("detailModalTitle");
    const modalBody = document.getElementById("detailModalBody");

    if (!modalTitle || !modalBody) return;

    modalTitle.innerText = t.name;

    // Filter reviews for this template
    const tReviews = reviews.filter(r => r.templateId === templateId);
    
    // Check if owned/accessible
    const isOwned = ownedTemplates.includes(t.id);
    const hasPremiumAccess = activeUser && activeUser.membership === 'premium';
    const canDownload = isOwned || hasPremiumAccess;

    let actionsHtml = "";
    if (canDownload) {
        actionsHtml = `
            <div class="alert alert-success d-flex justify-content-between align-items-center" style="border-radius:12px;">
                <span><i class="fa-solid fa-circle-check text-success me-2"></i> ${hasPremiumAccess ? 'Akses Premium Aktif' : 'Anda telah membeli template ini.'}</span>
                <button class="btn btn-success fw-bold" onclick="simulateDownload(${t.id})"><i class="fa-solid fa-download me-2"></i> Download (${t.fileFormat})</button>
            </div>
        `;
    } else {
        actionsHtml = `
            <div class="d-flex align-items-center justify-content-between bg-light p-3 rounded-4 border">
                <div>
                    <div class="text-muted small">Harga Sekali Beli</div>
                    <div class="fw-extrabold fs-4 text-dark">${formatRupiah(t.price)}</div>
                </div>
                <div class="d-flex gap-2">
                    <button class="btn btn-outline-primary fw-bold" onclick="toggleWishlist(${t.id})"><i class="fa-regular fa-heart me-2"></i> Favorit</button>
                    <button class="btn btn-primary-grad fw-bold" onclick="addToCart(${t.id}); bootstrap.Modal.getInstance(document.getElementById('detailModal')).hide();"><i class="fa-solid fa-cart-plus me-2"></i> Beli Sekarang</button>
                </div>
            </div>
        `;
    }

    modalBody.innerHTML = `
        <div class="row g-4">
            <div class="col-md-5">
                <img src="${t.thumbnail}" class="img-fluid rounded-4 border w-100 shadow-sm" alt="${t.name}">
                <div class="mt-3 p-3 bg-light rounded-3 text-secondary" style="font-size:13.5px;">
                    <div><i class="fa-solid fa-folder me-2"></i> Kategori: <strong>${categories.find(c => c.id === t.categoryId).name}</strong></div>
                    <div class="mt-2"><i class="fa-solid fa-tag me-2"></i> Subkategori: <strong>${t.subcategory}</strong></div>
                    <div class="mt-2"><i class="fa-solid fa-file-code me-2"></i> Format File: <strong>${t.fileFormat}</strong></div>
                    <div class="mt-2"><i class="fa-solid fa-cart-shopping me-2"></i> Jumlah Unduh: <strong>${t.salesCount}x Terjual</strong></div>
                </div>
            </div>
            <div class="col-md-7 d-flex flex-column justify-content-between">
                <div>
                    <h4 class="fw-bold text-dark">${t.name}</h4>
                    <div class="d-flex align-items-center gap-2 my-2">
                        <span class="tv-stars fs-6">${renderStarRating(t.ratingAvg)}</span>
                        <strong class="text-dark">${t.ratingAvg}</strong>
                        <span class="text-muted">(${tReviews.length} Ulasan)</span>
                    </div>
                    <p class="text-secondary mt-3" style="font-size:14.5px; line-height:1.7;">${t.description}</p>
                </div>
                
                <div class="mt-4">
                    ${actionsHtml}
                </div>
            </div>
        </div>

        <hr class="my-4">

        <div class="row">
            <div class="col-12">
                <h5 class="fw-bold mb-3"><i class="fa-regular fa-comment-dots text-primary me-2"></i>Ulasan Pelanggan</h5>
                
                <!-- Review List -->
                <div class="d-flex flex-column gap-3 mb-4" id="modalReviewsList">
                    ${tReviews.length === 0 ? '<p class="text-muted small italic">Belum ada ulasan untuk template ini.</p>' : tReviews.map(r => `
                        <div class="border-bottom pb-3">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="fw-bold text-dark" style="font-size:14px;">${r.user}</div>
                                <span class="text-muted small" style="font-size:11px;">${r.date}</span>
                            </div>
                            <div class="tv-stars my-1" style="font-size:11px;">${renderStarRating(r.rating)}</div>
                            <p class="m-0 text-secondary" style="font-size:13.5px;">"${r.comment}"</p>
                        </div>
                    `).join('')}
                </div>

                <!-- Add Review Form -->
                ${activeUser ? `
                    <div class="bg-light p-3 rounded-4 border">
                        <h6 class="fw-bold mb-2">Tulis Ulasan Anda</h6>
                        <form id="submitReviewForm" onsubmit="submitReview(event)">
                            <div class="mb-2">
                                <label class="form-label small text-muted mb-1">Rating</label>
                                <select class="form-select form-select-sm w-auto" id="reviewRating" required>
                                    <option value="5">⭐⭐⭐⭐⭐ (5 - Sangat Puas)</option>
                                    <option value="4">⭐⭐⭐⭐ (4 - Puas)</option>
                                    <option value="3">⭐⭐⭐ (3 - Cukup)</option>
                                    <option value="2">⭐⭐ (2 - Kurang Puas)</option>
                                    <option value="1">⭐ (1 - Buruk)</option>
                                </select>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small text-muted mb-1">Komentar</label>
                                <textarea class="form-control form-control-sm" rows="3" id="reviewComment" placeholder="Berikan pendapat Anda mengenai template ini..." required></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary btn-sm fw-bold">Kirim Ulasan</button>
                        </form>
                    </div>
                ` : '<p class="text-muted small italic text-center">Silakan login untuk mengirimkan ulasan.</p>'}
            </div>
        </div>
    `;

    // Trigger Bootstrap Modal
    const myModal = new bootstrap.Modal(document.getElementById('detailModal'));
    myModal.show();
}

// Download Simulator Action
function simulateDownload(templateId) {
    const t = templates.find(temp => temp.id === templateId);
    if (!t) return;
    alert(`Mendownload file: ${t.fileName} (${t.fileFormat}).\nTerima kasih telah menggunakan TemplateVerse!`);
}

// Review Submission Handler
function submitReview(e) {
    e.preventDefault();
    if (!activeUser || !activeModalTemplateId) return;

    const ratingVal = parseInt(document.getElementById("reviewRating").value);
    const commentVal = document.getElementById("reviewComment").value;

    const newReview = {
        templateId: activeModalTemplateId,
        user: activeUser.username,
        rating: ratingVal,
        comment: commentVal,
        date: new Date().toISOString().split('T')[0]
    };

    reviews.push(newReview);

    // Recalculate average rating of active template
    const tReviews = reviews.filter(r => r.templateId === activeModalTemplateId);
    const sum = tReviews.reduce((acc, curr) => acc + curr.rating, 0);
    const avg = parseFloat((sum / tReviews.length).toFixed(1));

    const tIdx = templates.findIndex(temp => temp.id === activeModalTemplateId);
    if (tIdx > -1) {
        templates[tIdx].ratingAvg = avg;
    }

    saveState();
    alert("Ulasan Anda berhasil dikirim!");
    
    // Refresh modal UI
    openDetailModal(activeModalTemplateId);
    renderTemplates();
}

// Cart Modal View & Checkout simulation
function openCartModal() {
    const modalBody = document.getElementById("cartModalBody");
    if (!modalBody) return;

    if (!activeUser) {
        alert("Silakan login terlebih dahulu.");
        return;
    }

    if (cart.length === 0) {
        modalBody.innerHTML = `
            <div class="text-center py-5">
                <i class="fa-solid fa-cart-shopping display-1 text-muted opacity-25"></i>
                <h5 class="mt-3">Keranjang Belanja Kosong</h5>
                <p class="text-muted small">Cari template menarik kami dan tambahkan ke keranjang.</p>
                <button class="btn btn-primary-grad mt-2" data-bs-dismiss="modal">Mulai Berbelanja</button>
            </div>
        `;
        document.getElementById("cartModalFooter").style.display = "none";
    } else {
        let total = 0;
        let cartItemsHtml = cart.map(itemId => {
            const t = templates.find(temp => temp.id === itemId);
            if (!t) return "";
            total += t.price;
            return `
                <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-3">
                    <div class="d-flex align-items-center gap-3">
                        <img src="${t.thumbnail}" class="rounded-3 border" style="width: 60px; height: 45px; object-fit: cover;">
                        <div>
                            <h6 class="m-0 fw-bold text-dark">${t.name}</h6>
                            <span class="text-primary fw-bold" style="font-size:13px;">${formatRupiah(t.price)}</span>
                        </div>
                    </div>
                    <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart(${t.id})" title="Hapus"><i class="fa-solid fa-trash"></i></button>
                </div>
            `;
        }).join('');

        modalBody.innerHTML = `
            <div class="d-flex flex-column gap-1">
                ${cartItemsHtml}
            </div>
            <div class="d-flex justify-content-between align-items-center bg-light p-3 rounded-4 border mt-3">
                <span class="fw-bold text-secondary">Total Belanja</span>
                <span class="fw-extrabold fs-5 text-primary" id="cartTotalSum">${formatRupiah(total)}</span>
            </div>
        `;

        const checkoutBtn = document.getElementById("checkoutBtn");
        if (checkoutBtn) {
            checkoutBtn.onclick = () => simulateCheckout(total);
        }
        document.getElementById("cartModalFooter").style.display = "flex";
    }

    const myModal = new bootstrap.Modal(document.getElementById('cartModal'));
    myModal.show();
}

// Checkout simulation
function simulateCheckout(totalAmount) {
    if (cart.length === 0) return;

    const confirmed = confirm(`Konfirmasi Pembelian:\nTotal tagihan: ${formatRupiah(totalAmount)}\n\nSistem akan mensimulasikan pembayaran instan otomatis. Lanjutkan?`);
    
    if (confirmed) {
        // Move cart items to owned
        cart.forEach(itemId => {
            if (!ownedTemplates.includes(itemId)) {
                ownedTemplates.push(itemId);
            }
        });
        cart = []; // clear cart
        saveState();
        updateCartCount();
        
        // Hide cart modal
        const cartModalEl = document.getElementById('cartModal');
        const modalInstance = bootstrap.Modal.getInstance(cartModalEl);
        if (modalInstance) modalInstance.hide();

        alert("Pembayaran Berhasil!\nTemplate telah ditambahkan ke dashboard koleksi Anda. Silakan unduh langsung.");
        openOwnedModal();
        renderTemplates();
    }
}

// Owned Templates Modal View
function openOwnedModal() {
    const modalBody = document.getElementById("ownedModalBody");
    if (!modalBody) return;

    if (!activeUser) {
        alert("Silakan login terlebih dahulu.");
        return;
    }

    const premiumUser = activeUser.membership === 'premium';
    const list = premiumUser ? templates : templates.filter(t => ownedTemplates.includes(t.id));

    if (list.length === 0) {
        modalBody.innerHTML = `
            <div class="text-center py-5">
                <i class="fa-solid fa-folder-open display-1 text-muted opacity-25"></i>
                <h5 class="mt-3">Belum Ada Template</h5>
                <p class="text-muted small">Anda belum membeli template apapun. Beli template atau upgrade ke Premium Membership.</p>
                <button class="btn btn-primary-grad mt-2" data-bs-dismiss="modal">Cari Template</button>
            </div>
        `;
    } else {
        modalBody.innerHTML = `
            ${premiumUser ? `
                <div class="alert alert-warning mb-4" style="border-radius:12px; font-size:13.5px;">
                    <i class="fa-solid fa-star text-warning me-2"></i> Status Premium Aktif: <strong>Semua template premium bebas Anda download!</strong>
                </div>
            ` : ''}
            <div class="d-flex flex-column gap-3">
                ${list.map(t => `
                    <div class="d-flex justify-content-between align-items-center border-bottom pb-3">
                        <div class="d-flex align-items-center gap-3">
                            <img src="${t.thumbnail}" class="rounded-3 border" style="width: 70px; height: 50px; object-fit: cover;">
                            <div>
                                <h6 class="m-0 fw-bold text-dark">${t.name}</h6>
                                <span class="text-secondary small" style="font-size:12px;">Format: ${t.fileFormat}</span>
                            </div>
                        </div>
                        <button class="btn btn-sm btn-success fw-bold px-3" onclick="simulateDownload(${t.id})"><i class="fa-solid fa-download me-1"></i> Unduh</button>
                    </div>
                `).join('')}
            </div>
        `;
    }

    const myModal = new bootstrap.Modal(document.getElementById('ownedModal'));
    myModal.show();
}

// User Dashboard Info modal
function openUserDashboardModal() {
    const modalBody = document.getElementById("userDashboardModalBody");
    if (!modalBody) return;

    if (!activeUser) {
        alert("Silakan login terlebih dahulu.");
        return;
    }

    const list = templates.filter(t => ownedTemplates.includes(t.id));
    const wishlistItems = templates.filter(t => wishlist.includes(t.id));

    modalBody.innerHTML = `
        <div class="d-flex flex-column align-items-center text-center pb-4 border-bottom">
            <img src="assets/default-profile.png" alt="Profile" class="rounded-circle border" style="width: 80px; height: 80px; object-fit: cover;">
            <h5 class="fw-bold mt-3 mb-1 text-dark">${activeUser.username}</h5>
            <p class="text-muted mb-2" style="font-size:13px;">Role: User | Status Akun: Aktif</p>
            <span class="badge ${activeUser.membership === 'premium' ? 'bg-warning text-dark' : 'bg-secondary'} fs-7 px-3 py-2" style="border-radius:20px;">
                <i class="fa-solid ${activeUser.membership === 'premium' ? 'fa-star' : 'fa-user'} me-1"></i> Membership: ${activeUser.membership.toUpperCase()}
            </span>
        </div>

        <div class="row text-center mt-4 g-3">
            <div class="col-4">
                <div class="bg-light p-3 rounded-4 border">
                    <div class="fw-extrabold fs-4 text-primary">${list.length}</div>
                    <div class="text-muted small" style="font-size:11.5px;">Beli</div>
                </div>
            </div>
            <div class="col-4">
                <div class="bg-light p-3 rounded-4 border">
                    <div class="fw-extrabold fs-4 text-danger">${wishlistItems.length}</div>
                    <div class="text-muted small" style="font-size:11.5px;">Favorit</div>
                </div>
            </div>
            <div class="col-4">
                <div class="bg-light p-3 rounded-4 border">
                    <div class="fw-extrabold fs-4 text-success">${activeUser.membership === 'premium' ? 'Akses Pro' : 'Free'}</div>
                    <div class="text-muted small" style="font-size:11.5px;">Tipe</div>
                </div>
            </div>
        </div>

        <div class="mt-4">
            <h6 class="fw-bold mb-3"><i class="fa-regular fa-star me-2 text-warning"></i>Koleksi Favorit Saya (${wishlistItems.length})</h6>
            ${wishlistItems.length === 0 ? '<p class="text-muted italic small text-center">Belum ada item favorit.</p>' : `
                <div class="d-flex flex-column gap-2" style="max-height: 200px; overflow-y: auto;">
                    ${wishlistItems.map(t => `
                        <div class="d-flex justify-content-between align-items-center bg-light p-2 rounded-3 border-0" style="font-size:13.5px;">
                            <span class="text-dark fw-bold text-truncate me-2">${t.name}</span>
                            <button class="btn btn-sm btn-link text-primary p-0 fw-bold" onclick="bootstrap.Modal.getInstance(document.getElementById('userDashboardModal')).hide(); openDetailModal(${t.id});">Detail</button>
                        </div>
                    `).join('')}
                </div>
            `}
        </div>
    `;

    const myModal = new bootstrap.Modal(document.getElementById('userDashboardModal'));
    myModal.show();
}
