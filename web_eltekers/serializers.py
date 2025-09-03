from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Peserta, Peraga, Instruktur, PengurusSasana, PengurusDaerah, Presensi, Sasana

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']
        
class SasanaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sasana
        fields = "__all__"
        
class PesertaSerializer(serializers.ModelSerializer):
    sasana = SasanaSerializer(read_only=True) 

    class Meta:
        model = Peserta
        fields = [
            "id_peserta",
            "nama_peserta",
            "tanggal_lahir_peserta",
            "kendala_terapi",
            "sasana",
        ]

class InstrukturSerializer(serializers.ModelSerializer):
    sasana = SasanaSerializer(read_only=True) 
    
    class Meta:
        model = Instruktur
        fields = "__all__"

class PeragaSerializer(serializers.ModelSerializer):
    sasana = SasanaSerializer(read_only=True) 
    
    class Meta:
        model = Peraga
        fields = "__all__"

class PengurusSasanaSerializer(serializers.ModelSerializer):
    sasana = SasanaSerializer(read_only=True) 
    
    class Meta:
        model = PengurusSasana
        fields = "__all__"

class PengurusDaerahSerializer(serializers.ModelSerializer):
    class Meta:
        model = PengurusDaerah
        fields = "__all__"
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # tambahkan role ke dalam payload JWT
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # tambahkan role juga ke response body
        data['role'] = self.user.role
        return data
    
class PresensiSerializer(serializers.ModelSerializer):
    nama_peserta = serializers.CharField(source='peserta.nama_peserta', read_only=True)
    nama_sasana = serializers.CharField(source='sasana.nama_sasana', read_only=True)

    class Meta:
        model = Presensi
        fields = [
            'id_presensi',
            'peserta',
            'nama_peserta',
            'sasana',
            'nama_sasana',
            'jadwal',
            'tanggal',
            'waktu'
        ]