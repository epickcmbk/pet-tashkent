"""
database.py - SQLite bilan ishlash
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from config import DB_PATH, DEFAULT_CLINICS, DEFAULT_PET_SCHOOLS

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Bazaga ulanish"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Jadvallarni yaratish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Foydalanuvchilar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Hayvonlar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                pet_name TEXT,
                animal_type TEXT,
                breed TEXT,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Klinikalar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clinics (
                clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                hours TEXT,
                services TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Pet School jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pet_schools (
                school_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                courses TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Buyurtmalar jadvali (Grooming)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grooming_orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                service_name TEXT,
                scheduled_time TEXT,
                clinic_id INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id)
            )
        ''')
        
        # Veterinar Tibbiyot buyurtmalari
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vet_orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                pet_name TEXT,
                pet_type TEXT,
                service_type TEXT,
                phone TEXT,
                clinic_id INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id)
            )
        ''')
        
        # Pet Oqitish buyurtmalari
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_name TEXT,
                phone TEXT,
                school_id INTEGER,
                name TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (school_id) REFERENCES pet_schools(school_id)
            )
        ''')
        
        # Hayvon Sotish
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pet_sale_orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                animal_type TEXT,
                description TEXT,
                phone TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Vaqtinchalik Asrab Turish
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daycare_orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT,
                phone TEXT,
                animal_type TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Feedback jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rating INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        
        # Dastlabki klinikalarni qo'shish
        self.init_default_clinics()
        self.init_default_pet_schools()
        
        conn.close()
    
    def init_default_clinics(self):
        """Dastlabki klinikalarni qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM clinics')
        if cursor.fetchone()[0] == 0:
            for clinic in DEFAULT_CLINICS.values():
                cursor.execute('''
                    INSERT INTO clinics (name, address, phone, hours, services)
                    VALUES (?, ?, ?, ?, ?)
                ''', (clinic['name'], clinic['address'], clinic['phone'], 
                      clinic['hours'], clinic['services']))
            conn.commit()
        conn.close()
    
    def init_default_pet_schools(self):
        """Dastlabki pet schoollarni qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM pet_schools')
        if cursor.fetchone()[0] == 0:
            for school in DEFAULT_PET_SCHOOLS:
                cursor.execute('''
                    INSERT INTO pet_schools (name, address, phone, courses)
                    VALUES (?, ?, ?, ?)
                ''', (school['name'], school['address'], school['phone'], 
                      school['courses']))
            conn.commit()
        conn.close()
    
    # ===== FOYDALANUVCHI OPERATSIYALARI =====
    
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str = None) -> bool:
        """Foydalanuvchini qo'shish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Xato: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Foydalanuvchini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'user_id': result[0],
                'username': result[1],
                'first_name': result[2],
                'last_name': result[3],
                'phone': result[4],
                'created_at': result[5]
            }
        return None
    
    # ===== KLINIKA OPERATSIYALARI =====
    
    def add_clinic(self, name: str, address: str, phone: str, hours: str, services: str) -> bool:
        """Klinika qo'shish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clinics (name, address, phone, hours, services)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, address, phone, hours, services))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Xato: {e}")
            return False
    
    def get_all_clinics(self) -> List[Dict]:
        """Barcha klinikalarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clinics ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        clinics = []
        for result in results:
            clinics.append({
                'clinic_id': result[0],
                'name': result[1],
                'address': result[2],
                'phone': result[3],
                'hours': result[4],
                'services': result[5]
            })
        return clinics
    
    def delete_clinic(self, clinic_id: int) -> bool:
        """Klinikani o'chirish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM clinics WHERE clinic_id = ?', (clinic_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Xato: {e}")
            return False
    
    # ===== PET SCHOOL OPERATSIYALARI =====
    
    def add_pet_school(self, name: str, address: str, phone: str, courses: str) -> bool:
        """Pet School qo'shish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pet_schools (name, address, phone, courses)
                VALUES (?, ?, ?, ?)
            ''', (name, address, phone, courses))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Xato: {e}")
            return False
    
    def get_all_pet_schools(self) -> List[Dict]:
        """Barcha pet schoollarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pet_schools ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        schools = []
        for result in results:
            schools.append({
                'school_id': result[0],
                'name': result[1],
                'address': result[2],
                'phone': result[3],
                'courses': result[4]
            })
        return schools
    
    def delete_pet_school(self, school_id: int) -> bool:
        """Pet Schoolni o'chirish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM pet_schools WHERE school_id = ?', (school_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Xato: {e}")
            return False
    
    # ===== GROOMING BUYURTMA =====
    
    def create_grooming_order(self, user_id: int, service_name: str, 
                              scheduled_time: str, clinic_id: int) -> int:
        """Grooming buyurtma yaratish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO grooming_orders (user_id, service_name, scheduled_time, clinic_id)
                VALUES (?, ?, ?, ?)
            ''', (user_id, service_name, scheduled_time, clinic_id))
            conn.commit()
            order_id = cursor.lastrowid
            conn.close()
            return order_id
        except Exception as e:
            print(f"Xato: {e}")
            return None
    
    # ===== VET TIBBIYOT BUYURTMA =====
    
    def create_vet_order(self, user_id: int, pet_name: str, pet_type: str, 
                        service_type: str, phone: str, clinic_id: int) -> int:
        """Veterinar tibbiyot buyurtma yaratish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vet_orders (user_id, pet_name, pet_type, service_type, phone, clinic_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, pet_name, pet_type, service_type, phone, clinic_id))
            conn.commit()
            order_id = cursor.lastrowid
            conn.close()
            return order_id
        except Exception as e:
            print(f"Xato: {e}")
            return None
    
    # ===== PET OQITISH BUYURTMA =====
    
    def create_training_order(self, user_id: int, course_name: str, 
                             phone: str, school_id: int, name: str) -> int:
        """Pet oqitish buyurtma yaratish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO training_orders (user_id, course_name, phone, school_id, name)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, course_name, phone, school_id, name))
            conn.commit()
            order_id = cursor.lastrowid
            conn.close()
            return order_id
        except Exception as e:
            print(f"Xato: {e}")
            return None
    
    # ===== HAYVON SOTISH =====
    
    def create_pet_sale_order(self, user_id: int, animal_type: str, 
                             description: str, phone: str) -> int:
        """Hayvon sotish buyurtmasi yaratish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pet_sale_orders (user_id, animal_type, description, phone)
                VALUES (?, ?, ?, ?)
            ''', (user_id, animal_type, description, phone))
            conn.commit()
            order_id = cursor.lastrowid
            conn.close()
            return order_id
        except Exception as e:
            print(f"Xato: {e}")
            return None
    
    # ===== VAQTINCHALIK ASRAB TURISH =====
    
    def create_daycare_order(self, user_id: int, name: str, phone: str, 
                            animal_type: str) -> int:
        """Vaqtinchalik asrab turish buyurtmasi yaratish"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO daycare_orders (user_id, name, phone, animal_type)
                VALUES (?, ?, ?, ?)
            ''', (user_id, name, phone, animal_type))
            conn.commit()
            order_id = cursor.lastrowid
            conn.close()
            return order_id
        except Exception as e:
            print(f"Xato: {e}")
            return None
    
    # ===== BUYURTMALAR OLINGANI =====
    
    def get_all_grooming_orders(self) -> List[Dict]:
        """Barcha grooming buyurtmalarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM grooming_orders ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        orders = []
        for result in results:
            orders.append({
                'order_id': result[0],
                'user_id': result[1],
                'service_name': result[2],
                'scheduled_time': result[3],
                'clinic_id': result[4],
                'status': result[5],
                'created_at': result[6]
            })
        return orders
    
    def get_all_vet_orders(self) -> List[Dict]:
        """Barcha vet buyurtmalarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vet_orders ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        orders = []
        for result in results:
            orders.append({
                'order_id': result[0],
                'user_id': result[1],
                'pet_name': result[2],
                'pet_type': result[3],
                'service_type': result[4],
                'phone': result[5],
                'clinic_id': result[6],
                'status': result[7],
                'created_at': result[8]
            })
        return orders
    
    def get_all_training_orders(self) -> List[Dict]:
        """Barcha oqitish buyurtmalarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM training_orders ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        orders = []
        for result in results:
            orders.append({
                'order_id': result[0],
                'user_id': result[1],
                'course_name': result[2],
                'phone': result[3],
                'school_id': result[4],
                'name': result[5],
                'status': result[6],
                'created_at': result[7]
            })
        return orders
    
    def get_all_pet_sale_orders(self) -> List[Dict]:
        """Barcha sotish buyurtmalarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pet_sale_orders ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        orders = []
        for result in results:
            orders.append({
                'order_id': result[0],
                'user_id': result[1],
                'animal_type': result[2],
                'description': result[3],
                'phone': result[4],
                'status': result[5],
                'created_at': result[6]
            })
        return orders
    
    def get_all_daycare_orders(self) -> List[Dict]:
        """Barcha asrab turish buyurtmalarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM daycare_orders ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        orders = []
        for result in results:
            orders.append({
                'order_id': result[0],
                'user_id': result[1],
                'name': result[2],
                'phone': result[3],
                'animal_type': result[4],
                'status': result[5],
                'created_at': result[6]
            })
        return orders

# Database misoli
db = Database()