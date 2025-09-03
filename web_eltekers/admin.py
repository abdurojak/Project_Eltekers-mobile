from django.contrib import admin
from .models import Instruktur, JadwalLatihan, PengurusSasana, Peserta, Presensi, Sasana
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(Sasana)
admin.site.register(JadwalLatihan)
admin.site.register(Peserta)
admin.site.register(Instruktur)
admin.site.register(PengurusSasana)
admin.site.register(Presensi)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("role",)}),
    )
