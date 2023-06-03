from django.contrib import admin
from .models import Kullanıcı, Oyun, Alan, Yöneticiİşletme, İşletme, Satış, Çalışma

# Register your models here.
admin.site.register(Kullanıcı)
admin.site.register(Oyun)
admin.site.register(Alan)
admin.site.register(Yöneticiİşletme)
admin.site.register(İşletme)
admin.site.register(Satış)
admin.site.register(Çalışma)
