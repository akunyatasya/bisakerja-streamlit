# Business Questions for EDA and Explanatory Analysis

Dokumen ini merangkum pertanyaan bisnis utama yang akan dipakai untuk Exploratory Data Analysis (EDA), visualisasi, dan explanatory analysis pada dua dataset utama:

- `indotech_job_cleaned.csv` untuk data lowongan kerja tech di Indonesia
- `techtalent_profile_cleaned.csv` untuk data profil kandidat / resume

## Tujuan Analisis

1. Memetakan kebutuhan skill dan role yang paling dominan di pasar kerja tech Indonesia.
2. Mengukur seberapa dekat profil kandidat dengan kebutuhan pasar kerja.
3. Mengidentifikasi gap skill dan peluang upskilling yang paling penting.
4. Menyusun dasar analisis yang bisa diterjemahkan ke visualisasi dashboard dan narasi bisnis.

## Pertanyaan Utama

### 1. Skill apa yang paling banyak diminta oleh lowongan tech di Indonesia, dan seberapa siap kandidat terhadap skill tersebut?

**Pertanyaan inti:**
- Apa 10 skill teknis yang paling banyak diminta oleh lowongan kerja tech di Indonesia berdasarkan data terbaru?
- Berapa persentase kandidat dalam dataset resume yang sudah memiliki masing-masing skill tersebut?

**Nilai bisnis:**
- Menunjukkan skill paling kritikal di pasar.
- Membantu mengukur supply-demand skill gap antara lowongan dan kandidat.

**Catatan analisis:**
- Skill lowongan dapat diambil dari `skills_clean` dan dinormalisasi dengan `skill_taxonomy_bisakerja_v3.csv`.
- Skill kandidat diambil dari kolom `Skills` pada `techtalent_profile_cleaned.csv`.

### 2. Bagaimana distribusi tingkat pengalaman pada lowongan tech, dan apakah kandidat entry-level sudah memenuhi skill minimum?

**Pertanyaan inti:**
- Bagaimana distribusi tingkat pengalaman pada lowongan tech di Indonesia: `ENTRY_LEVEL`, `JUNIOR`, `MID_LEVEL`, `SENIOR`, dan `LEAD`?
- Apakah kandidat dengan profil `Fresher` dan `1-2 years` dalam dataset resume sudah memenuhi kualifikasi skill minimum untuk posisi entry level?

**Nilai bisnis:**
- Menunjukkan struktur kebutuhan tenaga kerja berdasarkan senioritas.
- Menguji kesiapan kandidat awal karier terhadap kebutuhan posisi entry-level.

**Catatan analisis:**
- Analisis skill minimum dapat didefinisikan dari pola skill yang paling sering muncul pada lowongan `ENTRY_LEVEL`.
- Cocok untuk dibandingkan dengan kandidat `Fresher` dan `1-2 years`.

### 3. Job role tech apa yang paling banyak tersedia di pasar kerja Indonesia, dan berapa proporsi kandidat yang sesuai?

**Pertanyaan inti:**
- Job role tech apa yang paling banyak tersedia berdasarkan data lowongan?
- Seberapa besar proporsi kandidat dalam dataset resume yang memiliki profil sesuai dengan role tersebut?

**Nilai bisnis:**
- Menunjukkan role dengan demand tertinggi.
- Membantu melihat apakah supply kandidat sudah mengikuti komposisi kebutuhan pasar.

**Catatan analisis:**
- Role lowongan perlu dinormalisasi menggunakan `job_role_taxonomy_bisakerja_v3.csv` bila ada variasi penamaan.
- Role kandidat diambil dari kolom `Job_Role`.

### 4. Seberapa besar kemiripan skill kandidat dengan kebutuhan lowongan entry-level tech?

**Pertanyaan inti:**
- Berapa rata-rata persentase kemiripan skill overlap antara profil kandidat dan persyaratan skill lowongan entry-level tech?
- Role atau kategori apa yang memiliki overlap paling tinggi dan paling rendah?

**Nilai bisnis:**
- Mengukur kualitas kecocokan kandidat terhadap pasar kerja.
- Menjadi dasar untuk rekomendasi pelatihan dan penempatan kandidat.

**Catatan analisis:**
- Skill overlap dapat dihitung dari irisan skill kandidat dan skill lowongan dibagi total skill yang relevan.
- Hasilnya bisa ditampilkan per role, kategori, atau tingkat pengalaman.

## Pertanyaan Tambahan yang Disarankan

### 5. Kategori lowongan tech apa yang paling dominan di Indonesia?

**Mengapa penting:**
- Membantu memahami komposisi pasar kerja tech secara lebih makro.
- Berguna untuk membandingkan demand antar kategori seperti `IT & Software`, `Data & Analytics`, `Product Management`, `QA & Testing`, dan lainnya.

### 6. Skill apa yang paling sering muncul di setiap kategori pekerjaan?

**Mengapa penting:**
- Menunjukkan skill spesifik per kategori, bukan hanya skill global.
- Membantu kandidat fokus pada skill yang paling relevan untuk role yang dituju.

### 7. Apakah kebutuhan skill berbeda berdasarkan tingkat pengalaman?

**Mengapa penting:**
- Entry-level biasanya menuntut skill dasar, sedangkan senior-level menuntut kombinasi skill teknis dan tools yang lebih kompleks.
- Analisis ini bisa memperjelas transisi kompetensi antar level karier.

### 8. Seberapa besar proporsi lowongan yang bersifat onsite, hybrid, dan remote?

**Mengapa penting:**
- Memberi konteks preferensi kerja di pasar tech Indonesia.
- Berguna untuk kandidat yang mempertimbangkan fleksibilitas kerja.

### 9. Apakah ada hubungan antara lokasi pekerjaan dan kebutuhan skill tertentu?

**Mengapa penting:**
- Membantu melihat perbedaan demand skill antar provinsi atau kota utama.
- Relevan untuk analisis regional dan strategi pencarian kerja.

### 10. Bagaimana distribusi gaji pada lowongan tech, khususnya untuk entry-level?

**Mengapa penting:**
- Memberi gambaran kompensasi di pasar kerja tech.
- Berguna sebagai konteks tambahan untuk narasi hasil analisis, meskipun sebagian lowongan tidak menampilkan gaji.

## Prioritas Analisis

### Prioritas tinggi
- Top 10 skill paling banyak diminta dan persentase kandidat yang memilikinya.
- Distribusi tingkat pengalaman lowongan.
- Job role tech paling banyak tersedia dan proporsi kandidat yang sesuai.
- Rata-rata skill overlap kandidat vs lowongan entry-level.

### Prioritas menengah
- Skill paling dominan per kategori pekerjaan.
- Perbedaan skill berdasarkan tingkat pengalaman.
- Distribusi work type dan lokasi pekerjaan.

### Prioritas tambahan jika waktu tersedia
- Analisis gaji.
- Analisis lokasi/provinsi.
- Visualisasi gap skill per role atau kategori.

## Definisi Operasional Singkat

- **Skill demand**: jumlah lowongan yang mencantumkan skill tertentu.
- **Skill supply**: jumlah kandidat yang memiliki skill tertentu.
- **Skill overlap**: irisan skill kandidat dan skill lowongan dalam bentuk persentase.
- **Entry-level jobs**: lowongan dengan `experience_level = ENTRY_LEVEL`.
- **Entry-level candidates**: kandidat dengan `Experience = Fresher` atau `1-2 years`.

## Output yang Diharapkan dari EDA

1. Tabel top skill dan top role.
2. Grafik distribusi experience level.
3. Diagram perbandingan demand vs supply skill.
4. Visualisasi overlap skill kandidat terhadap lowongan entry-level.
5. Ringkasan insight utama untuk dashboard dan presentasi.
