"""
states.py - Finite State Machine holatlari
"""
from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    """Foydalanuvchi holatlari"""
    main_menu = State()
    selecting_service = State()
    viewing_clinics = State()
    viewing_grooming = State()

class AdminStates(StatesGroup):
    """Admin holatlari"""
    admin_menu = State()
    adding_clinic_name = State()
    adding_clinic_address = State()
    adding_clinic_phone = State()
    adding_clinic_hours = State()
    adding_clinic_services = State()
    deleting_clinic = State()
    
    adding_school_name = State()
    adding_school_address = State()
    adding_school_phone = State()
    adding_school_courses = State()
    deleting_school = State()
    
    viewing_orders = State()

class GroomingStates(StatesGroup):
    """Grooming jarayoni holatlari"""
    waiting_for_service = State()
    confirming_service = State()
    waiting_for_time = State()
    waiting_for_clinic = State()
    confirming_order = State()

class VetStates(StatesGroup):
    """Veterinar tibbiyot holatlari"""
    waiting_for_pet_type = State()
    waiting_for_service = State()
    waiting_for_pet_name = State()
    waiting_for_phone = State()
    waiting_for_clinic = State()
    confirming_order = State()

class TrainingStates(StatesGroup):
    """Pet oqitish holatlari"""
    waiting_for_course = State()
    waiting_for_phone = State()
    waiting_for_phone_confirm = State()
    waiting_for_name = State()
    confirming_order = State()

class PetSaleStates(StatesGroup):
    """Hayvon sotish holatlari"""
    waiting_for_pet_type = State()
    waiting_for_description = State()
    waiting_for_phone = State()
    confirming_order = State()

class DaycareStates(StatesGroup):
    """Vaqtinchalik asrab turish holatlari"""
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_pet_type = State()
    confirming_order = State()

class PetStates(StatesGroup):
    """Hayvon qo'shish holatlari"""
    waiting_for_pet_name = State()
    waiting_for_pet_type = State()
    waiting_for_breed = State()
    waiting_for_age = State()
    confirming_pet = State()

class ContactStates(StatesGroup):
    """Kontakt ma'lumotlari"""
    waiting_for_phone = State()
    waiting_for_name = State()
    waiting_for_message = State()

class FeedbackStates(StatesGroup):
    """Feedback holatlari"""
    waiting_for_rating = State()
    waiting_for_comment = State()