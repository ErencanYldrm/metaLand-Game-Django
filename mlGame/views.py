import json
from django.shortcuts import render
import pytz
from mlGame.models import Kullanıcı, Oyun, Alan, Yöneticiİşletme, İşletme,  Satış, Çalışma
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone


def Giriş(request):
    if request.method == 'POST':
        kullanıcıAdı = request.POST['kullanıcıAdı']
        şifre = request.POST['şifre']
        kullanıcı = Kullanıcı.objects.filter(
            kullanıcıAdı=kullanıcıAdı, şifre=şifre)
        if kullanıcı:
            kullanıcı = kullanıcı[0]
            oyun = Oyun.objects.last()
            kullanıcı.oyun = oyun
            kullanıcı.save()
            zaman()
            if kullanıcı.yemekmiktarı <= 0 or kullanıcı.eşyamiktarı <= 0:
                return render(request, 'gameover.html')
            else:
                pk = kullanıcı.id
                url = reverse('Yükle', args=(pk,))
                return redirect(url)
        else:
            message = "Kullanıcı adı veya şifre yanlış"
            return render(request, 'login.html', {'message': message})
    return render(request, 'login.html')


def Kayıt(request):
    if request.method == 'POST':
        kullanıcıAdı = request.POST['kullanıcıAdı']
        ad = request.POST['ad']
        soyad = request.POST['soyad']
        şifre = request.POST['şifre']
        kullanıcı = Kullanıcı(kullanıcıAdı=kullanıcıAdı, ad=ad,
                              soyad=soyad, şifre=şifre)
        kullanıcı.yemekmiktarı = Oyun.objects.last().başlangıçYemekMiktarı
        kullanıcı.paramiktarı = Oyun.objects.last().başlangıçParaMiktarı
        kullanıcı.eşyamiktarı = Oyun.objects.last().başlangıçEşyaMiktarı
        kullanıcı.oyun = Oyun.objects.last()
        kullanıcı.save()
        return redirect('Giriş')
    return render(request, 'register.html')


def Yarat(request):
    if request.method == "POST":
        oyunAlanıX = request.POST['xUzunluk']
        oyunAlanıY = request.POST['yUzunluk']
        başlangıçEşya = request.POST['baslangicEsya']
        başlangıçYemek = request.POST['baslangicYiyecek']
        başlangıçPara = request.POST['baslangicPara']
        günlükYiyecekGideri = request.POST['yiyecekAzalma']
        günlükEşyaGideri = request.POST['esyaAzalma']
        günlükParaGideri = request.POST['paraAzalma']
        işletmeÜcreti = request.POST['İşletmeÜcreti']
        sabitGelir = request.POST['sabitGelir']
        sabitGelirOranı = request.POST['sabitGelirOran']
        çalışmaücreti = request.POST['çalışmaÜcreti']
        oyun = Oyun(oyunAlanBoyutuX=oyunAlanıX, oyunAlanBoyutuY=oyunAlanıY, başlangıçEşyaMiktarı=başlangıçEşya, başlangıçParaMiktarı=başlangıçPara, başlangıçYemekMiktarı=başlangıçYemek,
                    günlükEşyaGideri=günlükEşyaGideri, günlükParaGideri=günlükParaGideri, günlükYiyecekGideri=günlükYiyecekGideri, işletmeSabitGelirMiktarı=sabitGelir, işletmeSabitGelirOranı=sabitGelirOranı, İşletmeÜcreti=işletmeÜcreti, çalışmaÜcreti=çalışmaücreti)
        oyun.save()
        # global oyunGüncellenmeTarihi
        # oyunGüncellenmeTarihi = oyun.oyunBaşlangıçTarihi
        # oyunGüncellenmeTarihi = oyunGüncellenmeTarihi.replace(tzinfo=None)
        # oyunGüncellenmeTarihi = oyunGüncellenmeTarihi + timedelta(hours=3)
        # print(oyunGüncellenmeTarihi)
        # print("&&&&&&&&&&&&&&&&")
        Kullanıcılar = Kullanıcı.objects.all()

        for kullanıcı in Kullanıcılar:
            kullanıcı.yemekmiktarı = başlangıçYemek
            kullanıcı.paramiktarı = başlangıçPara
            kullanıcı.eşyamiktarı = başlangıçEşya
            kullanıcı.save()
        yöneticiYerleştir()
        return redirect("Giriş")
    return render(request, 'creategame.html')


def Yükle(request, pk):
    oyun = Oyun.objects.last()
    kullanıcı = Kullanıcı.objects.get(id=pk)
    global sonkullanıcı
    sonkullanıcı = kullanıcı
    if kullanıcı.yemekmiktarı <= 0 or kullanıcı.eşyamiktarı <= 0:
        return render(request, 'gameover.html')
    return render(request, 'loadgame.html', {'oyun': oyun, "x": oyun.oyunAlanBoyutuX, "y": oyun.oyunAlanBoyutuY, "başlangıçYemekMiktarı": oyun.başlangıçYemekMiktarı, "başlangıçEşyaMiktarı": oyun.başlangıçEşyaMiktarı,
                                             "başlangıçParaMiktarı": oyun.başlangıçParaMiktarı,
                                             "günlükYiyecekGideri": oyun.günlükYiyecekGideri, "günlükEşyaGideri": oyun.günlükEşyaGideri,
                                             "günlükParaGideri": oyun.günlükParaGideri, "işletmeSabitGelirMiktarı": oyun.işletmeSabitGelirMiktarı,
                                             "işletmeSabitGelirOranı": oyun.işletmeSabitGelirOranı, "İşletmeÜcreti": oyun.İşletmeÜcreti, "oyunBaşlangıçTarihi": oyun.oyunBaşlangıçTarihi, "kullanıcı": kullanıcı,
                                             "yiyecekMiktarı": kullanıcı.yemekmiktarı, "paraMiktarı": kullanıcı.paramiktarı, "eşyaMiktarı": kullanıcı.eşyamiktarı})


def alan_bilgisi(request):
    x = request.GET.get('x')
    y = request.GET.get('y')

    oyun = Oyun.objects.last()
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=oyun)
    alan_json = alan.to_json()
    print(JsonResponse({'alan': alan_json}))

    return JsonResponse({'alan': alan_json})


def ilerisar(request):
    ilavegün = int(request.POST.get("ilavegün"))
    zaman(ilavegün)
    oyun = Oyun.objects.last()
    işletmeler = Alan.objects.filter(alanTürü=1, oyun=oyun)
    oyuncular = Kullanıcı.objects.filter(oyun=oyun)
    return render(request, "yöneticipaneli.html", {'işletmeler': işletmeler, 'oyuncular': oyuncular, 'oyun': oyun, "ilavegün": ilavegün})


def zaman(ilavegün=0):
    oyun = Oyun.objects.last()
    oyunBaşlangıçTarihi = oyun.oyunBaşlangıçTarihi
    oyunBaşlangıçTarihi = oyunBaşlangıçTarihi.replace(tzinfo=None)
    oyunBaşlangıçTarihi = oyunBaşlangıçTarihi + timedelta(hours=3)
    print(oyunBaşlangıçTarihi)
    günSayısı = oyun.günSayısı
    zaman = datetime.now()
    zaman = zaman.replace(tzinfo=None)
    fark = zaman - oyunBaşlangıçTarihi
    fark = fark.days + ilavegün
    çalışmalar = Çalışma.objects.filter(
        oyun=oyun, çalışmaBitiş__gte=timezone.now())
    alanlar = Alan.objects.filter(oyun=oyun)
    if fark > günSayısı:
        x = fark - günSayısı
        kullanıcılar = Kullanıcı.objects.all()
        for çalışma in Çalışma.objects.filter(oyun=oyun):
            if çalışma.işletme != None:
                çalışma.işletme.işletmeÇalışanSayısı = 0
                çalışma.işletme.save()
            if çalışma.yöneticiİşletme != None:
                çalışma.yöneticiİşletme.işletmeÇalışanSayısı = 0
                çalışma.yöneticiİşletme.save()
        for çalışma in çalışmalar:
            if çalışma.işletme != None:
                çalışma.işletme.işletmeÇalışanSayısı += 1
                çalışma.işletme.save()
            if çalışma.yöneticiİşletme != None:
                çalışma.yöneticiİşletme.işletmeÇalışanSayısı += 1
                çalışma.yöneticiİşletme.save()
        for kullanıcı in kullanıcılar:
            kullanıcı.yemekmiktarı -= (oyun.günlükYiyecekGideri)*x
            kullanıcı.eşyamiktarı -= oyun.günlükEşyaGideri*x
            kullanıcı.paramiktarı -= oyun.günlükParaGideri*x
            kullanıcı.save()
        for alan in alanlar:
            if alan.alanTürü == 1 and alan.işletme != None:
                if alan.işletme.işletmeKapasitesi == alan.işletme.işletmeÇalışanSayısı and x >= 7:
                    alan.işletme.işletmeSeviyesi += 1
                    alan.işletme.işletmeKapasitesi *= 2
                    alan.işletme.save()
                alınacak = oyun.işletmeSabitGelirMiktarı *\
                    ((100+oyun.işletmeSabitGelirOranı *
                     (alan.işletme.işletmeSeviyesi-1))/100) * x
                alan.alanSahibi.paramiktarı += alınacak
                alan.alanSahibi.save()
        for çalışma in çalışmalar:
            if çalışma.işletme != None:
                işletme = çalışma.işletme
                çalışan = çalışma.çalışan
                işletmeGünlükÜcreti = işletme.çalışmaÜcreti
                çalışan.paramiktarı += işletmeGünlükÜcreti * x
                çalışan.save()
                if işletme.işletmeTürü == "Market":
                    çalışan.yemekmiktarı += (oyun.günlükYiyecekGideri)*x
                if işletme.işletmeTürü == "Mağaza":
                    çalışan.eşyamiktarı += oyun.günlükEşyaGideri*x
                if işletme.işletmeTürü == "Emlak":
                    çalışan.paramiktarı += oyun.günlükParaGideri*x
                çalışan.save()
            if çalışma.yöneticiİşletme != None:
                yöneticiİşletme = çalışma.yöneticiİşletme
                çalışan = çalışma.çalışan
                yöneticiGünlükÜcreti = oyun.çalışmaÜcreti
                çalışan.paramiktarı += yöneticiGünlükÜcreti * x
                if yöneticiİşletme.işletmeTürü == "Market":
                    çalışan.yemekmiktarı += (oyun.günlükYiyecekGideri)*x
                if yöneticiİşletme.işletmeTürü == "Mağaza":
                    çalışan.eşyamiktarı += oyun.günlükEşyaGideri*x
                if yöneticiİşletme.işletmeTürü == "Emlak":
                    çalışan.paramiktarı += oyun.günlükParaGideri*x
                çalışan.save()

        oyun.günSayısı += x

        oyun.save()
        print(oyun.günSayısı)
    else:
        pass


def yöneticiYerleştir():
    oyun = Oyun.objects.last()
    alan1 = Alan.objects.get(oyun=oyun, alanNoX=0, alanNoY=0)
    alan2 = Alan.objects.get(oyun=oyun, alanNoX=1, alanNoY=0)
    alan3 = Alan.objects.get(oyun=oyun, alanNoX=2, alanNoY=0)
    yİşletme1 = Yöneticiİşletme.objects.create(
        işletmeTürü="Market", işletmeÇalışanSayısı=999, ürünÜcreti=1, oyun=Oyun.objects.last())
    yİşletme2 = Yöneticiİşletme.objects.create(
        işletmeTürü="Mağaza", işletmeÇalışanSayısı=999, ürünÜcreti=1, oyun=Oyun.objects.last())
    yİşletme3 = Yöneticiİşletme.objects.create(
        işletmeTürü="Emlak", işletmeÇalışanSayısı=999, ürünÜcreti=1, oyun=Oyun.objects.last())
    alan1.yöneticiİşletme = yİşletme1
    alan2.yöneticiİşletme = yİşletme2
    alan3.yöneticiİşletme = yİşletme3
    alan1.alanTürü = 1
    alan2.alanTürü = 1
    alan3.alanTürü = 1
    alan1.save()
    alan2.save()
    alan3.save()


def yöneticiEmlak(request):
    oyun = Oyun.objects.last()
    kullanıcı = sonkullanıcı
    return render(request, 'yöneticiemlak.html', {'kullanıcı': kullanıcı.ad, "ücret": oyun.İşletmeÜcreti, "para": kullanıcı.paramiktarı})


def yöneticiMağaza(request):
    oyun = Oyun.objects.last()
    kullanıcı = sonkullanıcı
    mağaza = Yöneticiİşletme.objects.get(işletmeTürü="Mağaza", oyun=oyun)
    ücret = mağaza.ürünÜcreti
    return render(request, 'yöneticiMağaza.html', {'kullanıcı': kullanıcı, "ücret": ücret, "para": kullanıcı.paramiktarı})


def yöneticiMarket(request):
    oyun = Oyun.objects.last()
    kullanıcı = sonkullanıcı
    market = Yöneticiİşletme.objects.get(işletmeTürü="Market", oyun=oyun)
    ücret = market.ürünÜcreti
    return render(request, 'yöneticiMarket.html', {'kullanıcı': kullanıcı, "ücret": ücret, "para": kullanıcı.paramiktarı})


def yöneticiEmlakSatış(request):
    if request.method == "POST":
        x = request.POST.get('x')
        y = request.POST.get('y')
        oyun = Oyun.objects.last()
        kullanıcı = sonkullanıcı
        alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=oyun)
        if alan.alanSahibi is None and alan.yöneticiİşletme is None:
            alan.alanSahibi = kullanıcı
            alan.alanTürü = 0
            alan.save()
            kullanıcı.paramiktarı -= oyun.İşletmeÜcreti
            kullanıcı.save()
            pk = kullanıcı.id
            url = reverse('Yükle', args=(pk,))
            return redirect(url)
        else:
            return render(request, 'yöneticiemlak.html', {'kullanıcı': kullanıcı.ad, "ücret": oyun.İşletmeÜcreti, "hata": "Alan zaten satın alınmış"})


def yöneticiSatınAl(request):
    x = request.POST.get('x')
    y = request.POST.get('y')
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=Oyun.objects.last())
    kullanıcı = sonkullanıcı
    mağaza = Yöneticiİşletme.objects.get(
        işletmeTürü="Mağaza", oyun=Oyun.objects.last())
    ücret = mağaza.ürünÜcreti
    if kullanıcı.paramiktarı >= ücret:
        if alan.yöneticiİşletme.işletmeTürü == "Market":
            kullanıcı.yemekmiktarı += 1
            kullanıcı.paramiktarı -= ücret
            kullanıcı.save()
            return render(request, 'yöneticiMarket.html', {'kullanıcı': kullanıcı, "ücret": ücret, "para": kullanıcı.paramiktarı, "mesaj": "Ürün satın alındı"})
        elif alan.yöneticiİşletme.işletmeTürü == "Mağaza":
            kullanıcı.eşyamiktarı += 1
            kullanıcı.paramiktarı -= ücret
            kullanıcı.save()
            return render(request, 'yöneticiMağaza.html', {'kullanıcı': kullanıcı, "ücret": ücret, "para": kullanıcı.paramiktarı, "mesaj": "Ürün satın alındı"})
    else:
        if alan.yöneticiİşletme.işletmeTürü == "Market":
            return render(request, 'yöneticiMarket.html', {'kullanıcı': kullanıcı, "ücret": ücret, "para": kullanıcı.paramiktarı, "mesaj": "Yeterli paranız yok"})
        elif alan.yöneticiİşletme.işletmeTürü == "Mağaza":
            return render(request, 'yöneticiMağaza.html', {'kullanıcı': kullanıcı, "ücret": ücret, "para": kullanıcı.paramiktarı, "mesaj": "Yeterli paranız yok"})
    return render(request, 'yöneticiMarket.html', {'kullanıcı': kullanıcı, "ücret": ücret, "para": kullanıcı.paramiktarı, "mesaj": "Yeterli paranız yok"})


def işletmeKur(request):
    oyun = Oyun.objects.last()
    kullanıcı = sonkullanıcı
    arsalar = Alan.objects.filter(alanSahibi=kullanıcı, alanTürü=0, oyun=oyun)
    return render(request, 'işletmekur.html', {'kullanıcı': kullanıcı.ad, "para": kullanıcı.paramiktarı, "ücret": oyun.İşletmeÜcreti, "arsalar": arsalar})


def mağazaOnClick(request, arsa_id):
    arsa = Alan.objects.get(id=arsa_id)
    kullanıcı = sonkullanıcı
    oyun = Oyun.objects.last()
    if arsa.alanTürü == 0:
        if kullanıcı.paramiktarı >= oyun.İşletmeÜcreti:
            işletme = İşletme.objects.create(
                işletmeTürü='Mağaza', ürünÜcreti=1)
            arsa.işletme = işletme
            arsa.alanTürü = 1
            arsa.save()
            kullanıcı.paramiktarı -= oyun.İşletmeÜcreti
            kullanıcı.save()
            response_data = {"arsa": arsa.işletme.işletmeTürü}
            return JsonResponse(response_data)

    return JsonResponse({"arsa": "hata"})


def marketOnClick(request, arsa_id):
    arsa = Alan.objects.get(id=arsa_id)
    kullanıcı = sonkullanıcı
    oyun = Oyun.objects.last()
    if arsa.alanTürü == 0:
        if kullanıcı.paramiktarı >= oyun.İşletmeÜcreti:
            işletme = İşletme.objects.create(
                işletmeTürü='Market', ürünÜcreti=1)
            arsa.işletme = işletme
            arsa.alanTürü = 1
            arsa.save()
            kullanıcı.paramiktarı -= oyun.İşletmeÜcreti
            kullanıcı.save()
            response_data = {"arsa": arsa.işletme.işletmeTürü}
            return JsonResponse(response_data)

    return JsonResponse({"arsa": "hata"})


def emlakOnClick(request, arsa_id):
    arsa = Alan.objects.get(id=arsa_id)
    kullanıcı = sonkullanıcı
    oyun = Oyun.objects.last()
    if arsa.alanTürü == 0:
        if kullanıcı.paramiktarı >= oyun.İşletmeÜcreti:
            işletme = İşletme.objects.create(işletmeTürü='Emlak', ürünÜcreti=1)
            arsa.işletme = işletme
            arsa.alanTürü = 1
            arsa.save()
            kullanıcı.paramiktarı -= oyun.İşletmeÜcreti
            kullanıcı.save()
            response_data = {"arsa": arsa.işletme.işletmeTürü}
            return JsonResponse(response_data)

    return JsonResponse({"arsa": "hata"})


def alanGönder(request):
    x = request.POST.get('x')
    y = request.POST.get('y')

    print(x, y)
    oyun = Oyun.objects.last()
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=oyun)
    return render(request, 'iş.html', {'alan': alan.alanNoX})


def işlem(request):
    x = request.POST.get('x')
    y = request.POST.get('y')
    oyun = Oyun.objects.last()
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=oyun)
    kullanıcı = sonkullanıcı
    sahip = alan.alanSahibi
    if kullanıcı == sahip:
        alanlar = Alan.objects.filter(
            alanSahibi=kullanıcı, alanTürü=1, oyun=oyun)
        return render(request, 'panel.html', {'kullanıcı': kullanıcı, "alanlar": alanlar})

    if alan.işletme is not None:
        if alan.işletme.işletmeTürü == 'Mağaza':
            return render(request, 'mağaza.html', {'alan': alan, 'eşya': sonkullanıcı.eşyamiktarı, "sahipeşya": alan.alanSahibi.eşyamiktarı})
        elif alan.işletme.işletmeTürü == 'Market':
            return render(request, 'market.html', {'alan': alan, "yiyecek": sonkullanıcı.yemekmiktarı, 'kullanıcı': sonkullanıcı, "sahipyemek": alan.alanSahibi.yemekmiktarı})
        elif alan.işletme.işletmeTürü == 'Emlak':
            return render(request, 'emlak.html', {'alan': alan, 'kullanıcı': sonkullanıcı})
    pk = sonkullanıcı.id
    url = reverse('Yükle', args=(pk,))
    return redirect(url)


def satınAl(request):
    x = request.POST.get('x')
    y = request.POST.get('y')
    print(x, y)
    oyun = Oyun.objects.last()
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=oyun)
    Kullanıcı = sonkullanıcı
    sahip = alan.alanSahibi

    if Kullanıcı.paramiktarı >= alan.işletme.ürünÜcreti:
        Kullanıcı.paramiktarı -= alan.işletme.ürünÜcreti
        if alan.işletme.işletmeTürü == 'Mağaza' and sahip.eşyamiktarı > 0:
            Kullanıcı.eşyamiktarı += 1
            sahip.eşyamiktarı -= 1
        elif alan.işletme.işletmeTürü == 'Market' and sahip.yemekmiktarı > 0:
            Kullanıcı.yemekmiktarı += 1
            sahip.yemekmiktarı -= 1
        else:
            return render(request, "stokbitti.html")
        Kullanıcı.save()
        sahip.paramiktarı += alan.işletme.ürünÜcreti
        sahip.save()
        if alan.işletme.işletmeTürü == 'Mağaza':
            return render(request, "mağaza.html", {"mesaj": "Satın Alındı", "alan": alan, "eşya": Kullanıcı.eşyamiktarı, "sahipeşya": alan.alanSahibi.eşyamiktarı})
        elif alan.işletme.işletmeTürü == 'Market':
            return render(request, "market.html", {"mesaj": "Satın Alındı", "alan": alan, "yiyecek": Kullanıcı.yemekmiktarı, "sahipyemek": alan.alanSahibi.yemekmiktarı})
    else:
        if alan.işletme.işletmeTürü == 'Mağaza':
            return render(request, "mağaza.html", {"mesaj": "Bakiye yetersiz", "alan": alan,
                                                   "eşya": Kullanıcı.eşyamiktarı, "sahipeşya": alan.alanSahibi.eşyamiktarı})
        elif alan.işletme.işletmeTürü == 'Market':
            return render(request, "market.html", {"mesaj": "Bakiye yetersiz", "alan": alan, "yiyecek": Kullanıcı.yemekmiktarı, "sahipyemek": alan.alanSahibi.yemekmiktarı})


def güncelle(request):
    x = request.POST.get('alanX')
    y = request.POST.get('alanY')
    oyun = Oyun.objects.last()
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=oyun)
    kullanıcı = sonkullanıcı
    ücret = request.POST.get('ürünÜcreti')
    print(ücret)
    alan.işletme.ürünÜcreti = ücret
    alan.işletme.save()
    alanlar = Alan.objects.filter(alanSahibi=kullanıcı, alanTürü=1, oyun=oyun)
    return render(request, "panel.html", {"mesaj": "Güncellendi", "ücret": ücret, "alanlar": alanlar, "kullanıcı": kullanıcı})


def işletmeSat(request):
    alanlar = Alan.objects.filter(
        alanSahibi=sonkullanıcı, alanTürü=1, oyun=Oyun.objects.last())
    x = request.POST.get('x')
    y = request.POST.get('y')
    return render(request, "işletmesat.html", {"kullanıcı": sonkullanıcı, "alanlar": alanlar, "emlakx": x, "emlaky": y})


def emlakçıyaver(request):
    emlakx = request.POST.get('emlakx')
    emlaky = request.POST.get('emlaky')
    ücret = request.POST.get('ücret')
    x = request.POST.get('x')
    y = request.POST.get('y')
    oyun = Oyun.objects.last()
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=oyun)
    emlak = Alan.objects.get(alanNoX=emlakx, alanNoY=emlaky, oyun=oyun)
    kullanıcı = sonkullanıcı
    alan.işletme.işletmeSatışFiyatı = ücret
    emlak.işletme.emlakİşletmeler.add(alan)
    emlak.işletme.save()
    alan.işletme.save()
    alanlar = Alan.objects.filter(alanSahibi=kullanıcı, alanTürü=1, oyun=oyun)
    return render(request, "işletmesat.html", {"kullanıcı": sonkullanıcı, "alanlar": alanlar, "emlakx": x, "emlaky": y, "mesaj": "Emlakçıya Verildi"})


def işletmeSatınAl(request):
    emlakx = request.POST.get('emlakx')
    emlaky = request.POST.get('emlaky')
    x = request.POST.get('x')
    y = request.POST.get('y')
    oyun = Oyun.objects.last()
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=oyun)
    alansahibi = alan.alanSahibi
    emlak = Alan.objects.get(alanNoX=emlakx, alanNoY=emlaky, oyun=oyun)
    kullanıcı = sonkullanıcı
    satışÜcreti = alan.işletme.işletmeSatışFiyatı + emlak.işletme.ürünÜcreti
    if kullanıcı.paramiktarı >= satışÜcreti:
        Satış.objects.create(
            alan=alan, satılanKişi=kullanıcı, satanKişi=alansahibi)
        alan.alanSahibi.paramiktarı += alan.işletme.işletmeSatışFiyatı
        alan.alanSahibi.save()
        kullanıcı.paramiktarı -= satışÜcreti
        kullanıcı.save()
        emlak.alanSahibi.paramiktarı += emlak.işletme.ürünÜcreti
        emlak.alanSahibi.save()
        alan.alanSahibi = kullanıcı
        emlak.işletme.emlakİşletmeler.remove(alan)
        emlak.işletme.save()
        kullanıcı.save()
        alan.işletme.save()
        alan.save()
        alanlar = Alan.objects.filter(
            alanSahibi=kullanıcı, alanTürü=1, oyun=oyun)
        return render(request, "emlak.html", {"kullanıcı": sonkullanıcı, "alanlar": alanlar, "emlakx": x, "emlaky": y, "mesaj": "Satın Alındı"})
    return render(request, "emlak.html", {"kullanıcı": sonkullanıcı, "alan": emlak, "mesaj": "Bakiye Yetersiz"})


def çalışmaücreti(request):
    x = request.POST.get('x')
    y = request.POST.get('y')
    çalışmaücreti = request.POST.get('çalışmaÜcreti')
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=Oyun.objects.last())
    alan.işletme.çalışmaÜcreti = çalışmaücreti
    alan.işletme.save()
    alanlar = Alan.objects.filter(
        alanSahibi=sonkullanıcı, alanTürü=1, oyun=Oyun.objects.last())
    return render(request, "panel.html", {"mesaj": "Çalışma Ücreti Güncellendi", "alanlar": alanlar, "kullanıcı": sonkullanıcı})


def çalışma(request):
    x = request.POST.get('x')
    y = request.POST.get('y')
    print(x, y)
    günsayısı = request.POST.get('günsayısı')
    gün = int(günsayısı)
    alan = Alan.objects.get(alanNoX=x, alanNoY=y, oyun=Oyun.objects.last())
    kullanıcı = sonkullanıcı
    alanlar = Alan.objects.filter(
        alanSahibi=sonkullanıcı, alanTürü=1, oyun=Oyun.objects.last())
    çalışmalar = Çalışma.objects.filter(
        çalışan=kullanıcı, oyun=Oyun.objects.last(),  çalışmaBitiş__gte=timezone.now())
    if çalışmalar.count() == 0:
        if alan.yöneticiİşletme != None:
            Çalışma.objects.create(çalışan=kullanıcı, yöneticiİşletme=alan.yöneticiİşletme,
                                   oyun=Oyun.objects.last(), çalışmaGünSayısı=gün)
            alan.yöneticiİşletme.işletmeÇalışanSayısı += 1
            alan.yöneticiİşletme.save()
            return render(request, 'emlak.html', {'alan': alan, 'kullanıcı': sonkullanıcı, 'mesaj': 'Çalışmaya Başladınız'})
        else:
            Çalışma.objects.create(çalışan=kullanıcı, işletme=alan.işletme,
                                   oyun=Oyun.objects.last(), çalışmaGünSayısı=gün)
            alan.işletme.işletmeÇalışanSayısı += 1
            alan.işletme.save()
            alanlar = Alan.objects.filter(
                alanSahibi=sonkullanıcı, alanTürü=1, oyun=Oyun.objects.last())
            return render(request, 'emlak.html', {'alan': alan, 'kullanıcı': sonkullanıcı, 'mesaj': 'Çalışmaya Başladınız'})

    return render(request, 'emlak.html', {'alan': alan, 'kullanıcı': sonkullanıcı, 'mesaj': 'Zaten Çalışıyorsunuz'})


def geçmişişlemler(request):
    kullanıcı = sonkullanıcı
    sattıkları = Satış.objects.filter(
        satanKişi=kullanıcı, oyun=Oyun.objects.last())
    aldıkları = Satış.objects.filter(
        satılanKişi=kullanıcı, oyun=Oyun.objects.last())
    çalışmalar = Çalışma.objects.filter(
        çalışan=kullanıcı, oyun=Oyun.objects.last())
    alanlar = Alan.objects.filter(
        alanSahibi=kullanıcı, oyun=Oyun.objects.last())
    işletmeler = Alan.objects.filter(
        alanTürü=1, alanSahibi=kullanıcı, oyun=Oyun.objects.last())
    return render(request, "geçmişişlemler.html", {'kullanıcı': kullanıcı, "işletmeler": işletmeler, 'satışlar': sattıkları, "alışlar": aldıkları, 'çalışmalar': çalışmalar, 'alanlar': alanlar})


def yöneticiPaneli(request):
    oyun = Oyun.objects.last()
    işletmeler = Alan.objects.filter(alanTürü=1, oyun=oyun)
    oyuncular = Kullanıcı.objects.filter(oyun=oyun)

    return render(request, "yöneticipaneli.html", {'işletmeler': işletmeler, 'oyuncular': oyuncular, 'oyun': oyun})


def oyunGüncelle(request):
    oyun = Oyun.objects.last()
    günlükyiyecekgideri = request.POST.get('günlükyiyecekgideri')
    günlükeşyagideri = request.POST.get('günlükeşyagideri')
    günlükparagideri = request.POST.get('günlükparagideri')
    isletmeucreti = request.POST.get('isletmeucreti')
    isletmesabitgelirmiktari = request.POST.get('isletmesabitgelirmiktari')
    isletmesabitgelirorani = request.POST.get('isletmesabitgelirorani')
    çalışmaücreti = request.POST.get('çalışmaÜcreti')

    oyun.günlükYiyecekGideri = günlükyiyecekgideri
    oyun.günlükEşyaGideri = günlükeşyagideri
    oyun.günlükParaGideri = günlükparagideri
    oyun.İşletmeÜcreti = isletmeucreti
    oyun.işletmeSabitGelirMiktarı = isletmesabitgelirmiktari
    oyun.işletmeSabitGelirOranı = isletmesabitgelirorani
    oyun.çalışmaÜcreti = çalışmaücreti

    oyun.save()

    return redirect('yöneticiPaneli')
