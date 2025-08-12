# di web_eltekers/urls.py (jika ada)
from django.urls import path
from . import views

urlpatterns = [
    # URL untuk Sasana
    # Mengarah ke halaman list sebagai halaman utama modul sasana
    path('sasana/', views.list_sasana, name='list-sasana'), 
    path('sasana/tambah/', views.create_sasana, name='create-sasana'),
    path('sasana/<uuid:id_sasana>/', views.detail_sasana, name='detail-sasana'),
    path('sasana/<uuid:id_sasana>/edit/', views.update_sasana, name='update-sasana'),
    path('sasana/<uuid:id_sasana>/hapus/', views.delete_sasana, name='delete-sasana'),

    # URL untuk Peserta
    path('<uuid:sasana_id>/peserta/', views.list_peserta, name='list-peserta'),
    path('<uuid:sasana_id>/peserta/tambah/', views.create_peserta, name='create-peserta'),
    path('peserta/<uuid:id_peserta>/', views.detail_peserta, name='detail-peserta'),
    path('peserta/<uuid:id_peserta>/edit/', views.update_peserta, name='update-peserta'),
    path('peserta/<uuid:id_peserta>/hapus/', views.delete_peserta, name='delete-peserta'),

    # URL untuk Instruktur
    path('<uuid:sasana_id>/instruktur/', views.list_instruktur, name='list-instruktur'),
    path('<uuid:sasana_id>/instruktur/tambah/', views.create_instruktur, name='create-instruktur'),
    path('instruktur/<uuid:id_instruktur>/', views.detail_instruktur, name='detail-instruktur'),
    path('instruktur/<uuid:id_instruktur>/edit/', views.update_instruktur, name='update-instruktur'),
    path('instruktur/<uuid:id_instruktur>/hapus/', views.delete_instruktur, name='delete-instruktur'),
    
    # Url untuk presensi
    path('<uuid:sasana_id>/presensi-barcode/', views.show_barcode, name='show-barcode'), 
]
