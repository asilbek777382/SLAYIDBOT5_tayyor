from aiogram import Router

# Import qilinadigan fayllar:
from . import help
from . import referat_en
from . import admin_tanlov
from . import majburiy_azolik
from . import start
from . import echo
from . import referat  # yangi qo‘shilgan fayl
from . import presentatsiya
from . import buyruqlar
from . import kurs_ishi
from . import bot_tolov
from . import settings
from . import settings_en
from . import settings_ru
from . import presentatsiya_ru
from . import presentatsiya_en
from . import kurs_ishi_en
from . import kurs_ishi_ru
from . import referal
from . import referat_ru
from . import presentatsiya_shablon
from . import presentatsiya_shablon_en
from . import presentatsiya_shablon_ru
from . import referat_shablon_uz
from . import referat_shablon_ru
from . import referat_shablon_en
from . import kurs_ishi_shablon
router = Router()

# Barcha routerlarni ulaymiz:
router.include_router(kurs_ishi_shablon.router)
router.include_router(referat_shablon_ru.router)
router.include_router(referat_shablon_en.router)
router.include_router(presentatsiya_shablon_en.router)
router.include_router(referal.router)
router.include_router(referat_shablon_uz.router)
router.include_router(kurs_ishi_ru.router)
router.include_router(kurs_ishi_en.router)
router.include_router(referat_en.router)
router.include_router(referat_ru.router)


router.include_router(presentatsiya_en.router)
router.include_router(settings_en.router)
router.include_router(settings_ru.router)
router.include_router(presentatsiya_ru.router)
router.include_router(presentatsiya_shablon.router)

router.include_router(presentatsiya_shablon_ru.router)

router.include_router(help.router)
router.include_router(admin_tanlov.router)
router.include_router(majburiy_azolik.router)
router.include_router(start.router)
router.include_router(presentatsiya.router)
router.include_router(referat.router)  # yangi qo‘shilgan router
router.include_router(buyruqlar.router)
router.include_router(bot_tolov.router)
router.include_router(kurs_ishi.router)
router.include_router(settings.router)

