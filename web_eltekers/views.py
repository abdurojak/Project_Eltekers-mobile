from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CustomUserCreationForm, SasanaForm, PesertaForm, InstrukturForm
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import localtime
from rest_framework import status
from django.utils.timezone import now
from datetime import date

# Autentikasi
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from django.contrib.auth.decorators import login_required

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
       
# List Api
@api_view(["GET"])
@permission_classes([IsAuthenticated])
# Detail Saya (Untuk Peserta)
def me(request):
    user = request.user

    user_data = UserSerializer(user).data

    if user.role == "peserta":
        try:
            peserta = Peserta.objects.get(user=user)
            peserta_data = PesertaSerializer(peserta).data

            qr_payload = {
                "id_peserta": str(peserta.id_peserta),
                "nama_peserta": peserta.nama_peserta,
                "tanggal_lahir_peserta": str(peserta.tanggal_lahir_peserta),
                "id_sasana": str(peserta.sasana_id) if peserta.sasana else None
            }

            qr = qrcode.make(qr_payload)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            peserta_data["qrcode"] = f"data:image/png;base64,{qr_base64}"
            user_data["detail"] = peserta_data

        except Peserta.DoesNotExist:
            user_data["detail"] = None

    elif user.role == "instruktur":
        try:
            instruktur = Instruktur.objects.get(user=user)
            user_data["detail"] = InstrukturSerializer(instruktur).data
        except Instruktur.DoesNotExist:
            user_data["detail"] = None

    elif user.role == "peraga":
        try:
            peraga = Peraga.objects.get(user=user)
            user_data["detail"] = PeragaSerializer(peraga).data
        except Peraga.DoesNotExist:
            user_data["detail"] = None

    elif user.role == "pengurus_sasana":
        try:
            pengurus = PengurusSasana.objects.get(user=user)
            user_data["detail"] = PengurusSasanaSerializer(pengurus).data
        except PengurusSasana.DoesNotExist:
            user_data["detail"] = None

    elif user.role == "pengurus_daerah":
        try:
            pengurus = PengurusDaerah.objects.get(user=user)
            user_data["detail"] = PengurusDaerahSerializer(pengurus).data
        except PengurusDaerah.DoesNotExist:
            user_data["detail"] = None

    return Response(user_data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_sasana(request):
    user = request.user
    sasana_data = None

    try:
        if user.role == "peserta":
            peserta = Peserta.objects.get(user=user)
            if peserta.sasana:
                sasana_data = SasanaSerializer(peserta.sasana).data

        elif user.role == "instruktur":
            instruktur = Instruktur.objects.get(user=user)
            if instruktur.sasana:
                sasana_data = SasanaSerializer(instruktur.sasana).data

        elif user.role == "peraga":
            peraga = Peraga.objects.get(user=user)
            if peraga.sasana:
                sasana_data = SasanaSerializer(peraga.sasana).data

        elif user.role == "pengurus_sasana":
            pengurus = PengurusSasana.objects.get(user=user)
            if pengurus.sasana:
                sasana_data = SasanaSerializer(pengurus.sasana).data

    except Exception:
        sasana_data = None

    return Response({"sasana": sasana_data})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def presensi_hari_ini(request):
    id_sasana = request.query_params.get("id_sasana")
    if not id_sasana:
        return Response({"status": "error", "message": "id_sasana harus diisi"}, status=400)

    today = now().date()
    presensi = Presensi.objects.filter(
        sasana_id=id_sasana,
        tanggal=today
    ).select_related("peserta", "sasana", "jadwal").order_by("waktu")

    serializer = PresensiSerializer(presensi, many=True)

    return Response({
        "status": "success",
        "message": f"Daftar presensi di sasana {id_sasana} tanggal {today}",
        "count": len(serializer.data),
        "results": serializer.data
    })
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def presensi_saya_hari_ini(request):
    user = request.user

    try:
        # Tentukan sasana user
        sasana = None
        if user.role == "peserta":
            peserta = Peserta.objects.get(user=user)
            sasana = peserta.sasana
        elif user.role == "instruktur":
            instruktur = Instruktur.objects.get(user=user)
            sasana = instruktur.sasana
        elif user.role == "peraga":
            peraga = Peraga.objects.get(user=user)
            sasana = peraga.sasana
        elif user.role == "pengurus_sasana":
            pengurus = PengurusSasana.objects.get(user=user)
            sasana = pengurus.sasana

        if not sasana:
            return Response({
                "status": "error",
                "message": "User tidak terdaftar pada sasana manapun"
            }, status=status.HTTP_404_NOT_FOUND)

        # Ambil presensi hari ini di sasana user
        presensi_qs = Presensi.objects.filter(
            sasana=sasana,
            tanggal=date.today()
        ).select_related("peserta").order_by("waktu")

        data = [
            {
                "id_presensi": str(p.id_presensi),
                "peserta": p.peserta.nama_peserta,
                "tanggal": str(p.tanggal),
                "waktu": p.waktu.strftime("%H:%M:%S")
            }
            for p in presensi_qs
        ]

        return Response({
            "status": "success",
            "sasana": sasana.nama_sasana,
            "tanggal": str(date.today()),
            "data": data
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def presensi_scan(request):
    try:
        print("DEBUG request.data:", request.data)

        id_peserta = request.data.get("id_peserta")
        id_sasana = request.data.get("id_sasana")

        if not id_peserta or not id_sasana:
            return Response({
                "status": "error",
                "message": "id_peserta dan id_sasana wajib diisi"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validasi peserta & sasana
        try:
            peserta = Peserta.objects.get(id_peserta=id_peserta)
        except Peserta.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Peserta tidak ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            sasana = Sasana.objects.get(id_sasana=id_sasana)
        except Sasana.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Sasana tidak ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)

        # Cek jadwal hari ini
        hari_ini = now().strftime("%A")  # "Monday", "Tuesday" ...
        hari_map = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
        }
        hari_django = hari_map.get(hari_ini)

        jadwal = JadwalLatihan.objects.filter(hari=hari_django, sasana=sasana).first()
        if not jadwal:
            return Response({
                "status": "error",
                "message": f"Tidak ada jadwal latihan di {sasana.nama_sasana} hari {hari_django}"
            }, status=status.HTTP_404_NOT_FOUND)

        # Cek duplikat presensi
        if Presensi.objects.filter(
            peserta=peserta,
            sasana=sasana,
            jadwal=jadwal,
            tanggal=date.today()
        ).exists():
            return Response({
                "status": "error",
                "message": "Peserta sudah melakukan presensi hari ini"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Simpan presensi
        presensi = Presensi.objects.create(
            peserta=peserta,
            sasana=sasana,
            jadwal=jadwal,
            tanggal=date.today(),
            waktu=now().time()
        )

        return Response({
            "status": "success",
            "message": "Presensi berhasil disimpan",
            "data": {
                "id_presensi": str(presensi.id_presensi),
                "peserta": peserta.nama_peserta,
                "sasana": sasana.nama_sasana,
                "hari": jadwal.hari,
                "jam_latihan": jadwal.jam_latihan.strftime("%H:%M"),
                "tanggal": str(presensi.tanggal),
                "waktu": presensi.waktu.strftime("%H:%M:%S"),
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("ERROR presensi_scan:", e)
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def presensi_manual(request):
    try:
        user = request.user

        # tentukan sasana user dari role
        sasana = None
        if user.role == "instruktur":
            instruktur = Instruktur.objects.get(user=user)
            sasana = instruktur.sasana
        elif user.role == "pengurus_sasana":
            pengurus = PengurusSasana.objects.get(user=user)
            sasana = pengurus.sasana
        else:
            return Response({
                "status": "error",
                "message": "Hanya instruktur / pengurus sasana yang boleh menambah presensi manual"
            }, status=status.HTTP_403_FORBIDDEN)

        if not sasana:
            return Response({
                "status": "error",
                "message": "Sasana tidak ditemukan"
            }, status=status.HTTP_404_NOT_FOUND)

        # data dari request
        nama = request.data.get("nama_peserta")
        tanggal_lahir = request.data.get("tanggal_lahir_peserta")
        kendala = request.data.get("kendala_terapi")
        username = request.data.get("username")
        password = request.data.get("password")

        if not all([nama, tanggal_lahir, username, password]):
            return Response("Field wajib belum lengkap", status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response(
                "Username sudah terpakai!",
                status=status.HTTP_400_BAD_REQUEST
        )

        # cari jadwal hari ini
        hari_ini = now().strftime("%A")
        hari_map = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
        }
        hari_django = hari_map.get(hari_ini)

        jadwal = JadwalLatihan.objects.filter(hari=hari_django, sasana=sasana).first()
        if not jadwal:
            return Response(f"Tidak ada jadwal latihan di {sasana.nama_sasana} hari {hari_django}"
            , status=status.HTTP_404_NOT_FOUND)

        # buat user baru
        new_user = CustomUser.objects.create_user(
            username=username,
            password=password,
            role="peserta"
        )

        # buat peserta baru
        peserta = Peserta.objects.create(
            nama_peserta=nama,
            tanggal_lahir_peserta=tanggal_lahir,
            kendala_terapi=kendala or "",
            sasana=sasana,
            user=new_user
        )

        # simpan presensi
        presensi = Presensi.objects.create(
            peserta=peserta,
            sasana=sasana,
            jadwal=jadwal,
            tanggal=date.today(),
            waktu=now().time()
        )

        return Response({
            "status": "success",
            "message": f"Peserta {peserta.nama_peserta} berhasil ditambahkan & presensi tercatat",
            "data": {
                "id_peserta": str(peserta.id_peserta),
                "id_presensi": str(presensi.id_presensi),
                "sasana": sasana.nama_sasana,
                "tanggal": str(presensi.tanggal),
                "waktu": presensi.waktu.strftime("%H:%M:%S"),
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("ERROR presensi_manual:", e)
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
@login_required
def me_web(request):
    user = request.user
    context = {"user": user}

    # Tambahkan detail sesuai role
    if user.role == "peserta":
        try:
            peserta = Peserta.objects.get(user=user)
            context["detail"] = peserta
        except Peserta.DoesNotExist:
            context["detail"] = None

    elif user.role == "instruktur":
        try:
            instruktur = Instruktur.objects.get(user=user)
            context["detail"] = instruktur
        except Instruktur.DoesNotExist:
            context["detail"] = None

    elif user.role == "peraga":
        try:
            peraga = Peraga.objects.get(user=user)
            context["detail"] = peraga
        except Peraga.DoesNotExist:
            context["detail"] = None

    elif user.role == "pengurus_sasana":
        try:
            pengurus = PengurusSasana.objects.get(user=user)
            context["detail"] = pengurus
        except PengurusSasana.DoesNotExist:
            context["detail"] = None

    elif user.role == "pengurus_daerah":
        try:
            pengurus = PengurusDaerah.objects.get(user=user)
            context["detail"] = pengurus
        except PengurusDaerah.DoesNotExist:
            context["detail"] = None

    return render(request, "me.html", context)

# Register User
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # arahkan ke halaman login
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # redirect ke homepage
    return render(request, "login.html")

def custom_logout(request):
    logout(request)
    return redirect("login")

# Sasana
def create_sasana(request):
    if request.method == 'POST':
        form = SasanaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-sasana')
    else:
        form = SasanaForm()
    return render(request, 'sasana_form.html', {'form': form})

def list_sasana(request):
    data = Sasana.objects.all()
    return render(request, 'sasana_list.html', {'data': data})

# Di sini, 'id_sasana' harus cocok dengan nama parameter di urls.py
def detail_sasana(request, id_sasana):
    sasana = get_object_or_404(Sasana, id_sasana=id_sasana)
    return render(request, 'sasana_detail.html', {'sasana': sasana})

def update_sasana(request, id_sasana):
    sasana = get_object_or_404(Sasana, id_sasana=id_sasana)
    if request.method == 'POST':
        form = SasanaForm(request.POST, request.FILES, instance=sasana)
        if form.is_valid():
            form.save()
            return redirect('list-sasana')
    else:
        form = SasanaForm(instance=sasana)
    return render(request, 'sasana_form.html', {'form': form})

def delete_sasana(request, id_sasana):
    sasana = get_object_or_404(Sasana, id_sasana=id_sasana)
    if request.method == 'POST':
        sasana.delete()
        return redirect('list-sasana')
    return render(request, 'sasana_confirm_delete.html', {'sasana': sasana})


# Peserta
def create_peserta(request, sasana_id):
#    sasana_id = request.GET.get('sasana_id')
    sasana = get_object_or_404(Sasana, id_sasana=sasana_id)

    if request.method == 'POST':
        form = PesertaForm(request.POST)
        if form.is_valid():
            peserta = form.save(commit=False)
            peserta.sasana = sasana
            peserta.save()
            return redirect('list-peserta', sasana_id=sasana.id_sasana)
    else:
        form = PesertaForm()

    return render(request, 'peserta_form.html', {'form': form, 'sasana': sasana})

# List Peserta
def list_peserta(request, sasana_id):
    sasana = get_object_or_404(Sasana, id_sasana=sasana_id)
    data = Peserta.objects.filter(sasana=sasana)
    return render(request, 'peserta_list.html', {'data': data, 'sasana': sasana})

# Detail Peserta
# Detail Peserta
def detail_peserta(request, id_peserta):
    peserta = get_object_or_404(Peserta, id_peserta=id_peserta)

    qr_data = {
        "id_peserta": str(peserta.id_peserta),
        "nama_peserta": peserta.nama_peserta,
        "tanggal_lahir_peserta": str(peserta.tanggal_lahir_peserta),
        "id_sasana": str(peserta.sasana_id) if peserta.sasana else None
    }

    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(request, "peserta_detail.html", {
        "peserta": peserta,
        "qr_code": qr_base64
    })
    
# Download QR Peserta
# Download QR Peserta
def download_qr_peserta(request, id_peserta):
    peserta = get_object_or_404(Peserta, id_peserta=id_peserta)

    qr_data = {
        "id_peserta": str(peserta.id_peserta),
        "nama_peserta": peserta.nama_peserta,
        "tanggal_lahir_peserta": str(peserta.tanggal_lahir_peserta),
        "id_sasana": str(peserta.sasana_id) if peserta.sasana else None
    }

    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="qr_{peserta.nama_peserta}.png"'
    return response


# Edit Peserta
def update_peserta(request, id_peserta):
    peserta = get_object_or_404(Peserta, id_peserta=id_peserta)
    sasana = peserta.sasana

    if request.method == 'POST':
        form = PesertaForm(request.POST, instance=peserta)
        if form.is_valid():
            form.save()
            return redirect('list-peserta', sasana_id=sasana.id_sasana)
    else:
        form = PesertaForm(instance=peserta)
    return render(request, 'peserta_form.html', {'form': form, 'sasana': sasana, 'peserta': peserta})

# Delete Peserta
def delete_peserta(request, id_peserta):
    peserta = get_object_or_404(Peserta, id_peserta=id_peserta)
    if request.method == 'POST':
        peserta.delete()
        return redirect('list-peserta')
    return render(request, 'peserta_confirm_delete.html', {'peserta': peserta})


# Instruktur
def create_instruktur(request, sasana_id):
#    sasana_id = request.GET.get('sasana_id')
    sasana = get_object_or_404(Sasana, id_sasana=sasana_id)

    if request.method == 'POST':
        form = InstrukturForm(request.POST, request.FILES)  
        if form.is_valid():
            instruktur = form.save(commit=False)
            instruktur.sasana = sasana
            instruktur.save()
            return redirect('list-instruktur', sasana_id=sasana.id_sasana)
    else:
        form = InstrukturForm()

    return render(request, 'instruktur_form.html', {'form': form, 'sasana': sasana})

# List Instruktur
def list_instruktur(request, sasana_id):
    sasana = get_object_or_404(Sasana, id_sasana=sasana_id)
    data = Instruktur.objects.filter(sasana=sasana)
    return render(request, 'instruktur_list.html', {'data': data, 'sasana': sasana})

# Detail Instruktur
def detail_instruktur(request, id_instruktur):
    instruktur = get_object_or_404(Instruktur, id_instruktur=id_instruktur)
    return render(request, 'instruktur_detail.html', {'instruktur': instruktur})

# Edit Instruktur
def update_instruktur(request, id_instruktur):
    instruktur = get_object_or_404(Instruktur, id_instruktur=id_instruktur)
    sasana = instruktur.sasana

    if request.method == 'POST':
        form = InstrukturForm(request.POST, request.FILES, instance=instruktur)
        if form.is_valid():
            form.save()
            return redirect('list-instruktur', sasana_id=sasana.id_sasana)
    else:
        form = InstrukturForm(instance=instruktur)
    return render(request, 'instruktur_form.html', {'form': form, 'sasana': sasana, 'instruktur':instruktur})

# Delete Instruktur
def delete_instruktur(request, id_instruktur):
    instruktur = get_object_or_404(Instruktur, id_instruktur=id_instruktur)
    if request.method == 'POST':
        instruktur.delete()
        return redirect('list-instruktur')
    return render(request, 'instruktur_confirm_delete.html', {'instruktur': instruktur})

# Map weekday ke nama hari
DAY_NAME = {
    0: 'Senin',
    1: 'Selasa',
    2: 'Rabu',
    3: 'Kamis',
    4: 'Jumat',
    5: 'Sabtu',
    6: 'Minggu',
}

# Show Barcode
def show_barcode(request, sasana_id):
    sasana = get_object_or_404(Sasana, id_sasana=sasana_id)

    now = timezone.localtime()
    today_name = DAY_NAME[now.weekday()]
    current_time = now.time()

    jadwal = JadwalLatihan.objects.filter(
        sasana=sasana,
        hari=today_name,
        jam_latihan__gte=current_time
    ).order_by('jam_latihan').first()

    if not jadwal:
        return render(request, 'show_barcode.html', {
            'error': 'Tidak ada jadwal hari ini.',
            'sasana': sasana,
        })

    barcode_data = f"{sasana.id_sasana}_{jadwal.id_jadwal}_{now.date()}_{jadwal.jam_latihan}"

    qr = qrcode.make(barcode_data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    return render(request, 'show_barcode.html', {
        'sasana': sasana,
        'jadwal': jadwal,
        'tanggal_jadwal': now.date(),
        'barcode_base64': img_base64,
    })