# ☸️ Strategi Viral Kalacakra OS

> Dokumen ini jujur tentang **apa yang membuat sebuah distro Linux viral** dan bagaimana
> Kalacakra bisa sampai ke sana — tanpa klaim berlebihan. Ditulis sebagai peta jalan,
> bukan janji.

---

## 1. Kenapa distro jadi viral (3 sumber)

Viral di komunitas Linux hampir selalu datang dari salah satu (atau kombinasi) dari ini:

1. **"Aku harus nyobain ini"** — UX/aesthetic yang belum ada di tempat lain (r/unixporn, rice).
2. **"Ini menyelesaikan masalah yang kubenci"** — painkiller nyata (Bazzite: "Steam Deck di PC-mu").
3. **"Aman/tumbuh buat user biasa"** — onboarding mulus.

**Realita Kalacakra saat ini:** 35 tool yang bagus, tapi belum ada **satu cerita** yang diingat orang.
Distro viral bukan yang fiturnya paling banyak — tapi yang punya **satu hal unforgettable**.

> ⚠️ **Diri sendiri jujur:** `k-wx`, `k-doas`, `k-signify` itu *canggih*, tapi tak ada yang bikin
> video tentang audit ELF. Fitur-fitur itu **pendukung kredibilitas**, bukan kendaraan viral.

---

## 2. Formula Kalacakra

```
1 FITUR IKONIK  (Look/Ricing)   ← bikin orang pertama meng-klik
+ 1 PAINKILLER  (Immutable UX)  ← bikin orang bertahan
+ 1 CERITA KHAS INDONESIA       ← bikin orang mengingatmu
= viral
```

### 🥇 Pilar 1 — FITUR IKONIK: Kalacakra Look

**Status: ✅ SUDAH DIIMPLEMENTASIKAN** (`rootfs/usr/bin/k-look`, 5 preset + wallpaper SVG).

- **Apa:** satu perintah mengubah seluruh identitas desktop (tema, warna, wallpaper, kursor,
  ikon, font, terminal, fastfetch) dan bisa di-rollback penuh.
- **Kenapa viral:** orang berbagi *screenshot*, bukan fitur. Anda punya peluang jadi
  **"distro paling cantik dari Indonesia"**.
- **Demo:** `kalacakra look apply mandala-cyberpunk --screenshot`
  → langsung hasilkan PNG + caption siap-tempel r/unixporn.
- **Bilingual & atomik:** cocok dengan DNA immutable; tulisan ke config user (aman).

**Langkah lanjutan (belum ada):**
- Preset tambahan (mis. "Batik Parang", "Rimba Sumatra", "Jakarta Neon").
- GUI kecil / KCM (System Settings module) untuk pemilihan preset visual.
- Galeri showcase daring + tombol "share" langsung terintegrasi.

### 🥈 Pilar 2 — PAINKILLER: Immutable yang Tidak Menyakitkan

**Status: ✅ SUDAH DIIMPLEMENTASIKAN** (`k-interceptor` cerdas).

- **Apa:** user ketik `sudo apt install vlc` → Kalacakra menjawab
  *"Rekomendasi: opsi 1 — 'vlc' tersedia sebagai Flatpak resmi. Tekan Enter."*
  → nama umum dipetakan ke ID Flathub (`org.videolan.VLC`) secara otomatis.
- **Kenapa viral:** *"Distro immutable yang tidak bikin pusing"* — painkiller nyata.
  Ambil pain terbesar distro immutable dan hapus.
- **Jujur:** hanya merekomendasikan backend yang **benar-benar tersedia**; jika Flatpak absen,
  tidak memaksa/memalsukan.

**Langkah lanjutan (belum ada):**
- Basis data alias Flatpak yang jauh lebih besar / lookup daring.
- Integrasi Discover/GNOME Software yang otomatis menyarankan sumber yang benar.

### 🇮🇩 Pilar 3 — CERITA KHAS INDONESIA

**Status: ✅ SUDAH DIIMPLEMENTASIKAN** (`k-showcase`, i18n penuh, tema bernuansa Nusantara).

- **Apa:** dwibahasa EN/ID penuh sejak boot pertama; preset bernuansa Indonesia
  (Mandala Cyberpunk, Nusantara Bronze, Kraton Gold); `kalacakra showcase` menampilkan
  identitas siap-screenshot.
- **Kenapa viral (di Indonesia):** *"distro Linux yang serius berbahasa Indonesia"* hampir
  tidak ada. Ini pasar yang bisa dimenangkan total.

**Langkah lanjutan (belum ada):**
- Video/screenshot dwibahasa, dokumentasi penuh ID, tutorial YouTube.
- Landing page dengan galeri tema + testimonials.

---

## 3. Yang JANGAN dilakukan

- ❌ **Menambah tool ke-36, ke-37, ke-38…** — 35 sudah lebih dari cukup. Tambah **cerita**, bukan tool.
- ❌ **Mengklaim "setara Debian/OpenBSD/Arch"** secara literal — sudah dikoreksi di README sebagai filosofi.
- ❌ **Menjanjikan fitur roadmap sebagai fitur jadi** — lawan dari prinsip proyek ini.

---

## 4. Definisi Sukses (jujur & terukur)

| Metrik | Baseline | Target realistis |
|---|---|---|
| Screenshot Kalacakra Look di r/unixporn | 0 | ≥ 1 post viral |
| Preset Look | 5 | 10+ komunitas |
| Dokumentasi dwibahasa penuh | sebagian | lengkap |
| First-run experience | CLI | wizard yang mulus |

**Yang paling penting:** satu orang membuat satu video/screenshot dengan caption
*"Distro Linux dari Indonesia yang bikin desktop-ku cantik dalam satu perintah."*
Itulah momen viral-nya.

---

## 5. Langkah konkret berikutnya (prioritas)

1. ✅ **Preset komunitas** — `kalacakra look import <berkas/URL> [--install]` (format JSON tervalidasi; preset user menimpa preset bawaan).
2. ✅ **Wizard first-run** (`kalacakra welcome`) — alur bahasa → tema Look → status AI/voice → ringkasan (dwibahasa, bisa non-interaktif `--yes`).
3. ⬜ **Galeri showcase daring** — halaman statis yang menampilkan screenshot komunitas (belum ada).
4. ⬜ **Konten** — tutorial dwibahasa, video "1 perintah ubah tampilan" (belum ada).

> **Status jujur:** Item 1 & 2 **sudah dikerjakan** dan diuji (`tests/test_cli.py`, kini 65 test). Item 3 & 4 masih rencana. Dokumen ini peta, bukan klaim.
