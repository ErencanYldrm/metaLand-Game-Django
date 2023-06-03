from datetime import timedelta
import json
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

# Create your models here.


class Oyun(models.Model):
    başlangıçYemekMiktarı = models.IntegerField()
    başlangıçEşyaMiktarı = models.IntegerField()
    başlangıçParaMiktarı = models.IntegerField()
    oyunBaşlangıçTarihi = models.DateTimeField(auto_now_add=True)
    günSayısı = models.IntegerField(default=0)
    oyunAlanBoyutuX = models.IntegerField(default=3)
    oyunAlanBoyutuY = models.IntegerField(default=3)
    günlükYiyecekGideri = models.IntegerField()
    günlükEşyaGideri = models.IntegerField()
    günlükParaGideri = models.IntegerField()
    İşletmeÜcreti = models.IntegerField()
    işletmeSabitGelirMiktarı = models.IntegerField(default=10)
    işletmeSabitGelirOranı = models.IntegerField(default=10)
    çalışmaÜcreti = models.IntegerField(default=1)
    grid = models.TextField(default="")

    def __str__(self):
        return self.oyunBaşlangıçTarihi

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

            grid = []
            for y in range(int(self.oyunAlanBoyutuY)):
                row = []
                for x in range(int(self.oyunAlanBoyutuX)):
                    alan = Alan(oyun=self, alanNoX=x, alanNoY=y)
                    alan.save()
                    row.append(alan.pk)
                grid.append(row)
            self.grid = json.dumps(grid)

        super().save(*args, **kwargs)

    class Meta:
        db_table = "MLOyun"


class Kullanıcı(models.Model):
    kullanıcıAdı = models.CharField(max_length=50)
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    şifre = models.CharField(max_length=50)
    yemekmiktarı = models.IntegerField(default=10)
    eşyamiktarı = models.IntegerField(default=10)
    paramiktarı = models.IntegerField(default=10)
    oyun = models.ForeignKey(Oyun, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.kullanıcıAdı

    def to_json(self):
        return {
            'kullanıcıAdı': self.kullanıcıAdı,
            'ad': self.ad,
            'soyad': self.soyad,
            'şifre': self.şifre,
            'yemekmiktarı': self.yemekmiktarı,
            'eşyamiktarı': self.eşyamiktarı,
            'paramiktarı': self.paramiktarı,
            "oyun": self.oyun.pk
        }

    class Meta:
        db_table = "MLKullanıcı"


class İşletme(models.Model):
    işletme = [("Mağaza", "Mağaza"), ("Market", "Market"), ("Emlak", "Emlak")]
    seviyeler = [(1, 1), (2, 2), (3, 3)]
    işletmeTürü = models.CharField(max_length=50, choices=işletme)
    işletmeSeviyesi = models.IntegerField(choices=seviyeler, default=1)
    işletmeKapasitesi = models.IntegerField(default=3)
    işletmeÇalışanSayısı = models.IntegerField(default=0)
    # emlak ise satış başı alınacak komisyon
    ürünÜcreti = models.IntegerField(default=1)
    mevcutSeviyeBaşlangıçTarihi = models.DateTimeField(auto_now_add=True)
    işletmeSatışFiyatı = models.IntegerField(null=True)
    emlakİşletmeler = models.ManyToManyField(
        'Alan', blank=True, related_name='satılacakİşletmeler')
    çalışmaÜcreti = models.IntegerField(default=1)

    def to_json(self):
        json_data = {
            "işletmeTürü": self.işletmeTürü,
            "işletmeSeviyesi": self.işletmeSeviyesi,
            "işletmeKapasitesi": self.işletmeKapasitesi,
            "işletmeÇalışanSayısı": self.işletmeÇalışanSayısı,
            "ürünÜcreti": self.ürünÜcreti,
            "işletmeSatışFiyatı": self.işletmeSatışFiyatı,
            "çalışmaÜcreti": self.çalışmaÜcreti,
        }

    def __str__(self):
        return self.işletmeTürü

    class Meta:
        db_table = "MLİşletme"


class Yöneticiİşletme(models.Model):
    işletme = [("Mağaza", "Mağaza"), ("Market", "Market"), ("Emlak", "Emlak")]
    işletmeTürü = models.CharField(max_length=50, choices=işletme)
    işletmeÇalışanSayısı = models.IntegerField(default=0)
    # market yiyecek , mağaza ürün ücreti
    ürünÜcreti = models.IntegerField()
    oyun = models.ForeignKey(Oyun, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.işletmeTürü

    class Meta:
        db_table = "MLYöneticiİşletme"


class Alan(models.Model):
    alanNoX = models.IntegerField(default=0)
    alanNoY = models.IntegerField(default=0)
    # 0 arsa 1 işletme
    alanTürü = models.IntegerField(default=0)
    oyun = models.ForeignKey(Oyun, on_delete=models.CASCADE, null=True)
    alanSahibi = models.ForeignKey(
        Kullanıcı, on_delete=models.CASCADE, null=True)
    işletme = models.ForeignKey(İşletme, on_delete=models.CASCADE, null=True)
    yöneticiİşletme = models.ForeignKey(
        Yöneticiİşletme, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Alan:" + str(self.alanNoX) + "," + str(self.alanNoY)

    def to_json(self):
        json_data = {
            "alanNoX": self.alanNoX,
            "alanNoY": self.alanNoY,
            "alanTürü": self.alanTürü,
        }

        if self.yöneticiİşletme:
            json_data["yöneticiİşletme"] = {
                "işletmeTürü": self.yöneticiİşletme.işletmeTürü,
                "işletmeÇalışanSayısı": self.yöneticiİşletme.işletmeÇalışanSayısı,
                "ürünÜcreti": self.yöneticiİşletme.ürünÜcreti,
            }
        if self.alanSahibi:
            json_data["alanSahibi"] = {
                "kullanıcıAdı": self.alanSahibi.kullanıcıAdı,
                "ad": self.alanSahibi.ad,
                "soyad": self.alanSahibi.soyad,
                "şifre": self.alanSahibi.şifre,
                "yemekmiktarı": self.alanSahibi.yemekmiktarı,
                "eşyamiktarı": self.alanSahibi.eşyamiktarı,
                "paramiktarı": self.alanSahibi.paramiktarı,
            }

        if self.işletme:
            json_data["işletme"] = {
                "işletmeTürü": self.işletme.işletmeTürü,
                "işletmeSeviyesi": self.işletme.işletmeSeviyesi,
                "işletmeKapasitesi": self.işletme.işletmeKapasitesi,
                "işletmeÇalışanSayısı": self.işletme.işletmeÇalışanSayısı,
                "ürünÜcreti": self.işletme.ürünÜcreti,
                "işletmeSatışFiyatı": self.işletme.işletmeSatışFiyatı,
                "çalışmaÜcreti": self.işletme.çalışmaÜcreti,
            }

        return json_data

    class Meta:
        db_table = "MLAlan"


class Satış(models.Model):
    alan = models.ForeignKey(Alan, on_delete=models.CASCADE, null=True)
    satılanKişi = models.ForeignKey(
        Kullanıcı, on_delete=models.CASCADE, related_name="satılanKişi")
    satanKişi = models.ForeignKey(
        Kullanıcı, on_delete=models.CASCADE, related_name="satanKişi", null=True)
    satışTarihi = models.DateTimeField(auto_now_add=True)
    oyun = models.ForeignKey(Oyun, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "MLSatış"


class Çalışma(models.Model):
    çalışan = models.ForeignKey(Kullanıcı, on_delete=models.CASCADE)
    işletme = models.ForeignKey(İşletme, on_delete=models.CASCADE, null=True)
    yöneticiİşletme = models.ForeignKey(
        Yöneticiİşletme, on_delete=models.CASCADE, null=True)
    çalışmaBaşlangıç = models.DateTimeField(auto_now_add=True)
    çalışmaBitiş = models.DateTimeField()
    çalışmaGünSayısı = models.IntegerField()
    oyun = models.ForeignKey(Oyun, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Çalışma : " + str(self.çalışmaGünSayısı) + "gün " + str(self.işletme)

    class Meta:
        db_table = "MLÇalışma"

    def save(self, *args, **kwargs):
        if not self.id:
            if self.çalışmaBaşlangıç is None:
                self.çalışmaBaşlangıç = timezone.now()
            self.çalışmaBitiş = self.çalışmaBaşlangıç + \
                timedelta(days=self.çalışmaGünSayısı)
        super().save(*args, **kwargs)
