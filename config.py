"""
config.py - Bot konfiguratsiyasi
"""
from typing import Final
from dotenv import load_dotenv
import os

load_dotenv()

# Bot Token
BOT_TOKEN: Final[str] = os.getenv('BOT_TOKEN', '8579181727:AAHBfRvqPZCAeCOWWvPKzLBpRbiRGLLyUQ8')

# Database
DB_PATH: Final[str] = 'pet_tashkent.db'

# Admin ID va Grup ID
ADMIN_IDS = [7987528056]  # Admin ID larini qo'ying
ADMIN_GROUP_ID = -1003380142003  # Admin gruppa ID sini qo'ying

# Dastlabki Klinikalar
DEFAULT_CLINICS = {
    "clinic1": {
        "name": "Tashkent Pet Care",
        "address": "Amir Temur ko'chasi, 45",
        "phone": "+998 71 200 50 50",
        "hours": "09:00 - 20:00",
        "services": "Tibbiyot, Joyasizlik operatsiyasi, Vaksinatsiya"
    },
    "clinic2": {
        "name": "Happy Paws Clinic",
        "address": "Nukus ko'chasi, 12",
        "phone": "+998 71 150 40 40",
        "hours": "09:00 - 21:00",
        "services": "Konsultatsiya, Dermatologiya, Stomatologiya"
    },
    "clinic3": {
        "name": "DrPet Veterinary",
        "address": "Oltin Vodii, 55",
        "phone": "+998 71 300 60 60",
        "hours": "08:00 - 22:00",
        "services": "Chirurgiya, USM, Laboratoriya"
    }
}

# Dastlabki Pet School Filyallari
DEFAULT_PET_SCHOOLS = [
    {
        "name": "Pet Academy Tashkent",
        "address": "Amir Temur ko'chasi, 50",
        "phone": "+998 71 210 50 50",
        "courses": "Asosiy oqitish, Advansed oqitish"
    },
    {
        "name": "Smart Pets School",
        "address": "Nukus ko'chasi, 25",
        "phone": "+998 71 160 60 60",
        "courses": "Oqitish, Yuzakore, Frizbi"
    }
]

# Xizmatlar va narxlar
SERVICES = {
    "tibbiyot": {
        "name": "🏥 Veterinar Tibbiyoti",
        "price": "50,000 - 200,000 so'm",
        "description": "Professional veterinar konsultatsiyasi va shifokori",
        "icon": "🏥"
    },
    "grooming": {
        "name": "✂️ Grooming Xizmatlar",
        "price": "50,000 - 150,000 so'm",
        "description": "Shampooylash, kesish, tirnoq kesish, quloq tozalash",
        "icon": "✂️"
    },
    "oqitish": {
        "name": "🎓 Pet Oqitish",
        "price": "100,000 so'm/oy",
        "description": "Profesional trenerni bilan hayvon oqitish",
        "icon": "🎓"
    },
    "hotel": {
        "name": "🏨 Pet Hotel",
        "price": "30,000 so'm/kun",
        "description": "Xavfsiz va qulay mehmanxona xizmati",
        "icon": "🏨"
    },
    "sotish": {
        "name": "🐕 Hayvon Sotish",
        "price": "Turli narxlar",
        "description": "Sog'lom hayvonlarni sotish",
        "icon": "🐕"
    },
    "asrab_turish": {
        "name": "👶 Vaqtinchalik Asrab Turishga Berish",
        "price": "20,000 - 50,000 so'm/kun",
        "description": "Vaqtinchalik asrab turish xizmati",
        "icon": "👶"
    }
}

# Grooming turlari
GROOMING_SERVICES = [
    "Shampooylash",
    "Kesish",
    "Tirnoq kesish",
    "Ko'z tozalash",
    "Quloq tozalash",
    "Barcha xizmatlar"
]

# Hayvon turlari
ANIMAL_TYPES = [
    "🐕 It",
    "🐈 Mushuk",
    "🐇 Quyonlar",
    "🦜 Qushlar",
    "🐹 Hamster",
    "Boshqasi"
]

# Veterinar Tibbiyot turlari
VET_SERVICES = [
    "Konsultatsiya",
    "Joyasizlik operatsiyasi",
    "Vaksinatsiya",
    "Dermatologiya",
    "Stomatologiya",
    "Chirurgiya",
    "USM",
    "Laboratoriya",
    "Boshqasi"
]

# Kontakt ma'lumotlari
CONTACT_INFO = {
    "username": "KHAKIMOV_A001",
    "phone": "+998 000 00 00",
    "telegram": "https://t.me/KHAKIMOV_A001",
    "address": "Tashkent shahar, Mirzo Ulugbek tumani"
}

# Pet School kurslar
PET_COURSES = [
    {"name": "Boshlang'ich Oqitish", "duration": "4 hafta", "price": "200,000 so'm"},
    {"name": "Advansed Oqitish", "duration": "6 hafta", "price": "350,000 so'm"},
    {"name": "Yuzakorе", "duration": "2 hafta", "price": "150,000 so'm"},
    {"name": "Frizbi", "duration": "3 hafta", "price": "180,000 so'm"}
]