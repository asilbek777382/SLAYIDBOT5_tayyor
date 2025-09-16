from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    admin_tanlov= State()
    bot_azolariga_xabar_yuborish = State()
    forward_xabar_yuborish = State()
    guruxlarga_xabar_yuborish = State()
    bitta_azoga_xabar_yuborish = State()
    admin_sozlamalari = State()
    balansmajburiy_azolik = State()
    kanallar_tanlov= State()





class admin_sozlamalari(StatesGroup):
    admin_royxati= State()
    admin_sozlamalari = State()
    admin_qoshish = State()
    admin_manzil_olish= State()
    admin_ismi_olish= State()
    admin_ochirish = State()




class kanallar_sozlamalari(StatesGroup):
    kanallar_royxati= State()
    kanallar_sozlamalari = State()
    kanallar_qoshish = State()
    kanallar_manzil_olish= State()
    kanallar_ismi_olish= State()
    kanallar_ochirish = State()



class bot_azolariga_xabar_yuborish(StatesGroup):
    bot_azolariga_xabar_yuborish = State()
    bot_azolariga_xabar_yuborish_xabarni_olish = State()



class guruxlarga_xabar_yuborish(StatesGroup):
    guruxlarga_xabar_yuborish=State()
    guruxlarga_xabar_yuborish_xabarni_olish=State()


class bitta_azoga_xabar_yuborish(StatesGroup):
    bitta_azoga_xabar_yuborish=State()
    bitta_azoga_xabar_yuborish=State()
    bitta_azoga_xabar_yuborish_oluvchi=State()

class statistika(StatesGroup):
    statistika = State()