from django import template
import datetime

register = template.Library()

bulan_indonesia = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

hari_indonesia = [
    "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"
]

@register.filter
def tanggal_indo(value):
    if isinstance(value, datetime.date):
        hari = hari_indonesia[value.weekday()]
        return f"{hari}, {value.day} {bulan_indonesia[value.month]} {value.year}"
    return value
