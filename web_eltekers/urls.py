# di web_eltekers/urls.py (jika ada)
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from web_eltekers.views import CustomTokenObtainPairView, me, me_web, my_sasana

urlpatterns = [
    # URL untuk autentikasi pengguna
    # Register User
    path("register/", views.register, name="register"),
    # Login/Logout via Django session
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),

    # Auth JWT
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Profile
    path('api/me/', me, name='me'),
    path("me/", me_web, name="me_web"),
    
    # URL untuk Sasana
    # Mengarah ke halaman list sebagai halaman utama modul sasana
    path('sasana/', views.list_sasana, name='list-sasana'), 
    path("api/my-sasana/", my_sasana, name="my_sasana"),
    path('sasana/tambah/', views.create_sasana, name='create-sasana'),
    path('sasana/<uuid:id_sasana>/', views.detail_sasana, name='detail-sasana'),
    path('sasana/<uuid:id_sasana>/edit/', views.update_sasana, name='update-sasana'),
    path('sasana/<uuid:id_sasana>/hapus/', views.delete_sasana, name='delete-sasana'),

    # URL untuk Peserta
    path('<uuid:sasana_id>/peserta/', views.list_peserta, name='list-peserta'),
    path('<uuid:sasana_id>/peserta/tambah/', views.create_peserta, name='create-peserta'),
    path('peserta/<uuid:id_peserta>/', views.detail_peserta, name='detail-peserta'),
    path('peserta/<uuid:id_peserta>/download-qr/', views.download_qr_peserta, name='download-qr-peserta'),
    path('peserta/<uuid:id_peserta>/edit/', views.update_peserta, name='update-peserta'),
    path('peserta/<uuid:id_peserta>/hapus/', views.delete_peserta, name='delete-peserta'),

    # URL untuk Instruktur
    path('<uuid:sasana_id>/instruktur/', views.list_instruktur, name='list-instruktur'),
    path('<uuid:sasana_id>/instruktur/tambah/', views.create_instruktur, name='create-instruktur'),
    path('instruktur/<uuid:id_instruktur>/', views.detail_instruktur, name='detail-instruktur'),
    path('instruktur/<uuid:id_instruktur>/edit/', views.update_instruktur, name='update-instruktur'),
    path('instruktur/<uuid:id_instruktur>/hapus/', views.delete_instruktur, name='delete-instruktur'),
    
    # Url untuk jadwal latihan
    path("api/jadwal-latihan/", views.jadwal_latihan_saya, name="jadwal_latihan"),
    
    # Url untuk presensi
    path('<uuid:sasana_id>/presensi-barcode/', views.show_barcode, name='show-barcode'),
    path('api/scan/', views.presensi_scan, name='presensi-scan'),
    path("presensi-hari-ini/", views.presensi_hari_ini, name="presensi_hari_ini"),
    path("api/presensi-saya-hari-ini/", views.presensi_saya_hari_ini, name="presensi_saya_hari_ini"),
    path("api/presensi-manual/", views.presensi_manual, name="presensi_manual"),
    path("api/sasana-terdekat/", views.sasana_terdekat, name="sasana_terdekat"),
    path("api/registrasi/", views.registrasi, name="registrasi"),
    path("api/riwayat-presensi/", views.riwayat_presensi, name="riwayat_presensi"),
    path("api/presensi-bulanan/", views.presensi_bulanan, name="presensi_bulanan"),
]
