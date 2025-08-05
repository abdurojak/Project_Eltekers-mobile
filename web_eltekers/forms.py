from django import forms
from .models import Sasana, Peserta, Instruktur

class SasanaForm(forms.ModelForm):
    # DEFINISIKAN FIELD LOKASI SECARA EKSPLISIT DI SINI
    # Ini memberitahu Django untuk menerima teks biasa, bukan memvalidasi pilihan.
    provinsi = forms.CharField(
        label='Provinsi',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    kota_kabupaten = forms.CharField(
        label='Kota/Kabupaten',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    kecamatan = forms.CharField(
        label='Kecamatan',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    kelurahan = forms.CharField(
        label='Kelurahan',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Sasana
        fields = [
            'nama_sasana', 'sejak', 'alamat_sasana',
            'provinsi', 'kota_kabupaten', 'kecamatan', 'kelurahan',
            'jumlah_instruktur', 'jumlah_peserta', 'peserta_aktif',
            'jumlah_latihan_per_minggu', 'link_gmap', 'profile'
        ]
        
        widgets = {
            'nama_sasana': forms.TextInput(attrs={'class': 'form-control'}),
            'sejak': forms.NumberInput(attrs={'class': 'form-control'}),
            'alamat_sasana': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'jumlah_instruktur': forms.NumberInput(attrs={'class': 'form-control'}),
            'jumlah_peserta': forms.NumberInput(attrs={'class': 'form-control'}),
            'peserta_aktif': forms.NumberInput(attrs={'class': 'form-control'}),
            'jumlah_latihan_per_minggu': forms.NumberInput(attrs={'class': 'form-control'}),
            'link_gmap': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://maps.app.goo.gl/abcdefg12345'}),
            'profile': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class PesertaForm(forms.ModelForm):
    class Meta:
        model = Peserta
        fields = '__all__'
        widgets = {
            'nama_peserta': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_lahir_peserta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'kendala_terapi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sasana': forms.Select(attrs={'class': 'form-control'}),
        }

class InstrukturForm(forms.ModelForm):
    class Meta:
        model = Instruktur
        fields = '__all__'
        widgets = {
            'nama_instruktur': forms.TextInput(attrs={'class': 'form-control'}),
            'sertifikasi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tanggal_sertifikasi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'file_sertifikat': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'sasana': forms.Select(attrs={'class': 'form-control'}),
        }