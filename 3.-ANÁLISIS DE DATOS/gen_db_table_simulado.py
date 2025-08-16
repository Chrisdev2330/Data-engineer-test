#!/usr/bin/env python3

import sqlite3
import random
from datetime import datetime, timedelta

def crear_base_datos():
    # Configuración
    DB_NAME = "casino_analytics.db"
    TOTAL_USUARIOS = 100
    
    PAISES = ['CHILE', 'MEXICO', 'COLOMBIA', 'PERU', 'ECUADOR', 'ARGENTINA', 'BRASIL', 'VENEZUELA', 'COSTA RICA']
    JUEGOS = ['Live Roulette', 'Bookofdead', 'Tomeofmadness', 'John Hunter And The Aztec', 'Mustang Gold', 
              'Gates Of Olympus', 'Sweet Bonanza', 'Fruit Cocktail', 'Crazy Time', 'Aviator', 'Blackjack', 'Poker']
    DISPOSITIVOS = ['Mobile', 'Desktop']
    
    fecha_actual = datetime.now()
    usuarios = []
    
    print("Generando usuarios...")
    
    # Generar 100 usuarios
    for user_id in range(1, TOTAL_USUARIOS + 1):
        perfil_random = random.random()
        
        if perfil_random < 0.15:  # 15% VIP
            dias_registro = random.randint(180, 720)
            deposit_count = random.randint(15, 100)
            avg_deposit = round(random.uniform(80, 300), 2)
            dias_ultimo_deposito = random.randint(1, 7)
            total_sessions = random.randint(100, 500)
            total_game_time = round(random.uniform(100, 800), 2)
            churn_risk = 0
            
        elif perfil_random < 0.35:  # 20% regulares
            dias_registro = random.randint(90, 365)
            deposit_count = random.randint(4, 20)
            avg_deposit = round(random.uniform(30, 100), 2)
            dias_ultimo_deposito = random.randint(5, 20)
            total_sessions = random.randint(30, 150)
            total_game_time = round(random.uniform(30, 200), 2)
            churn_risk = 0 if random.random() < 0.7 else 1
            
        elif perfil_random < 0.65:  # 30% casuales
            dias_registro = random.randint(60, 300)
            deposit_count = random.randint(1, 8)
            avg_deposit = round(random.uniform(15, 60), 2)
            dias_ultimo_deposito = random.randint(10, 45)
            total_sessions = random.randint(10, 60)
            total_game_time = round(random.uniform(5, 100), 2)
            churn_risk = 0 if random.random() < 0.4 else 1
            
        elif perfil_random < 0.80:  # 15% nuevos
            dias_registro = random.randint(1, 30)
            deposit_count = random.randint(0, 3)
            avg_deposit = round(random.uniform(10, 50), 2) if deposit_count > 0 else 0
            dias_ultimo_deposito = random.randint(1, dias_registro) if deposit_count > 0 else 0
            total_sessions = random.randint(1, 20)
            total_game_time = round(random.uniform(0.5, 30), 2)
            churn_risk = 0 if random.random() < 0.5 else 1
            
        else:  # 20% inactivos
            dias_registro = random.randint(120, 600)
            deposit_count = random.randint(2, 15)
            avg_deposit = round(random.uniform(20, 80), 2)
            dias_ultimo_deposito = random.randint(31, 180)
            total_sessions = random.randint(15, 80)
            total_game_time = round(random.uniform(10, 150), 2)
            churn_risk = 1
        
        fecha_registro = fecha_actual - timedelta(days=dias_registro)
        fecha_ultimo_deposito = None
        if deposit_count > 0 and dias_ultimo_deposito > 0:
            fecha_ultimo_deposito = fecha_actual - timedelta(days=dias_ultimo_deposito)
        
        usuario = {
            'user_id': user_id,
            'country': random.choice(PAISES),
            'registration_date': fecha_registro.strftime('%Y-%m-%d'),
            'deposit_count': deposit_count,
            'avg_deposit': avg_deposit,
            'last_deposit_date': fecha_ultimo_deposito.strftime('%Y-%m-%d') if fecha_ultimo_deposito else None,
            'total_sessions': total_sessions,
            'total_game_time': total_game_time,
            'favorite_game': random.choice(JUEGOS),
            'device_type': 'Mobile' if random.random() < 0.7 else 'Desktop',
            'churn_risk': churn_risk
        }
        
        usuarios.append(usuario)
    
    # Asegurar datos para queries
    print("Ajustando datos para queries...")
    
    # Query 1: usuarios con >3 depósitos y >5 horas/mes
    for i in range(10, 25):
        dias_reg = random.randint(60, 365)
        usuarios[i]['registration_date'] = (fecha_actual - timedelta(days=dias_reg)).strftime('%Y-%m-%d')
        usuarios[i]['deposit_count'] = random.randint(4, 50)
        meses = max(dias_reg / 30, 1)
        usuarios[i]['total_game_time'] = round(meses * random.uniform(6, 30), 2)
        usuarios[i]['churn_risk'] = 0
    
    # Query 2: usuarios inactivos 15-30 días
    for i in range(30, 45):
        usuarios[i]['deposit_count'] = random.randint(2, 30)
        dias_inactivo = random.randint(16, 30)
        usuarios[i]['last_deposit_date'] = (fecha_actual - timedelta(days=dias_inactivo)).strftime('%Y-%m-%d')
        usuarios[i]['avg_deposit'] = round(random.uniform(30, 150), 2)
    
    # Query 3: variedad de juegos
    for i in range(50, 70):
        usuarios[i]['favorite_game'] = JUEGOS[i % len(JUEGOS)]
        usuarios[i]['deposit_count'] = random.randint(1, 40)
    
    # Query 4: combinaciones país/dispositivo
    idx = 75
    for pais in PAISES[:5]:
        for dispositivo in DISPOSITIVOS:
            if idx < TOTAL_USUARIOS:
                usuarios[idx]['country'] = pais
                usuarios[idx]['device_type'] = dispositivo
                usuarios[idx]['deposit_count'] = random.randint(1, 30)
                usuarios[idx]['avg_deposit'] = round(random.uniform(20, 150), 2)
                idx += 1
    
    # Crear base de datos
    print(f"Creando base de datos {DB_NAME}...")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Eliminar tabla si existe
    cursor.execute("DROP TABLE IF EXISTS casino_users")
    
    # Crear tabla
    cursor.execute("""
        CREATE TABLE casino_users (
            user_id INTEGER PRIMARY KEY,
            country TEXT NOT NULL,
            registration_date DATE NOT NULL,
            deposit_count INTEGER DEFAULT 0,
            avg_deposit REAL DEFAULT 0,
            last_deposit_date DATE,
            total_sessions INTEGER DEFAULT 0,
            total_game_time REAL DEFAULT 0,
            favorite_game TEXT,
            device_type TEXT,
            churn_risk INTEGER DEFAULT 0
        )
    """)
    
    print("Insertando datos...")
    
    # Insertar datos
    for u in usuarios:
        cursor.execute("""
            INSERT INTO casino_users (
                user_id, country, registration_date, deposit_count,
                avg_deposit, last_deposit_date, total_sessions,
                total_game_time, favorite_game, device_type, churn_risk
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            u['user_id'], u['country'], u['registration_date'],
            u['deposit_count'], u['avg_deposit'], u['last_deposit_date'],
            u['total_sessions'], u['total_game_time'], u['favorite_game'],
            u['device_type'], u['churn_risk']
        ))
    
    # Crear índices para optimización
    print("Creando índices...")
    cursor.execute("CREATE INDEX idx_country ON casino_users(country)")
    cursor.execute("CREATE INDEX idx_deposit ON casino_users(deposit_count)")
    cursor.execute("CREATE INDEX idx_churn ON casino_users(churn_risk)")
    cursor.execute("CREATE INDEX idx_game ON casino_users(favorite_game)")
    cursor.execute("CREATE INDEX idx_device ON casino_users(device_type)")
    
    # Confirmar cambios
    conn.commit()
    
    # Verificar que se creó correctamente
    cursor.execute("SELECT COUNT(*) FROM casino_users")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM casino_users WHERE deposit_count > 0")
    con_depositos = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(avg_deposit) FROM casino_users WHERE deposit_count > 0")
    ticket_avg = cursor.fetchone()[0]
    
    print("\n" + "="*50)
    print(f"✓ Base de datos creada exitosamente: {DB_NAME}")
    print(f"✓ Tabla: casino_users")
    print(f"✓ Total usuarios: {total}")
    print(f"✓ Usuarios con depósitos: {con_depositos}")
    print(f"✓ Ticket promedio: ${ticket_avg:.2f}")
    print("="*50)
    print("\nLa base de datos está lista para usar en DBeaver")
    
    conn.close()

if __name__ == "__main__":
    try:
        crear_base_datos()
    except Exception as e:
        print(f"Error: {e}")
        print("Intenta ejecutar el script nuevamente")