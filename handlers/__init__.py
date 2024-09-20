from aiogram import Router

from .main import router as main_router
from .admin_bl import router as admin_bl_router
from .admin_wl import router as admin_wl_router
from .admin_blwn import router as admin_blwn_router

router = Router()

router.include_router(main_router)
router.include_router(admin_bl_router)
router.include_router(admin_wl_router)
router.include_router(admin_blwn_router)
