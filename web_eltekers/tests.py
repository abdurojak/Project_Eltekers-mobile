from django.test import TestCase
from .models import Sasana, Instruktur, Peserta
import uuid
import datetime

# Sasana
class SasanaPerformanceTestCase(TestCase):
    def setUp(self):
        start_time = datetime.datetime.now()

        sasanas = []
        size = 500
        for i in range(100000):
            sasana = Sasana(
                id_sasana=uuid.uuid4(),
                nama_sasana=f"Sasana {i}",
                sejak=2000 + (i % 24),
                alamat_sasana=f"Jl. Contoh No.{i}",
                kelurahan=f"Kelurahan {i % 100}",
                kecamatan=f"Kecamatan {i % 50}",
                kota_kabupaten=f"Kota {i % 30}",
                provinsi=f"Provinsi {i % 10}",
                nama_ketua=f"Ketua {i}",
                no_wa_ketua=6281234560000 + i,
                nama_pengurus=f"Pengurus {i}",
                no_wa_pengurus=628987650000 + i,
                jumlah_instruktur=i % 10 + 1,
                jumlah_peserta=i % 100 + 10,
                peserta_aktif=i % 100,
                jumlah_latihan_per_minggu=(i % 7) + 1
            )
            sasanas.append(sasana)
        Sasana.objects.bulk_create(sasanas, batch_size=size)

        end_time = datetime.datetime.now()
        print(f"Create method execution time: {end_time - start_time}")

    def test_lookup(self):
        start_time = datetime.datetime.now()

        for i in range(50000, 51000):
            Sasana.objects.get(nama_sasana=f"Sasana {i}")

        end_time = datetime.datetime.now()
        print(f"Get method execution time: {end_time - start_time}")

#Instruktur
class InstrukturSasanaRetrievalTestCase(TestCase):
    def setUp(self):
        start_time = datetime.datetime.now()

        self.sasana = Sasana.objects.create(
            id_sasana=uuid.uuid4(),
            nama_sasana="Sasana Hebat",
            sejak=2012,
            alamat_sasana="Jl. Contoh Hebat",
            kelurahan="Kelurahan Hebat",
            kecamatan="Kecamatan Hebat",
            kota_kabupaten="Kota Hebat",
            provinsi="Provinsi Hebat",
            nama_ketua="Ketua Hebat",
            no_wa_ketua=6281111111111,
            nama_pengurus="Pengurus Hebat",
            no_wa_pengurus=6282222222222,
            jumlah_instruktur=1,
            jumlah_peserta=1,
            peserta_aktif=1,
            jumlah_latihan_per_minggu=3
        )

        Instruktur.objects.create(
            id_instruktur=uuid.uuid4(),
            nama_instruktur="Instruktur Hebat",
            sertifikasi=True,
            tanggal_sertifikasi=datetime.date.today(),
            file_sertifikat='sertifikasi_instruktur/test.pdf',
            sasana=self.sasana
        )

        end_time = datetime.datetime.now()
        print(f"Instruktur create execution time: {end_time - start_time}")

    def test_without_select_related(self):
        start_time = datetime.datetime.now()
        for _ in range(100000):
            instruktur = Instruktur.objects.get(nama_instruktur="Instruktur Hebat")
            _ = instruktur.sasana.nama_sasana
        end_time = datetime.datetime.now()
        print(f"Instruktur without select_related time: {end_time - start_time}")

    def test_with_select_related(self):
        start_time = datetime.datetime.now()
        for _ in range(100000):
            instruktur = Instruktur.objects.select_related("sasana").get(nama_instruktur="Instruktur Hebat")
            _ = instruktur.sasana.nama_sasana
        end_time = datetime.datetime.now()
        print(f"Instruktur with select_related time: {end_time - start_time}")

#Peserta
class PesertaSasanaRetrievalTestCase(TestCase):
    def setUp(self):
        start_time = datetime.datetime.now()

        self.sasana = Sasana.objects.create(
            id_sasana=uuid.uuid4(),
            nama_sasana="Sasana Juara",
            sejak=2015,
            alamat_sasana="Jl. Juara No.1",
            kelurahan="Kelurahan Juara",
            kecamatan="Kecamatan Juara",
            kota_kabupaten="Kota Juara",
            provinsi="Provinsi Juara",
            nama_ketua="Ketua Juara",
            no_wa_ketua=6283333333333,
            nama_pengurus="Pengurus Juara",
            no_wa_pengurus=6284444444444,
            jumlah_instruktur=2,
            jumlah_peserta=2,
            peserta_aktif=2,
            jumlah_latihan_per_minggu=4
        )

        Peserta.objects.create(
            id_peserta=uuid.uuid4(),
            nama_peserta="Peserta Juara",
            tanggal_lahir_peserta=datetime.date(2010, 1, 1),
            kendala_terapi="Tidak ada",
            sasana=self.sasana
        )

        end_time = datetime.datetime.now()
        print(f"Peserta create execution time: {end_time - start_time}")

    def test_without_select_related(self):
        start_time = datetime.datetime.now()
        for _ in range(100000):
            peserta = Peserta.objects.get(nama_peserta="Peserta Juara")
            _ = peserta.sasana.nama_sasana
        end_time = datetime.datetime.now()
        print(f"Peserta without select_related time: {end_time - start_time}")

    def test_with_select_related(self):
        start_time = datetime.datetime.now()
        for _ in range(100000):
            peserta = Peserta.objects.select_related("sasana").get(nama_peserta="Peserta Juara")
            _ = peserta.sasana.nama_sasana
        end_time = datetime.datetime.now()
        print(f"Peserta with select_related time: {end_time - start_time}")