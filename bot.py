"""
bot.py - Asosiy Bot va Handlerlari (TO'LIQ VA XATOSIZ)
"""
import logging
from aiogram import Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, Contact
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN, SERVICES, ADMIN_IDS, ADMIN_GROUP_ID, CONTACT_INFO
from database import db
from states import *
from keyboards import *

from aiogram import Bot
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

# =================== ASOSIY KOMANDALAR ===================

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    """Boshlang'ich komanda"""
    user = message.from_user
    
    db.add_user(
        user_id=user.id,
        username=user.username or "NoUsername",
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    # Admin tekshirish
    if user.id in ADMIN_IDS:
        await state.set_state(AdminStates.admin_menu)
        await message.answer(
            f"🔐 Assalamu alaikum, Admin {user.first_name}!\n\nAdmin Panelga xush kelibsiz.",
            reply_markup=admin_menu_keyboard()
        )
    else:
        await state.set_state(UserStates.main_menu)
        welcome_text = f"""
🐾 <b>Pet Tashkent</b> ga xush kelibsiz, {user.first_name}! 👋

Biz Tashkentdagi eng ishonchli pet xizmatini taqdim etamiz.
"""
        await message.answer(welcome_text, reply_markup=main_menu_with_extra_keyboard())

@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    """Admin panelga kirish"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    
    await state.set_state(AdminStates.admin_menu)
    await message.answer("🔐 Admin Panelga xush kelibsiz!", reply_markup=admin_menu_keyboard())

# =================== ADMIN PANEL - KLINIKA ===================

@router.message(AdminStates.admin_menu, F.text == "➕ Klinika Qo'shish")
async def add_clinic_start(message: Message, state: FSMContext):
    """Klinika qo'shishni boshlash"""
    await state.set_state(AdminStates.adding_clinic_name)
    await message.answer("🏥 Klinika nomini kiriting:", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_clinic_name)
async def add_clinic_name(message: Message, state: FSMContext):
    """Klinika nomi"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    await state.update_data(clinic_name=message.text)
    await state.set_state(AdminStates.adding_clinic_address)
    await message.answer("📍 Manzilni kiriting:", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_clinic_address)
async def add_clinic_address(message: Message, state: FSMContext):
    """Klinika manzili"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    await state.update_data(clinic_address=message.text)
    await state.set_state(AdminStates.adding_clinic_phone)
    await message.answer("📞 Telefon raqamini kiriting:", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_clinic_phone)
async def add_clinic_phone(message: Message, state: FSMContext):
    """Klinika telefoni"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    await state.update_data(clinic_phone=message.text)
    await state.set_state(AdminStates.adding_clinic_hours)
    await message.answer("🕐 Ish vaqtini kiriting (masalan: 09:00 - 20:00):", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_clinic_hours)
async def add_clinic_hours(message: Message, state: FSMContext):
    """Klinika ish vaqti"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    await state.update_data(clinic_hours=message.text)
    await state.set_state(AdminStates.adding_clinic_services)
    await message.answer("🩺 Xizmatlarni kiriting (vergul bilan ajrating):", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_clinic_services)
async def add_clinic_services(message: Message, state: FSMContext):
    """Klinika xizmatlar"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    data = await state.get_data()
    
    success = db.add_clinic(
        name=data['clinic_name'],
        address=data['clinic_address'],
        phone=data['clinic_phone'],
        hours=data['clinic_hours'],
        services=message.text
    )
    
    if success:
        await state.set_state(AdminStates.admin_menu)
        await message.answer(f"✅ {data['clinic_name']} muvaffaqiyatli qo'shildi!", reply_markup=admin_menu_keyboard())
    else:
        await message.answer("❌ Xatolik yuz berdi", reply_markup=admin_menu_keyboard())

@router.message(AdminStates.admin_menu, F.text == "➖ Klinika O'chirish")
async def delete_clinic_menu(message: Message, state: FSMContext):
    """Klinika o'chirish menyu"""
    clinics = db.get_all_clinics()
    
    if not clinics:
        await message.answer("❌ Klinika yo'q", reply_markup=admin_menu_keyboard())
        return
    
    keyboard = []
    for clinic in clinics:
        keyboard.append([KeyboardButton(text=clinic['name'])])
    keyboard.append([KeyboardButton(text="❌ Bekor qilish")])
    
    await state.set_state(AdminStates.deleting_clinic)
    await message.answer("Klinikani tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))

@router.message(AdminStates.deleting_clinic)
async def delete_clinic(message: Message, state: FSMContext):
    """Klinikani o'chirish"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    clinics = db.get_all_clinics()
    clinic = next((c for c in clinics if c['name'] == message.text), None)
    
    if clinic:
        db.delete_clinic(clinic['clinic_id'])
        await state.set_state(AdminStates.admin_menu)
        await message.answer(f"✅ {clinic['name']} o'chirildi", reply_markup=admin_menu_keyboard())
    else:
        await message.answer("❌ Klinika topilmadi", reply_markup=admin_menu_keyboard())

# =================== ADMIN PANEL - PET SCHOOL ===================

@router.message(AdminStates.admin_menu, F.text == "🏫 School Qo'shish")
async def add_school_start(message: Message, state: FSMContext):
    """Pet School qo'shishni boshlash"""
    await state.set_state(AdminStates.adding_school_name)
    await message.answer("🏫 School nomini kiriting:", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_school_name)
async def add_school_name(message: Message, state: FSMContext):
    """School nomi"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    await state.update_data(school_name=message.text)
    await state.set_state(AdminStates.adding_school_address)
    await message.answer("📍 Manzilni kiriting:", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_school_address)
async def add_school_address(message: Message, state: FSMContext):
    """School manzili"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    await state.update_data(school_address=message.text)
    await state.set_state(AdminStates.adding_school_phone)
    await message.answer("📞 Telefon raqamini kiriting:", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_school_phone)
async def add_school_phone(message: Message, state: FSMContext):
    """School telefoni"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    await state.update_data(school_phone=message.text)
    await state.set_state(AdminStates.adding_school_courses)
    await message.answer("📚 Kurslarni kiriting (vergul bilan ajrating):", reply_markup=cancel_keyboard())

@router.message(AdminStates.adding_school_courses)
async def add_school_courses(message: Message, state: FSMContext):
    """School kurslar"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    data = await state.get_data()
    
    success = db.add_pet_school(
        name=data['school_name'],
        address=data['school_address'],
        phone=data['school_phone'],
        courses=message.text
    )
    
    if success:
        await state.set_state(AdminStates.admin_menu)
        await message.answer(f"✅ {data['school_name']} qo'shildi", reply_markup=admin_menu_keyboard())
    else:
        await message.answer("❌ Xatolik yuz berdi", reply_markup=admin_menu_keyboard())

@router.message(AdminStates.admin_menu, F.text == "🏫 School O'chirish")
async def delete_school_menu(message: Message, state: FSMContext):
    """Pet School o'chirish menyu"""
    schools = db.get_all_pet_schools()
    
    if not schools:
        await message.answer("❌ School yo'q", reply_markup=admin_menu_keyboard())
        return
    
    keyboard = []
    for school in schools:
        keyboard.append([KeyboardButton(text=school['name'])])
    keyboard.append([KeyboardButton(text="❌ Bekor qilish")])
    
    await state.set_state(AdminStates.deleting_school)
    await message.answer("Schoolni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))

@router.message(AdminStates.deleting_school)
async def delete_school(message: Message, state: FSMContext):
    """Pet Schoolni o'chirish"""
    if message.text == "❌ Bekor qilish":
        await state.set_state(AdminStates.admin_menu)
        await message.answer("Bekor qilindi", reply_markup=admin_menu_keyboard())
        return
    
    schools = db.get_all_pet_schools()
    school = next((s for s in schools if s['name'] == message.text), None)
    
    if school:
        db.delete_pet_school(school['school_id'])
        await state.set_state(AdminStates.admin_menu)
        await message.answer(f"✅ {school['name']} o'chirildi", reply_markup=admin_menu_keyboard())
    else:
        await message.answer("❌ School topilmadi", reply_markup=admin_menu_keyboard())

@router.message(AdminStates.admin_menu, F.text == "📋 Buyurtmalarni Ko'rish")
async def view_all_orders(message: Message, state: FSMContext):
    """Barcha buyurtmalarni ko'rish"""
    grooming = db.get_all_grooming_orders()
    vet = db.get_all_vet_orders()
    training = db.get_all_training_orders()
    sale = db.get_all_pet_sale_orders()
    daycare = db.get_all_daycare_orders()
    
    orders_text = f"""
📋 <b>BARCHA BUYURTMALAR</b>

✂️ <b>Grooming:</b> {len(grooming)} ta
🏥 <b>Veterinar:</b> {len(vet)} ta
🎓 <b>Oqitish:</b> {len(training)} ta
🐕 <b>Sotish:</b> {len(sale)} ta
👶 <b>Asrab turish:</b> {len(daycare)} ta
"""
    
    await message.answer(orders_text, reply_markup=admin_menu_keyboard())

@router.message(AdminStates.admin_menu, F.text == "🔙 Orqaga")
async def admin_back(message: Message, state: FSMContext):
    """Admin paneldan chiqish"""
    await state.clear()
    user = message.from_user
    await message.answer(f"🐾 Xush kelibsiz, {user.first_name}!", reply_markup=main_menu_with_extra_keyboard())

# =================== GROOMING XIZMATI ===================

@router.callback_query(F.data == "grooming")
async def show_grooming(callback: CallbackQuery):
    """Grooming xizmatlar"""
    await callback.message.edit_text(
        "<b>✂️ Grooming Xizmatlar</b>\n\nXizmatni tanlang:",
        reply_markup=grooming_inline()
    )

@router.callback_query(F.data.startswith("grooming_"))
async def grooming_order(callback: CallbackQuery, state: FSMContext):
    """Grooming buyurtmasini boshlash"""
    service = callback.data.split("_", 1)[1]
    
    service_names = {
        "shampoo": "Shampooylash",
        "cut": "Kesish",
        "nail": "Tirnoq kesish",
        "eye": "Ko'z tozalash",
        "ear": "Quloq tozalash",
        "all": "Barcha xizmatlar"
    }
    
    service_name = service_names.get(service, "Grooming")
    
    confirm_text = f"""
<b>✂️ {service_name}</b>

💰 <b>Narx:</b> 50,000 - 100,000 so'm
⏱️ <b>Vaqti:</b> 1-3 soat

Bu xizmatni buyurtma qilmoqchimisiz?
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha", callback_data=f"confirm_grooming_{service}")],
        [InlineKeyboardButton(text="❌ Yo'q", callback_data="grooming")]
    ])
    
    await callback.message.edit_text(confirm_text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("confirm_grooming_"))
async def grooming_confirmed(callback: CallbackQuery, state: FSMContext):
    """Grooming tasdiqland"""
    service = callback.data.split("_", 2)[2]
    
    service_names = {
        "shampoo": "Shampooylash",
        "cut": "Kesish",
        "nail": "Tirnoq kesish",
        "eye": "Ko'z tozalash",
        "ear": "Quloq tozalash",
        "all": "Barcha xizmatlar"
    }
    
    service_name = service_names.get(service, "Grooming")
    
    await state.update_data(grooming_service=service, grooming_service_name=service_name)
    await state.set_state(GroomingStates.waiting_for_time)
    
    await callback.message.edit_text(
        f"<b>✂️ {service_name}</b>\n\n<b>Sana va vaqtni kiriting (masalan: 15.12 14:00):</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")]
        ])
    )

@router.message(GroomingStates.waiting_for_time)
async def grooming_time_received(message: Message, state: FSMContext):
    """Grooming vaqti qabul qilindi"""
    await state.update_data(scheduled_time=message.text)
    await state.set_state(GroomingStates.waiting_for_clinic)
    
    await message.answer(
        "<b>🏢 Filyal tanlang:</b>",
        reply_markup=clinic_selection_inline()
    )

@router.message(GroomingStates.waiting_for_clinic)
async def grooming_clinic_received(message: Message, state: FSMContext):
    """Grooming filyali tanlandi"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Buyurtma bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    clinics = db.get_all_clinics()
    clinic = next((c for c in clinics if c['name'] == message.text), None)
    
    if not clinic:
        await message.answer("❌ Noto'g'ri filyal. Qayta tanlang:", reply_markup=clinic_selection_inline())
        return
    
    data = await state.get_data()
    
    confirm_text = f"""
<b>✅ Buyurtma Tasdiqlash</b>

<b>Xizmat:</b> {data['grooming_service_name']}
<b>Sana/Vaqt:</b> {data['scheduled_time']}
<b>Filyal:</b> {clinic['name']}
<b>Manzil:</b> {clinic['address']}
<b>Telefon:</b> {clinic['phone']}
"""
    
    await state.update_data(clinic_id=clinic['clinic_id'], clinic_name=clinic['name'])
    await state.set_state(GroomingStates.confirming_order)
    
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="✅ Tasdiqlash")],
        [KeyboardButton(text="❌ Bekor qilish")]
    ], resize_keyboard=True)
    
    await message.answer(confirm_text, reply_markup=keyboard)

@router.message(GroomingStates.confirming_order, F.text == "✅ Tasdiqlash")
async def confirm_grooming_final(message: Message, state: FSMContext):
    """Grooming yakuniy tasdiqlash"""
    data = await state.get_data()
    user_id = message.from_user.id
    
    order_id = db.create_grooming_order(
        user_id=user_id,
        service_name=data['grooming_service_name'],
        scheduled_time=data['scheduled_time'],
        clinic_id=data['clinic_id']
    )
    
    if order_id:
        await state.clear()
        confirmation_text = f"""
✅ <b>Buyurtma Muvaffaqiyatli Yaratildi!</b>

📝 <b>Buyurtma Raqami:</b> #{order_id}
✂️ <b>Xizmat:</b> {data['grooming_service_name']}
📅 <b>Sana/Vaqt:</b> {data['scheduled_time']}
🏢 <b>Filyal:</b> {data['clinic_name']}
"""
        await message.answer(confirmation_text, reply_markup=main_menu_with_extra_keyboard())
        
        admin_msg = f"""
📝 <b>YANGI GROOMING BUYURTMA</b>

<b>Buyurtma #:</b> {order_id}
<b>User ID:</b> {user_id}
<b>Xizmat:</b> {data['grooming_service_name']}
<b>Vaqt:</b> {data['scheduled_time']}
<b>Filyal:</b> {data['clinic_name']}
"""
        try:
            await bot.send_message(ADMIN_GROUP_ID, admin_msg)
        except Exception as e:
            logger.error(f"Gruppa xatosi: {e}")

@router.message(GroomingStates.confirming_order, F.text == "❌ Bekor qilish")
async def cancel_grooming(message: Message, state: FSMContext):
    """Grooming bekor qilish"""
    await state.clear()
    await message.answer("❌ Buyurtma bekor qilindi", reply_markup=main_menu_with_extra_keyboard())

# =================== VETERINAR TIBBIYOT ===================

@router.callback_query(F.data == "vet_service")
async def vet_services_list(callback: CallbackQuery):
    """Veterinar xizmatlar ro'yxati"""
    await callback.message.edit_text(
        "<b>🏥 Veterinar Xizmatlar</b>\n\nXizmatni tanlang:",
        reply_markup=vet_services_inline()
    )

@router.callback_query(F.data.startswith("vet_service_"))
async def vet_service_selected(callback: CallbackQuery, state: FSMContext):
    """Veterinar xizmati tanlandi"""
    service = callback.data.split("_", 2)[2]
    
    await state.update_data(vet_service=service)
    await state.set_state(VetStates.waiting_for_pet_type)
    
    await callback.message.edit_text(
        f"<b>🏥 {service}</b>\n\n<b>Hayvoningiz turini kiriting:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")]
        ])
    )

@router.message(VetStates.waiting_for_pet_type)
async def vet_pet_type(message: Message, state: FSMContext):
    """Hayvon turi"""
    await state.update_data(pet_type=message.text)
    await state.set_state(VetStates.waiting_for_pet_name)
    await message.answer("<b>Hayvoningizning ismini kiriting:</b>", reply_markup=cancel_keyboard())

@router.message(VetStates.waiting_for_pet_name)
async def vet_pet_name(message: Message, state: FSMContext):
    """Hayvon ismi"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    await state.update_data(pet_name=message.text)
    await state.set_state(VetStates.waiting_for_phone)
    await message.answer("<b>Telefon raqamingizni kiriting:</b>", reply_markup=phone_button_keyboard())

@router.message(VetStates.waiting_for_phone)
async def vet_phone(message: Message, state: FSMContext):
    """Telefon raqam"""
    if isinstance(message.contact, Contact):
        phone = message.contact.phone_number
    else:
        phone = message.text
    
    await state.update_data(phone=phone)
    await state.set_state(VetStates.waiting_for_clinic)
    
    await message.answer(
        "<b>🏢 Filyal tanlang:</b>",
        reply_markup=clinic_selection_inline()
    )

@router.message(VetStates.waiting_for_clinic)
async def vet_clinic(message: Message, state: FSMContext):
    """Filyal tanlash"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    clinics = db.get_all_clinics()
    clinic = next((c for c in clinics if c['name'] == message.text), None)
    
    if not clinic:
        await message.answer("❌ Noto'g'ri filyal. Qayta tanlang:", reply_markup=clinic_selection_inline())
        return
    
    data = await state.get_data()
    
    confirm_text = f"""
<b>✅ Buyurtma Tasdiqlash</b>

<b>Xizmat:</b> {data['vet_service']}
<b>Hayvon Turi:</b> {data['pet_type']}
<b>Hayvon Ismi:</b> {data['pet_name']}
<b>Telefon:</b> {data['phone']}
<b>Filyal:</b> {clinic['name']}
<b>Manzil:</b> {clinic['address']}
"""
    
    await state.update_data(clinic_id=clinic['clinic_id'], clinic_name=clinic['name'])
    await state.set_state(VetStates.confirming_order)
    
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="✅ Tasdiqlash")],
        [KeyboardButton(text="❌ Bekor qilish")]
    ], resize_keyboard=True)
    
    await message.answer(confirm_text, reply_markup=keyboard)

@router.message(VetStates.confirming_order, F.text == "✅ Tasdiqlash")
async def vet_confirm_final(message: Message, state: FSMContext):
    """Veterinar buyurtmasini tasdiqlash"""
    data = await state.get_data()
    user_id = message.from_user.id
    
    order_id = db.create_vet_order(
        user_id=user_id,
        pet_name=data['pet_name'],
        pet_type=data['pet_type'],
        service_type=data['vet_service'],
        phone=data['phone'],
        clinic_id=data['clinic_id']
    )
    
    if order_id:
        await state.clear()
        confirmation_text = f"""
✅ <b>Buyurtma Muvaffaqiyatli Yaratildi!</b>

📝 <b>Buyurtma Raqami:</b> #{order_id}
🏥 <b>Xizmat:</b> {data['vet_service']}
🐾 <b>Hayvon:</b> {data['pet_name']} ({data['pet_type']})
📞 <b>Telefon:</b> {data['phone']}

Biz tez orada siz bilan bog'lanamiz!
"""
        await message.answer(confirmation_text, reply_markup=main_menu_with_extra_keyboard())
        
        admin_msg = f"""
📝 <b>YANGI VETERINAR BUYURTMA</b>

<b>Buyurtma #:</b> {order_id}
<b>User ID:</b> {user_id}
<b>Xizmat:</b> {data['vet_service']}
<b>Hayvon:</b> {data['pet_name']} ({data['pet_type']})
<b>Telefon:</b> {data['phone']}
<b>Filyal:</b> {data['clinic_name']}
"""
        try:
            await bot.send_message(ADMIN_GROUP_ID, admin_msg)
        except Exception as e:
            logger.error(f"Vet gruppa xatosi: {e}")

# =================== PET OQITISH ===================

@router.callback_query(F.data == "training")
async def pet_training(callback: CallbackQuery):
    """Pet oqitish"""
    await callback.message.edit_text(
        "<b>🎓 Pet Oqitish Filyallari</b>\n\nFilyal tanlang:",
        reply_markup=pet_schools_inline()
    )

@router.callback_query(F.data.startswith("school_"))
async def select_school(callback: CallbackQuery, state: FSMContext):
    """School tanlandi"""
    school_id = int(callback.data.split("_")[1])
    schools = db.get_all_pet_schools()
    school = next((s for s in schools if s['school_id'] == school_id), None)
    
    if school:
        await state.update_data(school_id=school_id, school_name=school['name'])
        await state.set_state(TrainingStates.waiting_for_course)
        await callback.message.edit_text(
            f"<b>🏫 {school['name']}</b>\n\n<b>Kursni tanlang:</b>",
            reply_markup=courses_inline(school_id)
        )

@router.callback_query(F.data.startswith("course_"))
async def select_course(callback: CallbackQuery, state: FSMContext):
    """Kurs tanlandi"""
    parts = callback.data.split("_", 2)
    school_id = int(parts[1])
    course_name = parts[2]
    
    await state.update_data(course_name=course_name)
    await state.set_state(TrainingStates.waiting_for_phone)
    
    await callback.message.edit_text(
        f"<b>📚 {course_name}</b>\n\n<b>Telefon raqamingizni kiriting:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")]
        ])
    )

@router.message(TrainingStates.waiting_for_phone)
async def training_phone(message: Message, state: FSMContext):
    """Oqitish telefoni"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    await state.update_data(phone=message.text)
    await state.set_state(TrainingStates.waiting_for_phone_confirm)
    
    await message.answer(
        "<b>Telefon raqamingizni tugma bilan tasdiqlang:</b>",
        reply_markup=phone_button_keyboard()
    )

@router.message(TrainingStates.waiting_for_phone_confirm)
async def training_phone_confirm(message: Message, state: FSMContext):
    """Telefon tasdiqlash"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    if isinstance(message.contact, Contact):
        phone = message.contact.phone_number
        await state.update_data(phone=phone)
        await state.set_state(TrainingStates.waiting_for_name)
        await message.answer("<b>Ismingizni kiriting:</b>", reply_markup=cancel_keyboard())
    else:
        await message.answer("❌ Iltimos, tugma orqali raqam yuboring!", reply_markup=phone_button_keyboard())

@router.message(TrainingStates.waiting_for_name)
async def training_name(message: Message, state: FSMContext):
    """Oqitish ismi"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    data = await state.get_data()
    
    confirm_text = f"""
<b>✅ Buyurtma Tasdiqlash</b>

<b>Kurs:</b> {data['course_name']}
<b>Filyal:</b> {data['school_name']}
<b>Telefon:</b> {data['phone']}
<b>Ism:</b> {message.text}

Buyurtmani tasdiqlaysizmi?
"""
    
    await state.update_data(name=message.text)
    await state.set_state(TrainingStates.confirming_order)
    
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="✅ Tasdiqlash")],
        [KeyboardButton(text="❌ Bekor qilish")]
    ], resize_keyboard=True)
    
    await message.answer(confirm_text, reply_markup=keyboard)

@router.message(TrainingStates.confirming_order, F.text == "✅ Tasdiqlash")
async def training_confirm_final(message: Message, state: FSMContext):
    """Oqitish tasdiqlash"""
    data = await state.get_data()
    user_id = message.from_user.id
    
    order_id = db.create_training_order(
        user_id=user_id,
        course_name=data['course_name'],
        phone=data['phone'],
        school_id=data['school_id'],
        name=data['name']
    )
    
    if order_id:
        await state.clear()
        confirmation_text = f"""
✅ <b>Buyurtma Muvaffaqiyatli Yaratildi!</b>

📝 <b>Buyurtma Raqami:</b> #{order_id}
📚 <b>Kurs:</b> {data['course_name']}
🏫 <b>Filyal:</b> {data['school_name']}
👤 <b>Ism:</b> {data['name']}

Biz tez orada siz bilan bog'lanamiz!
"""
        await message.answer(confirmation_text, reply_markup=main_menu_with_extra_keyboard())
        
        admin_msg = f"""
📝 <b>YANGI OQITISH BUYURTMA</b>

<b>Buyurtma #:</b> {order_id}
<b>User ID:</b> {user_id}
<b>Kurs:</b> {data['course_name']}
<b>Filyal:</b> {data['school_name']}
<b>Ism:</b> {data['name']}
<b>Telefon:</b> {data['phone']}
"""
        try:
            await bot.send_message(ADMIN_GROUP_ID, admin_msg)
        except Exception as e:
            logger.error(f"Training gruppa xatosi: {e}")

@router.message(TrainingStates.confirming_order, F.text == "❌ Bekor qilish")
async def cancel_training(message: Message, state: FSMContext):
    """Oqitish bekor qilish"""
    await state.clear()
    await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())

# =================== HAYVON SOTISH ===================

@router.callback_query(F.data == "pet_sale")
async def pet_sale(callback: CallbackQuery, state: FSMContext):
    """Hayvon sotish"""
    await state.set_state(PetSaleStates.waiting_for_pet_type)
    await callback.message.edit_text(
        "<b>🐕 Hayvon Sotish</b>\n\n<b>Hayvoningiz turini kiriting:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")]
        ])
    )

@router.message(PetSaleStates.waiting_for_pet_type)
async def sale_pet_type(message: Message, state: FSMContext):
    """Sotish hayvon turi"""
    await state.update_data(animal_type=message.text)
    await state.set_state(PetSaleStates.waiting_for_description)
    await message.answer("<b>Hayvon haqida ma'lumot va kamchiliklarini yozing:</b>", reply_markup=cancel_keyboard())

@router.message(PetSaleStates.waiting_for_description)
async def sale_description(message: Message, state: FSMContext):
    """Sotish tavsifi"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    await state.update_data(description=message.text)
    await state.set_state(PetSaleStates.waiting_for_phone)
    await message.answer("<b>Telefon raqamingizni kiriting:</b>", reply_markup=phone_button_keyboard())

@router.message(PetSaleStates.waiting_for_phone)
async def sale_phone(message: Message, state: FSMContext):
    """Sotish telefoni"""
    if isinstance(message.contact, Contact):
        phone = message.contact.phone_number
    else:
        phone = message.text
    
    data = await state.get_data()
    user_id = message.from_user.id
    
    order_id = db.create_pet_sale_order(
        user_id=user_id,
        animal_type=data['animal_type'],
        description=data['description'],
        phone=phone
    )
    
    if order_id:
        await state.clear()
        confirmation_text = f"""
✅ <b>ADMINLARIMIZ TEZ ORADA RAQAMINGIZGA ALOQAGA CHIQISHADI</b>

📝 <b>Buyurtma Raqami:</b> #{order_id}
🐕 <b>Hayvon Turi:</b> {data['animal_type']}
📞 <b>Telefon:</b> {phone}
"""
        await message.answer(confirmation_text, reply_markup=main_menu_with_extra_keyboard())
        
        admin_msg = f"""
📝 <b>YANGI HAYVON SOTISH BUYURTMA</b>

<b>Buyurtma #:</b> {order_id}
<b>User ID:</b> {user_id}
<b>Hayvon Turi:</b> {data['animal_type']}
<b>Tavsif:</b> {data['description']}
<b>Telefon:</b> {phone}
"""
        try:
            await bot.send_message(ADMIN_GROUP_ID, admin_msg)
        except Exception as e:
            logger.error(f"Sotish gruppa xatosi: {e}")

# =================== VAQTINCHALIK ASRAB TURISH ===================

@router.callback_query(F.data == "daycare")
async def daycare_service(callback: CallbackQuery, state: FSMContext):
    """Vaqtinchalik asrab turish"""
    await state.set_state(DaycareStates.waiting_for_name)
    await callback.message.edit_text(
        "<b>👶 Vaqtinchalik Asrab Turishga Berish</b>\n\n<b>Odam ismini kiriting:</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="back_main")]
        ])
    )

@router.message(DaycareStates.waiting_for_name)
async def daycare_name(message: Message, state: FSMContext):
    """Daycare ism"""
    await state.update_data(name=message.text)
    await state.set_state(DaycareStates.waiting_for_phone)
    await message.answer("<b>Telefon raqamingizni kiriting:</b>", reply_markup=cancel_keyboard())

@router.message(DaycareStates.waiting_for_phone)
async def daycare_phone(message: Message, state: FSMContext):
    """Daycare telefon"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    # Contact bo'lsa telefon, yo'lsa text
    if isinstance(message.contact, Contact):
        phone = message.contact.phone_number
        await state.update_data(phone=phone)
        await state.set_state(DaycareStates.waiting_for_pet_type)
        await message.answer("<b>Hayvon turini kiriting:</b>", reply_markup=cancel_keyboard())
    else:
        await message.answer("❌ Iltimos, tugma orqali raqam yuboring!", reply_markup=phone_button_keyboard())

# =================== KONTAKT ===================

@router.callback_query(F.data == "contact_info")
async def contact_info(callback: CallbackQuery):
    """Kontakt ma'lumotlari"""
    contact_text = f"""
<b>📞 Bizga Bog'lanish</b>

👤 <b>Username:</b> @{CONTACT_INFO['username']}
📞 <b>Telefon:</b> {CONTACT_INFO['phone']}
📍 <b>Manzil:</b> {CONTACT_INFO['address']}
"""
    await callback.message.edit_text(contact_text, reply_markup=contact_info_inline())

# =================== ORQAGA TUGMASI ===================

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery, state: FSMContext):
    """Asosiy menyuya qaytish"""
    await state.clear()
    await callback.message.edit_text(
        "🐾 <b>Asosiy Menyu</b>",
        reply_markup=main_menu_inline()
    )

@router.callback_query(F.data == "services")
async def show_services(callback: CallbackQuery):
    """Xizmatlarni ko'rsatish"""
    services_text = "<b>🐾 Pet Xizmatlarimiz</b>\n\n"
    for key, service in SERVICES.items():
        services_text += f"{service['icon']} <b>{service['name']}</b>\n"
        services_text += f"💰 {service['price']}\n\n"
    
    await callback.message.edit_text(services_text, reply_markup=main_menu_inline())

@router.callback_query(F.data == "clinics")
async def show_clinics(callback: CallbackQuery):
    """Klinikalar ro'yxati"""
    await callback.message.edit_text(
        "<b>🏥 Veterinar Klinikalarimiz</b>\n\nKlinikani tanlang:",
        reply_markup=clinics_inline()
    )

@router.callback_query(F.data.startswith("clinic_"))
async def clinic_details(callback: CallbackQuery):
    """Klinika detalları"""
    clinic_id = int(callback.data.split("_")[1])
    clinics = db.get_all_clinics()
    clinic = next((c for c in clinics if c['clinic_id'] == clinic_id), None)
    
    if clinic:
        clinic_text = f"""
<b>🏥 {clinic['name']}</b>

📍 <b>Manzil:</b> {clinic['address']}
📞 <b>Telefon:</b> {clinic['phone']}
🕐 <b>Ish vaqti:</b> {clinic['hours']}
🩺 <b>Xizmatlar:</b> {clinic['services']}
"""
        await callback.message.edit_text(clinic_text, reply_markup=clinic_details_inline(clinic_id))

@router.callback_query(F.data == "hotel_service")
async def hotel_service(callback: CallbackQuery):
    """Pet Hotel xizmati"""
    hotel_text = f"""
<b>🏨 Pet Hotel</b>

{SERVICES['hotel']['description']}

💰 <b>Narx:</b> {SERVICES['hotel']['price']}
⏱️ <b>Banda vaqti:</b> Istalgan vaqt
🛏️ <b>Quloyi:</b> Komfort xonalar
🍽️ <b>Ovqat:</b> Premium sifatli yem

Buyurtma qilish uchun qo'ng'iroq qiling:
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Qo'ng'iroq", url=f"tel:{CONTACT_INFO['phone']}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
    ])
    
    await callback.message.edit_text(hotel_text, reply_markup=keyboard)

@router.callback_query(F.data == "feedback")
async def feedback(callback: CallbackQuery, state: FSMContext):
    """Feedback berish"""
    await state.set_state(FeedbackStates.waiting_for_rating)
    await callback.message.edit_text(
        "<b>⭐ Bizga Reyting Bering</b>\n\nXizmatimiz haqida qanday fikringiz?",
        reply_markup=rating_inline()
    )

@router.callback_query(F.data.startswith("rating_"), FeedbackStates.waiting_for_rating)
async def rating_selected(callback: CallbackQuery, state: FSMContext):
    """Reyting tanlandi"""
    rating = int(callback.data.split("_")[1])
    
    await state.update_data(rating=rating)
    await state.set_state(FeedbackStates.waiting_for_comment)
    
    await callback.message.edit_text(
        f"<b>Reyting:</b> {'⭐' * rating}\n\n<b>Fikringiz (ixtiyoriy):</b>",
        reply_markup=cancel_keyboard()
    )

@router.message(FeedbackStates.waiting_for_comment)
async def comment_received(message: Message, state: FSMContext):
    """Komment qabul qilindi"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi", reply_markup=main_menu_with_extra_keyboard())
        return
    
    await state.clear()
    await message.answer(
        "✅ Rahmat sizning fikringiz uchun!",
        reply_markup=main_menu_with_extra_keyboard()
    )

# =================== TEXT HANDLERI ===================

@router.message(F.text)
async def text_handler(message: Message):
    """Umumiy text handler"""
    text = message.text
    
    if text == "🐾 Pet Xizmatlar":
        await message.answer("<b>🐾 Pet Xizmatlar</b>", reply_markup=main_menu_inline())
    elif text == "🏥 Klinikalar":
        await message.answer("<b>🏥 Veterinar Klinikalarimiz</b>", reply_markup=clinics_inline())
    elif text == "✂️ Grooming":
        await message.answer("<b>✂️ Grooming Xizmatlar</b>", reply_markup=grooming_inline())
    elif text == "🎓 Pet Oqitish":
        await message.answer("<b>🎓 Pet Oqitish</b>", reply_markup=pet_schools_inline())
    elif text == "🏨 Pet Hotel":
        await message.answer("<b>🏨 Pet Hotel</b>", reply_markup=main_menu_inline())
    elif text == "🐕 Hayvon Sotish":
        await message.answer("<b>🐕 Hayvon Sotish</b>", reply_markup=main_menu_inline())
    elif text == "👶 Asrab Turish":
        await message.answer("<b>👶 Asrab Turish</b>", reply_markup=main_menu_inline())
    elif text == "📞 Bog'lanish":
        await message.answer("<b>📞 Bizga Bog'lanish</b>", reply_markup=contact_info_inline())
    elif text == "ℹ️ Ma'lumot":
        await message.answer("<b>ℹ️ Pet Tashkent</b>", reply_markup=main_menu_inline())
    else:
        await message.answer("🤔 Kechirasiz, bu buyruq ma'lum emas.", reply_markup=main_menu_with_extra_keyboard())

# =================== BOT ISHGA TUSHIRISH ===================

async def main():
    """Bot ishga tushirish"""
    dp.include_router(router)
    
    logger.info("🤖 Bot ishga tushdi...")
    
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())