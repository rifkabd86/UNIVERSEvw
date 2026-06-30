import os
import shutil

# Paths
brain_dir = r"C:\Users\rifka\.gemini\antigravity-ide\brain\aa4d7e8c-bc72-4ad6-be2d-dcb748947868"
workspace_dir = r"c:\xampp\htdocs\TemplateVerse"

dest_thumb_dir = os.path.join(workspace_dir, "static", "uploads", "thumbnails")
dest_temp_dir = os.path.join(workspace_dir, "static", "uploads", "templates")
dest_proof_dir = os.path.join(workspace_dir, "static", "uploads", "payment_proofs")
dest_img_dir = os.path.join(workspace_dir, "static", "images")

# Ensure directories exist
os.makedirs(dest_thumb_dir, exist_ok=True)
os.makedirs(dest_temp_dir, exist_ok=True)
os.makedirs(dest_proof_dir, exist_ok=True)
os.makedirs(dest_img_dir, exist_ok=True)

# List of generated files to copy
generated_files = {
    "cv_ats_friendly_1781007690070.png": "cv_ats_friendly.png",
    "template_skripsi_1781007716850.png": "template_skripsi.png",
    "invoice_professional_1781007736250.png": "invoice_professional.png",
    "portfolio_designer_1781007797239.png": "portfolio_designer.png",
    "ppt_seminar_1781007838307.png": "ppt_seminar.png"
}

print("Copying generated thumbnails...")
for src_name, dest_name in generated_files.items():
    src_path = os.path.join(brain_dir, src_name)
    dest_path = os.path.join(dest_thumb_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"Copied {src_name} -> {dest_name}")
    else:
        print(f"Warning: {src_path} not found!")

# Create dummy template files to download
print("Creating dummy template files for downloads...")
dummy_files = [
    "cv_ats_friendly.docx",
    "cv_creative.docx",
    "resume_international.docx",
    "cover_letter.docx",
    "portfolio_job.zip",
    "linkedin_profile.pdf",
    "makalah.docx",
    "skripsi.zip",
    "proposal_penelitian.docx",
    "ppt_seminar.pptx",
    "laporan_pkl.pdf",
    "jurnal.pdf",
    "invoice.xlsx",
    "proposal_bisnis.docx",
    "business_plan.pdf",
    "surat_penawaran.docx",
    "laporan_keuangan.xlsx",
    "canva_link.txt",
    "poster.psd",
    "brosur.ai",
    "banner.psd",
    "instagram_feed.zip",
    "planner_harian.pdf",
    "todo_list.pdf",
    "budget_planner.xlsx",
    "habit_tracker.pdf",
    "kalender_digital.pdf"
]

for file_name in dummy_files:
    file_path = os.path.join(dest_temp_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"This is a premium template download for '{file_name}' from TemplateVerse. Thank you for your purchase!")
    print(f"Created dummy file: {file_name}")

# Create default profile image if it doesn't exist
default_profile_path = os.path.join(dest_img_dir, "default-profile.png")
with open(default_profile_path, "w") as f:
    f.write("") # empty file or we can just leave it

print("Setup completed successfully!")
