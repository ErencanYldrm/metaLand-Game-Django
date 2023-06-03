# Generated by Django 4.1.7 on 2023-05-16 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='İşletme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('işletmeTürü', models.CharField(choices=[('Mağaza', 'Mağaza'), ('Market', 'Market')], max_length=50)),
                ('işletmeSeviyesi', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)])),
                ('işletmeKapasitesi', models.IntegerField(default=3)),
                ('işletmeÇalışanSayısı', models.IntegerField(default=0)),
                ('ürünÜcreti', models.IntegerField()),
                ('mevcutSeviyeBaşlangıçTarihi', models.DateTimeField()),
                ('işletmeSatışFiyatı', models.IntegerField()),
                ('işletmeKiralamaFiyatı', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Kullanıcı',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kullanıcıAdı', models.CharField(max_length=50)),
                ('ad', models.CharField(max_length=50)),
                ('soyad', models.CharField(max_length=50)),
                ('şifre', models.CharField(max_length=50)),
                ('yemekmiktarı', models.IntegerField(default=10)),
                ('eşyamiktarı', models.IntegerField(default=10)),
                ('paramiktarı', models.IntegerField(default=10)),
            ],
            options={
                'db_table': 'Kullanıcı',
            },
        ),
        migrations.CreateModel(
            name='Oyun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('başlangıçYemekMiktarı', models.IntegerField()),
                ('başlangıçEşyaMiktarı', models.IntegerField()),
                ('başlangıçParaMiktarı', models.IntegerField()),
                ('oyunBaşlangıçTarihi', models.DateTimeField(auto_now_add=True)),
                ('oyunAlanBoyutuX', models.IntegerField(default=3)),
                ('oyunAlanBoyutuY', models.IntegerField(default=3)),
                ('günlükYiyecekGideri', models.IntegerField()),
                ('günlükEşyaGideri', models.IntegerField()),
                ('günlükParaGideri', models.IntegerField()),
                ('İşletmeÜcreti', models.IntegerField()),
                ('işletmeSabitGelirMiktarı', models.IntegerField(default=10)),
                ('işletmeSabitGelirOranı', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Yöneticiİşletme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('işletmeTürü', models.CharField(choices=[('Mağaza', 'Mağaza'), ('Market', 'Market'), ('Emlak', 'Emlak')], max_length=50)),
                ('işletmeÇalışanSayısı', models.IntegerField(default=0)),
                ('ürünÜcreti', models.IntegerField()),
            ],
            options={
                'db_table': 'Yöneticiİşletme',
            },
        ),
        migrations.CreateModel(
            name='Çalışma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('çalışmaBaşlangıç', models.DateTimeField(auto_now_add=True)),
                ('çalışmaBitiş', models.DateTimeField()),
                ('çalışmaGünSayısı', models.IntegerField()),
                ('çalışmaSaatleri', models.IntegerField()),
                ('işletme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlGame.i̇şletme')),
                ('çalışan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlGame.kullanıcı')),
            ],
        ),
        migrations.CreateModel(
            name='Satış',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satışTarihi', models.DateTimeField(auto_now_add=True)),
                ('işletme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlGame.i̇şletme')),
                ('satılanKişi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlGame.kullanıcı')),
            ],
        ),
        migrations.CreateModel(
            name='Kiralama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kiralamaBaşlangıç', models.DateTimeField(auto_now_add=True)),
                ('kiralamaBitiş', models.DateTimeField()),
                ('kiraSüresi', models.IntegerField()),
                ('işletme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlGame.i̇şletme')),
                ('kiralayanKişi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlGame.kullanıcı')),
            ],
        ),
        migrations.AddField(
            model_name='i̇şletme',
            name='işletmeSahibi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlGame.kullanıcı'),
        ),
        migrations.CreateModel(
            name='Emlak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('işletmeSeviyesi', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)])),
                ('işletmeKapasitesi', models.IntegerField(default=3)),
                ('işletmeÇalışanSayısı', models.IntegerField(default=0)),
                ('emlakKomisyonu', models.IntegerField()),
                ('mevcutSeviyeBaşlangıçTarihi', models.DateTimeField()),
                ('işletmeSatışFiyatı', models.IntegerField()),
                ('işletmeKiralamaFiyatı', models.IntegerField()),
                ('işletmeSahibi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlGame.kullanıcı')),
            ],
        ),
        migrations.CreateModel(
            name='Alan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alanNo', models.IntegerField()),
                ('alanTürü', models.BooleanField()),
                ('alanSahibi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mlGame.kullanıcı')),
            ],
            options={
                'db_table': 'Alan',
            },
        ),
    ]
