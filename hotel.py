from datetime import datetime

class Kamar:
    def __init__(self, nomor_kamar, tipe_kamar, harga_per_malam, status="Tersedia"):
        self.nomor_kamar = nomor_kamar
        self.tipe_kamar = tipe_kamar
        self.harga_per_malam = harga_per_malam
        self.status = status

    def tampilkan_info_kamar(self):
        print(f"Nomor Kamar: {self.nomor_kamar}, Tipe: {self.tipe_kamar}, Harga per malam: {self.harga_per_malam}, Status: {self.status}")


class KamarSingle(Kamar):
    def __init__(self, nomor_kamar, harga_per_malam):
        super().__init__(nomor_kamar, "Single", harga_per_malam)


class KamarDouble(Kamar):
    def __init__(self, nomor_kamar, harga_per_malam):
        super().__init__(nomor_kamar, "Double", harga_per_malam)


class Tamu:
    def __init__(self, nama, nomor_identitas, kontak):
        self.nama = nama
        self.nomor_identitas = nomor_identitas
        self.kontak = kontak
        self.daftar_reservasi = []

    def tampilkan_info_tamu(self):
        print(f"Nama: {self.nama}, Nomor Identitas: {self.nomor_identitas}, Kontak: {self.kontak}")


class Reservasi:
    def __init__(self, tamu, kamar, tanggal_check_in, tanggal_check_out):
        self.tamu = tamu
        self.kamar = kamar
        self.status = "Aktif"
        self.kamar.status = "Dipesan"

        try:
            # Validasi format tanggal dan perhitungan durasi menginap
            check_in_date = datetime.strptime(tanggal_check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(tanggal_check_out, "%Y-%m-%d")

            # Pastikan check-out setelah check-in
            if check_out_date <= check_in_date:
                raise ValueError("Tanggal check-out harus setelah tanggal check-in.")

            self.tanggal_check_in = tanggal_check_in
            self.tanggal_check_out = tanggal_check_out
            self.durasi_menginap = (check_out_date - check_in_date).days

        except ValueError as e:
            print(f"Error pada tanggal: {e}")
            self.tanggal_check_in = None
            self.tanggal_check_out = None
            self.durasi_menginap = 0
            self.status = "Error"

    def tampilkan_info_reservasi(self):
        if self.status == "Error":
            print("Reservasi memiliki kesalahan dan tidak valid.")
        else:
            print(f"Tamu: {self.tamu.nama}, Kamar: {self.kamar.nomor_kamar}, "
                  f"Check-in: {self.tanggal_check_in}, Check-out: {self.tanggal_check_out}, "
                  f"Durasi: {self.durasi_menginap} malam, Status: {self.status}")

    def batalkan_reservasi(self):
        if self.status != "Error":
            self.status = "Dibatalkan"
            self.kamar.status = "Tersedia"
            print("Reservasi berhasil dibatalkan.")
        else:
            print("Tidak dapat membatalkan reservasi yang tidak valid.")


class Hotel:
    def __init__(self):
        self.kamar_dict = {}
        self.daftar_tamu = []
        self.daftar_reservasi = []

    def tambah_kamar(self, kamar):
        self.kamar_dict[kamar.nomor_kamar] = kamar
        print(f"Kamar {kamar.nomor_kamar} berhasil ditambahkan.")

    def tambah_tamu(self, tamu):
        self.daftar_tamu.append(tamu)
        print(f"Tamu {tamu.nama} berhasil ditambahkan.")

    def buat_reservasi(self, tamu, kamar, tanggal_check_in, tanggal_check_out):
        if kamar.status == "Tersedia":
            reservasi = Reservasi(tamu, kamar, tanggal_check_in, tanggal_check_out)
            if reservasi.status == "Aktif":
                self.daftar_reservasi.append(reservasi)
                tamu.daftar_reservasi.append(reservasi)
                print("Reservasi berhasil dibuat.")
            else:
                print("Gagal membuat reservasi karena tanggal tidak valid.")
        else:
            print("Kamar tidak tersedia untuk reservasi.")

    def batalkan_reservasi(self, reservasi):
        reservasi.batalkan_reservasi()

    def daftar_kamar_tersedia(self):
        print("Kamar yang tersedia:")
        for kamar in self.daftar_kamar:
            if kamar.status == "Tersedia":
                kamar.tampilkan_info_kamar()

    def cari_kamar(self, nomor_kamar):
        return self.kamar_dict.get(nomor_kamar, None)

    def cari_tamu(self, nama_tamu):
        for tamu in self.daftar_tamu:
            if tamu.nama == nama_tamu:
                return tamu
        return None


def main():
    hotel = Hotel()
    while True:
        print("\n=== Sistem Manajemen Hotel ===")
        print("1. Tambah Kamar")
        print("2. Tambah Tamu")
        print("3. Buat Reservasi")
        print("4. Batalkan Reservasi")
        print("5. Daftar Kamar Tersedia")
        print("6. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            nomor_kamar = input("Masukkan nomor kamar: ")
            tipe_kamar = input("Masukkan tipe kamar (Single/Double): ")
            harga_per_malam = float(input("Masukkan harga per malam: "))
            if tipe_kamar.lower() == "single":
                kamar = KamarSingle(nomor_kamar, harga_per_malam)
            elif tipe_kamar.lower() == "double":
                kamar = KamarDouble(nomor_kamar, harga_per_malam)
            else:
                print("Tipe kamar tidak valid.")
                continue
            hotel.tambah_kamar(kamar)

        elif pilihan == "2":
            nama = input("Masukkan nama tamu: ")
            nomor_identitas = input("Masukkan nomor identitas: ")
            kontak = input("Masukkan kontak: ")
            tamu = Tamu(nama, nomor_identitas, kontak)
            hotel.tambah_tamu(tamu)

        elif pilihan == "3":
            nama_tamu = input("Masukkan nama tamu: ")
            nomor_kamar = input("Masukkan nomor kamar: ")
            tanggal_check_in = input("Masukkan tanggal check-in (YYYY-MM-DD): ")
            tanggal_check_out = input("Masukkan tanggal check-out (YYYY-MM-DD): ")

            tamu = hotel.cari_tamu(nama_tamu)
            kamar = hotel.cari_kamar(nomor_kamar)

            if tamu and kamar:
                hotel.buat_reservasi(tamu, kamar, tanggal_check_in, tanggal_check_out)
            else:
                print("Tamu atau kamar tidak ditemukan.")

        elif pilihan == "4":
            nama_tamu = input("Masukkan nama tamu untuk membatalkan reservasi: ")
            tamu = hotel.cari_tamu(nama_tamu)
            if tamu and tamu.daftar_reservasi:
                hotel.batalkan_reservasi(tamu.daftar_reservasi[0])
            else:
                print("Tidak ada reservasi untuk dibatalkan.")

        elif pilihan == "5":
            hotel.daftar_kamar_tersedia()

        elif pilihan == "6":
            print("Terima kasih telah menggunakan sistem manajemen hotel.")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    main()