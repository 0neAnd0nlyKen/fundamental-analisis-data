
# Olist E-Commerce Analytics

Proyek ini menganalisis Brazilian E-Commerce Public Dataset by Olist dengan fokus pada:
1. Perkembangan jumlah pesanan dan total nilai pembayaran (GMV) per bulan.
2. Tingkat keterlambatan pengiriman berdasarkan negara bagian pelanggan.
3. Segmentasi pelanggan menggunakan metode RFM (Recency, Frequency, Monetary).

## Struktur Folder

```text
olist_submission/
├── notebook.ipynb
├── requirements.txt
├── README.md
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   └── olist_customers_dataset.csv
└── dashboard/
    └── dashboard.py
```

## 1. Persiapan Dataset

1. Unduh dataset Brazilian E-Commerce Public Dataset by Olist dari Kaggle:
   https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Ekstrak file dataset.
3. Masukkan file CSV ke dalam folder `data/`.
4. Pastikan empat file CSV utama tersedia.

## 2. Instalasi Library

Buka terminal pada direktori utama proyek, kemudian jalankan:

```bash
pip install -r requirements.txt
```

## 3. Menjalankan Notebook

Jalankan perintah:

```bash
jupyter notebook
```

Buka `notebook.ipynb`, kemudian jalankan seluruh cell secara berurutan menggunakan **Run All**.

## 4. Menjalankan Dashboard

Pastikan file `dashboard/dashboard.py` tersedia dan dataset sudah berada di folder `data/`.

Jalankan perintah berikut dari direktori utama proyek:

```bash
streamlit run dashboard/dashboard.py
```

Setelah berhasil dijalankan, buka alamat berikut melalui browser:

```text
http://localhost:8501
```

Dashboard akan menampilkan visualisasi dan ringkasan analisis data Olist.

Untuk menghentikan dashboard, tekan `Ctrl + C` pada terminal.

## 5. Catatan

- Dataset tidak disertakan dalam proyek dan harus diunduh secara terpisah.
- Jalankan perintah dari direktori utama proyek agar path folder `data/` dapat ditemukan.
- Pastikan nama file CSV tidak diubah.
