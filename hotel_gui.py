import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Kamar:
    def __init__(self, nomor_kamar, tipe_kamar, harga_per_malam, status="Tersedia"):
        self.nomor_kamar = nomor_kamar
        self.tipe_kamar = tipe_kamar
        self.harga_per_malam = harga_per_malam
        self.status = status

class Tamu:
    def __init__(self, nama, nomor_identitas, kontak):
        self.nama = nama
        self.nomor_identitas = nomor_identitas
        self.kontak = kontak
        self.reservasi = None  # Satu tamu hanya boleh memiliki satu reservasi aktif

class Reservasi:
    def __init__(self, tamu, kamar, tanggal_check_in, tanggal_check_out):
        self.tamu = tamu
        self.kamar = kamar
        self.tanggal_check_in = tanggal_check_in
        self.tanggal_check_out = tanggal_check_out
        self.status = "Aktif"
        # Set status kamar menjadi "Dipesan" setelah reservasi dibuat
        self.kamar.status = "Dipesan"

    def batalkan(self):
        self.status = "Dibatalkan"
        self.kamar.status = "Tersedia"

class Hotel:
    def __init__(self):
        self.kamar_dict = {}
        self.tamu_list = []
        self.reservasi_list = []

    def tambah_kamar(self, nomor_kamar, tipe_kamar, harga_per_malam):
        if nomor_kamar not in self.kamar_dict:
            kamar = Kamar(nomor_kamar, tipe_kamar, harga_per_malam)
            self.kamar_dict[nomor_kamar] = kamar
            return f"Kamar {nomor_kamar} berhasil ditambahkan."
        else:
            return "Kamar dengan nomor tersebut sudah ada."

    def tambah_tamu(self, nama, nomor_identitas, kontak):
        tamu = Tamu(nama, nomor_identitas, kontak)
        self.tamu_list.append(tamu)
        return f"Tamu {nama} berhasil ditambahkan."

    def daftar_kamar_tersedia(self):
        kamar_tersedia = [f"{k.nomor_kamar} - {k.tipe_kamar} ({k.status})" for k in self.kamar_dict.values() if k.status == "Tersedia"]
        return "\n".join(kamar_tersedia) if kamar_tersedia else "Tidak ada kamar tersedia."

    def buat_reservasi(self, nama_tamu, nomor_kamar, check_in, check_out):
        kamar = self.kamar_dict.get(nomor_kamar)
        tamu = next((t for t in self.tamu_list if t.nama == nama_tamu), None)

        if not tamu:
            return "Tamu tidak ditemukan."
        if not kamar or kamar.status != "Tersedia":
            return "Kamar tidak tersedia untuk reservasi."
        if tamu.reservasi:
            return "Tamu sudah memiliki reservasi aktif."

        reservasi = Reservasi(tamu, kamar, check_in, check_out)
        tamu.reservasi = reservasi
        self.reservasi_list.append(reservasi)
        return "Reservasi berhasil dibuat."

    def batalkan_reservasi(self, nama_tamu):
        tamu = next((t for t in self.tamu_list if t.nama == nama_tamu), None)
        if tamu and tamu.reservasi:
            tamu.reservasi.batalkan()
            tamu.reservasi = None
            return "Reservasi berhasil dibatalkan."
        return "Tidak ada reservasi aktif untuk tamu tersebut."

    def info_reservasi_aktif(self, nama_tamu):
        tamu = next((t for t in self.tamu_list if t.nama == nama_tamu), None)
        if tamu and tamu.reservasi:
            reservasi = tamu.reservasi
            return (f"Reservasi untuk {tamu.nama}:\nKamar: {reservasi.kamar.nomor_kamar}\n"
                    f"Check-in: {reservasi.tanggal_check_in}\nCheck-out: {reservasi.tanggal_check_out}\nStatus: {reservasi.status}")
        return "Tidak ada reservasi aktif untuk tamu tersebut."

# GUI Implementation
hotel = Hotel()

def tambah_kamar():
    nomor_kamar = entry_nomor_kamar.get()
    tipe_kamar = entry_tipe_kamar.get()
    harga_per_malam = entry_harga_per_malam.get()

    if nomor_kamar and tipe_kamar and harga_per_malam:
        pesan = hotel.tambah_kamar(nomor_kamar, tipe_kamar, harga_per_malam)
        messagebox.showinfo("Info", pesan)
        entry_nomor_kamar.delete(0, tk.END)
        entry_tipe_kamar.delete(0, tk.END)
        entry_harga_per_malam.delete(0, tk.END)
    else:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")

def tambah_tamu():
    nama = entry_nama_tamu.get()
    nomor_identitas = entry_nomor_identitas.get()
    kontak = entry_kontak.get()

    if nama and nomor_identitas and kontak:
        pesan = hotel.tambah_tamu(nama, nomor_identitas, kontak)
        messagebox.showinfo("Info", pesan)
        entry_nama_tamu.delete(0, tk.END)
        entry_nomor_identitas.delete(0, tk.END)
        entry_kontak.delete(0, tk.END)
    else:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")

def lihat_kamar_tersedia():
    kamar_tersedia = hotel.daftar_kamar_tersedia()
    messagebox.showinfo("Kamar Tersedia", kamar_tersedia)

def buat_reservasi():
    nama_tamu = entry_reservasi_nama_tamu.get()
    nomor_kamar = entry_reservasi_nomor_kamar.get()
    check_in = entry_check_in.get()
    check_out = entry_check_out.get()

    if nama_tamu and nomor_kamar and check_in and check_out:
        pesan = hotel.buat_reservasi(nama_tamu, nomor_kamar, check_in, check_out)
        messagebox.showinfo("Info", pesan)
    else:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")

def batalkan_reservasi():
    nama_tamu = entry_batal_reservasi.get()
    if nama_tamu:
        pesan = hotel.batalkan_reservasi(nama_tamu)
        messagebox.showinfo("Info", pesan)
    else:
        messagebox.showwarning("Peringatan", "Nama tamu harus diisi.")

def info_reservasi_aktif():
    nama_tamu = entry_info_reservasi.get()
    if nama_tamu:
        pesan = hotel.info_reservasi_aktif(nama_tamu)
        messagebox.showinfo("Info Reservasi", pesan)
    else:
        messagebox.showwarning("Peringatan", "Nama tamu harus diisi.")

root = tk.Tk()
root.title("Sistem Manajemen Hotel")

# Frame Tambah Kamar
frame_kamar = tk.Frame(root)
frame_kamar.pack(pady=5)

tk.Label(frame_kamar, text="Tambah Kamar").grid(row=0, column=1)
tk.Label(frame_kamar, text="Nomor Kamar:").grid(row=1, column=0)
entry_nomor_kamar = tk.Entry(frame_kamar)
entry_nomor_kamar.grid(row=1, column=1)
tk.Label(frame_kamar, text="Tipe Kamar:").grid(row=2, column=0)
entry_tipe_kamar = tk.Entry(frame_kamar)
entry_tipe_kamar.grid(row=2, column=1)
tk.Label(frame_kamar, text="Harga per Malam:").grid(row=3, column=0)
entry_harga_per_malam = tk.Entry(frame_kamar)
entry_harga_per_malam.grid(row=3, column=1)
tk.Button(frame_kamar, text="Tambah Kamar", command=tambah_kamar).grid(row=4, column=1)

# Frame Tambah Tamu
frame_tamu = tk.Frame(root)
frame_tamu.pack(pady=5)

tk.Label(frame_tamu, text="Tambah Tamu").grid(row=0, column=1)
tk.Label(frame_tamu, text="Nama Tamu:").grid(row=1, column=0)
entry_nama_tamu = tk.Entry(frame_tamu)
entry_nama_tamu.grid(row=1, column=1)
tk.Label(frame_tamu, text="Nomor Identitas:").grid(row=2, column=0)
entry_nomor_identitas = tk.Entry(frame_tamu)                  
entry_nomor_identitas.grid(row=2, column=1)
tk.Label(frame_tamu, text="Kontak:").grid(row=3, column=0)
entry_kontak = tk.Entry(frame_tamu)
entry_kontak.grid(row=3, column=1)
tk.Button(frame_tamu, text="Tambah Tamu", command=tambah_tamu).grid(row=4, column=1)

# Frame Reservasi
frame_reservasi = tk.Frame(root)
frame_reservasi.pack(pady=5)

tk.Label(frame_reservasi, text="Buat Reservasi").grid(row=0, column=1)
tk.Label(frame_reservasi, text="Nama Tamu:").grid(row=1, column=0)
entry_reservasi_nama_tamu = tk.Entry(frame_reservasi)
entry_reservasi_nama_tamu.grid(row=1, column=1)
tk.Label(frame_reservasi, text="Nomor Kamar:").grid(row=2, column=0)
entry_reservasi_nomor_kamar = tk.Entry(frame_reservasi)
entry_reservasi_nomor_kamar.grid(row=2, column=1)
tk.Label(frame_reservasi, text="Tanggal Check-in (YYYY-MM-DD):").grid(row=3, column=0)
entry_check_in = tk.Entry(frame_reservasi)
entry_check_in.grid(row=3, column=1)
tk.Label(frame_reservasi, text="Tanggal Check-out (YYYY-MM-DD):").grid(row=4, column=0)
entry_check_out = tk.Entry(frame_reservasi)
entry_check_out.grid(row=4, column=1)
tk.Button(frame_reservasi, text="Buat Reservasi", command=buat_reservasi).grid(row=5, column=1)

# Frame Batalkan Reservasi
frame_batal_reservasi = tk.Frame(root)
frame_batal_reservasi.pack(pady=5)

tk.Label(frame_batal_reservasi, text="Batalkan Reservasi").grid(row=0, column=1)
tk.Label(frame_batal_reservasi, text="Nama Tamu:").grid(row=1, column=0)
entry_batal_reservasi = tk.Entry(frame_batal_reservasi)
entry_batal_reservasi.grid(row=1, column=1)
tk.Button(frame_batal_reservasi, text="Batalkan Reservasi", command=batalkan_reservasi).grid(row=2, column=1)

# Frame Info Reservasi Aktif
frame_info_reservasi = tk.Frame(root)
frame_info_reservasi.pack(pady=5)

tk.Label(frame_info_reservasi, text="Informasi Reservasi Aktif").grid(row=0, column=1)
tk.Label(frame_info_reservasi, text="Nama Tamu:").grid(row=1, column=0)
entry_info_reservasi = tk.Entry(frame_info_reservasi)
entry_info_reservasi.grid(row=1, column=1)
tk.Button(frame_info_reservasi, text="Lihat Informasi", command=info_reservasi_aktif).grid(row=2, column=1)

# Frame Lihat Kamar Tersedia
frame_kamar_tersedia = tk.Frame(root)
frame_kamar_tersedia.pack(pady=5)

tk.Button(frame_kamar_tersedia, text="Lihat Kamar Tersedia", command=lihat_kamar_tersedia).grid(row=0, column=0)

# Menjalankan aplikasi GUI
root.mainloop()
