# Media Monitoring API & Dashboard

Backend service dan dashboard interaktif untuk melakukan ingestion, pencarian, serta analisis statistik data media mentions.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL (Cloud via Supabase)
- **ORM:** SQLAlchemy
- **Frontend / Dashboard:** Streamlit
- **Data Processing:** Python-dateutil, Pandas

## 🚀 Fitur Utama
1. **Bulk Ingestion (`POST /internal/mentions/bulk`)**
   - **Data Cleaning:** Menghapus tag HTML pada `content`/`title`, normalisasi nama `source` menjadi lowercase, serta parsing datetime ISO.
   - **Idempotency:** Menggunakan constraint `UNIQUE` pada kolom `url` (`ON CONFLICT DO NOTHING`) sehingga eksekusi berulang tidak memicu duplikasi data.
2. **Search & Filter (`GET /mentions`)**
   - Filtering berdasarkan `source` dan pencarian teks (`q`) pada judul/konten.
   - Support paginasi (`page`, `limit`) dan pengurutan (`sort_by`, `order`).
3. **Analytics Stats (`GET /mentions/stats`)**
   - Agregasi total mentions, total engagement, serta breakdown per media source.
4. **Interactive Dashboard**
   - Visualisasi grafis breakdown data dan pencarian interaktif menggunakan Streamlit.

## 📦 Cara Menjalankan Project

1. **Aktifkan Virtual Environment & Install Dependencies:**
   ```bash
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt

2. **Jalankan Backend FastAPI:**
  uvicorn app.main:app --reload
  Akses Swagger UI di: http://127.0.0.1:8000/docs

3. **Jalankan Dashboard Streamlit:**
  streamlit run streamlit_app.py
  Akses Dashboard di: http://localhost:8501