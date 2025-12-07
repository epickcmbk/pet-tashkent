"""
keyboards.py - Barcha keyboard va tugmalari
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import ANIMAL_TYPES, VET_SERVICES, PET_COURSES, CONTACT_INFO
from database import db

# =================== OUTLINE KEYBOARDS (Reply Keyboards) ===================

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy menyyu"""
    keyboard = [
        [KeyboardButton(text="🐾 Pet Xizmatlar"), KeyboardButton(text="🏥 Klinikalar")],
        [KeyboardButton(text="✂️ Grooming"), KeyboardButton(text="🏨 Pet Hotel")],
        [KeyboardButton(text="📞 Bog'lanish"), KeyboardButton(text="ℹ️ Ma'lumot")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def main_menu_with_extra_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy menyyu qo'shimcha xizmatlar bilan"""
    keyboard = [
        [KeyboardButton(text="🐾 Pet Xizmatlar"), KeyboardButton(text="🏥 Klinikalar")],
        [KeyboardButton(text="✂️ Grooming"), KeyboardButton(text="🎓 Pet Oqitish")],
        [KeyboardButton(text="🏨 Pet Hotel"), KeyboardButton(text="🐕 Hayvon Sotish")],
        [KeyboardButton(text="👶 Asrab Turish"), KeyboardButton(text="📞 Bog'lanish")],
        [KeyboardButton(text="ℹ️ Ma'lumot")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def admin_menu_keyboard() -> ReplyKeyboardMarkup:
    """Admin menyu"""
    keyboard = [
        [KeyboardButton(text="➕ Klinika Qo'shish"), KeyboardButton(text="➖ Klinika O'chirish")],
        [KeyboardButton(text="🏫 School Qo'shish"), KeyboardButton(text="🏫 School O'chirish")],
        [KeyboardButton(text="📋 Buyurtmalarni Ko'rish")],
        [KeyboardButton(text="🔙 Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def cancel_keyboard() -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi"""
    keyboard = [[KeyboardButton(text="❌ Bekor qilish")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def contact_keyboard() -> ReplyKeyboardMarkup:
    """Kontakt jo'natish"""
    keyboard = [[KeyboardButton(text="📱 Telefonni Jo'natish", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def phone_button_keyboard() -> ReplyKeyboardMarkup:
    """Telefon tugmasi"""
    keyboard = [
        [KeyboardButton(text="📱 Raqamni Jo'natish", request_contact=True)],
        [KeyboardButton(text="❌ Bekor qilish")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def pet_type_keyboard() -> ReplyKeyboardMarkup:
    """Hayvon turlarini tanlash"""
    keyboard = []
    for i in range(0, len(ANIMAL_TYPES), 2):
        row = [KeyboardButton(text=ANIMAL_TYPES[i])]
        if i + 1 < len(ANIMAL_TYPES):
            row.append(KeyboardButton(text=ANIMAL_TYPES[i + 1]))
        keyboard.append(row)
    keyboard.append([KeyboardButton(text="❌ Bekor qilish")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def vet_services_keyboard() -> ReplyKeyboardMarkup:
    """Veterinar xizmatlar"""
    keyboard = []
    for i in range(0, len(VET_SERVICES), 2):
        row = [KeyboardButton(text=VET_SERVICES[i])]
        if i + 1 < len(VET_SERVICES):
            row.append(KeyboardButton(text=VET_SERVICES[i + 1]))
        keyboard.append(row)
    keyboard.append([KeyboardButton(text="❌ Bekor qilish")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def confirm_keyboard() -> ReplyKeyboardMarkup:
    """Ha/Yo'q"""
    keyboard = [[KeyboardButton(text="✅ Ha"), KeyboardButton(text="❌ Yo'q")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# =================== INLINE KEYBOARDS ===================

def main_menu_inline() -> InlineKeyboardMarkup:
    """Asosiy menyyu (inline)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐾 Xizmatlar", callback_data="services")],
        [InlineKeyboardButton(text="🏥 Klinikalar", callback_data="clinics")],
        [InlineKeyboardButton(text="✂️ Grooming", callback_data="grooming")],
        [InlineKeyboardButton(text="🏥 Veterinar Tibbiyoti", callback_data="vet_service")],
        [InlineKeyboardButton(text="🎓 Pet Oqitish", callback_data="training")],
        [InlineKeyboardButton(text="🏨 Pet Hotel", callback_data="hotel_service")],
        [InlineKeyboardButton(text="🐕 Hayvon Sotish", callback_data="pet_sale")],
        [InlineKeyboardButton(text="👶 Asrab Turishga Berish", callback_data="daycare")],
        [InlineKeyboardButton(text="📞 Bog'lanish", callback_data="contact_info")],
        [InlineKeyboardButton(text="⭐ Feedback", callback_data="feedback")]
    ])
    return keyboard

def grooming_inline() -> InlineKeyboardMarkup:
    """Grooming xizmatlar"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✂️ Shampooylash", callback_data="grooming_shampoo")],
        [InlineKeyboardButton(text="✂️ Kesish", callback_data="grooming_cut")],
        [InlineKeyboardButton(text="✂️ Tirnoq kesish", callback_data="grooming_nail")],
        [InlineKeyboardButton(text="✂️ Ko'z tozalash", callback_data="grooming_eye")],
        [InlineKeyboardButton(text="✂️ Quloq tozalash", callback_data="grooming_ear")],
        [InlineKeyboardButton(text="✂️ Barcha xizmatlar", callback_data="grooming_all")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
    ])
    return keyboard

def clinics_inline() -> InlineKeyboardMarkup:
    """Klinikalar ro'yxati"""
    clinics = db.get_all_clinics()
    keyboard = []
    
    for clinic in clinics:
        keyboard.append([InlineKeyboardButton(
            text=f"🏥 {clinic['name']}", 
            callback_data=f"clinic_{clinic['clinic_id']}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def clinic_details_inline(clinic_id: int) -> InlineKeyboardMarkup:
    """Klinika detalları"""
    clinics = db.get_all_clinics()
    clinic = next((c for c in clinics if c['clinic_id'] == clinic_id), None)
    
    if clinic:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Qo'ng'iroq", url=f"tel:{clinic['phone']}")],
            [InlineKeyboardButton(text="🔙 Klinikalarga qaytish", callback_data="clinics")]
        ])
        return keyboard
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
    ])

def pet_schools_inline() -> InlineKeyboardMarkup:
    """Pet schoollar ro'yxati"""
    schools = db.get_all_pet_schools()
    keyboard = []
    
    for school in schools:
        keyboard.append([InlineKeyboardButton(
            text=f"🏫 {school['name']}", 
            callback_data=f"school_{school['school_id']}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def courses_inline(school_id: int) -> InlineKeyboardMarkup:
    """Kurslar ro'yxati"""
    keyboard = []
    
    for course in PET_COURSES:
        keyboard.append([InlineKeyboardButton(
            text=f"📚 {course['name']}", 
            callback_data=f"course_{school_id}_{course['name']}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def vet_services_inline() -> InlineKeyboardMarkup:
    """Veterinar xizmatlar (inline)"""
    keyboard = []
    
    for service in VET_SERVICES:
        keyboard.append([InlineKeyboardButton(
            text=f"🏥 {service}", 
            callback_data=f"vet_service_{service}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def vet_clinics_inline() -> InlineKeyboardMarkup:
    """Veterinar klinikalar"""
    clinics = db.get_all_clinics()
    keyboard = []
    
    for clinic in clinics:
        keyboard.append([InlineKeyboardButton(
            text=f"🏥 {clinic['name']}", 
            callback_data=f"vet_clinic_{clinic['clinic_id']}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def back_button_inline() -> InlineKeyboardMarkup:
    """Orqaga tugmasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Asosiy menyyu", callback_data="back_main")]
    ])
    return keyboard

def contact_info_inline() -> InlineKeyboardMarkup:
    """Kontakt ma'lumotlari"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 " + CONTACT_INFO['username'], 
                            url=CONTACT_INFO['telegram'])],
        [InlineKeyboardButton(text="📞 " + CONTACT_INFO['phone'], 
                            url=f"tel:{CONTACT_INFO['phone']}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
    ])
    return keyboard

def confirm_order_inline() -> InlineKeyboardMarkup:
    """Buyurtmani tasdiqlash"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_order")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")]
    ])
    return keyboard

def rating_inline() -> InlineKeyboardMarkup:
    """Reyting tugmalari"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐", callback_data="rating_1"),
         InlineKeyboardButton(text="⭐⭐", callback_data="rating_2"),
         InlineKeyboardButton(text="⭐⭐⭐", callback_data="rating_3")],
        [InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data="rating_4"),
         InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data="rating_5")]
    ])
    return keyboard

def clinic_selection_inline() -> ReplyKeyboardMarkup:
    """Klinika tanlash (outline)"""
    clinics = db.get_all_clinics()
    keyboard = []
    
    for i in range(0, len(clinics), 2):
        row = [KeyboardButton(text=clinics[i]['name'])]
        if i + 1 < len(clinics):
            row.append(KeyboardButton(text=clinics[i + 1]['name']))
        keyboard.append(row)
    
    keyboard.append([KeyboardButton(text="❌ Bekor qilish")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)