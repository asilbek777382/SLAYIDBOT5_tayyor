from django.contrib import admin
from myfiles.models import *
# Register your models here.


class Adminobxavo(admin.ModelAdmin):
    list_display = ['id','tg_user','user_ismi','balans','til']

admin.site.register(User,Adminobxavo)

class AdminAdmin(admin.ModelAdmin):
    list_display = ['id','tg_user','username','ismi']

admin.site.register(Admin,AdminAdmin)


class Adminkanallar(admin.ModelAdmin):
    list_display = ['id','tg_user','username','ismi']

admin.site.register(kanallar,Adminkanallar)




class Adminsumma(admin.ModelAdmin):
    list_display = ['id','summa']

admin.site.register(summa,Adminsumma)




class Adminreferal(admin.ModelAdmin):
    list_display = ['id','user_id','referal_id','balance']

admin.site.register(Referal,Adminreferal)


class Adminshablon_kurs(admin.ModelAdmin):
    list_display = ['id','tg_id','institut','ism_fam','til','sahifa_soni','kurs_tili']

admin.site.register(shablon_kurs,Adminshablon_kurs)






class Adminshablon_pre(admin.ModelAdmin):
    list_display = ['id','tg_id','bg_num','ism_fam','til','slayid_soni','pre_tili']

admin.site.register(shablon_pre,Adminshablon_pre)




