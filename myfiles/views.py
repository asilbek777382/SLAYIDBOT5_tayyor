#
# from django.shortcuts import render
#
# # Create your views here.
#
#
# from myfiles.models import fan, kurs, Royxat
#
#
# def home(malumot):
#     return render(malumot,'index.html')
#
# def home_en(malumot):
#     return render(malumot,'index_en.html')
#
# def home_ru(malumot):
#     return render(malumot,'index_ru.html')
#
# def biz_haqimizda_en(malumot):
#     return render(malumot,'biz_haqimizda_en.html')
#
# def biz_haqimizda_ru(malumot):
#     return render(malumot,'biz_haqimizda_ru.html')
#
# def biz_haqimizda(malumot):
#     return render(malumot,'biz_haqimizda.html')
#
# def contact(malumot):
#     if malumot.method=="POST":
#         vaqt = malumot.POST.get('vaqt')
#         manzil = malumot.POST.get('manzil')
#         tel = malumot.POST.get('tel')
#         ism = malumot.POST.get('ism')
#         kurs = malumot.POST.get('kurs')
#         fans=fan.objects.get(fans=kurs)
#
#         Royxat(ism=ism,manzil=manzil,vaqt=vaqt,telefon=tel,kurs=fans).save()
#
#         return render(malumot, 'SINOV.html')
#
#
#     Fanlar=fan.objects.all()
#     return render(malumot,'contact.html',{'fanss':Fanlar})
#
# def contact_ru(malumot):
#     if malumot.method=="POST":
#         vaqt = malumot.POST.get('vaqt')
#         manzil = malumot.POST.get('manzil')
#         tel = malumot.POST.get('tel')
#         ism = malumot.POST.get('ism')
#         kurs = malumot.POST.get('kurs')
#         fans=fan.objects.get(fans=kurs)
#         Royxat(ism=ism,manzil=manzil,vaqt=vaqt,telefon=tel,kurs=fans).save()
#         return render(malumot, 'SINOV.html')
#     Fanlar=fan.objects.all()
#     return render(malumot,'contact_ru.html',{'fanss':Fanlar})
#
# def contact_en(malumot):
#     if malumot.method=="POST":
#         vaqt = malumot.POST.get('vaqt')
#         manzil = malumot.POST.get('manzil')
#         tel = malumot.POST.get('tel')
#         ism = malumot.POST.get('ism')
#         kurs = malumot.POST.get('kurs')
#         fans=fan.objects.get(fans=kurs)
#         Royxat(ism=ism,manzil=manzil,vaqt=vaqt,telefon=tel,kurs=fans).save()
#         return render(malumot, 'SINOV.html')
#     Fanlar=fan.objects.all()
#     return render(malumot,'contact_en.html',{'fanss':Fanlar})
#
#
# def kurslar(malumot):
#     return render(malumot,'kurslar.html')
#
# def kurslar_ru(malumot):
#     return render(malumot,'kurslar_ru.html')
#
# def kurslar_en(malumot):
#     return render(malumot,'kurslar_en.html')