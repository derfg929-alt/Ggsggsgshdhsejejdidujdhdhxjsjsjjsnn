# ============================================================
# config.py - КОНФИГУРАЦИЯ, БАЗА ДАННЫХ, МОДЕЛИ
# ============================================================

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import (create_engine, Column, Integer, String, Float, 
                        Boolean, DateTime, BigInteger, ForeignKey, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from contextlib import asynccontextmanager

# ============================================================
# КОНФИГУРАЦИЯ
# ============================================================

class Config:
    # Токен бота
    TOKEN = "ВАШ_ТОКЕН_БОТА"
    
    # ID администратора
    ADMIN_ID = 123456789
    
    # База данных PostgreSQL
    DB_USER = "postgres"
    DB_PASS = "your_password"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "economy_bot"
    
    @property
    def DB_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Экономические лимиты
    TOTAL_MONEY_LIMIT = 100_000_000  # 100 миллионов
    START_BALANCE = 1000  # Стартовый баланс
    
    # Зарплаты по профессиям (в час)
    SALARIES = {
        "Грузчик": 125,
        "Курьер": 250,
        "Таксист": 500,
        "Продавец": 1000,
        "Водитель фуры": 2000,
        "Владелец киоска": 4000,
        "Владелец кафе": 8000,
        "Владелец магазина": 16000,
        "Владелец ресторана": 32000,
        "Владелец сети": 64000,
    }
    
    # Майнеры: {название: {цена, монеты/час, btc/час, sol/час, ton/час, doge/час, trx/час}}
    MINERS = {
        "S9": {
            "price": 5000,
            "coins": 50,
            "btc": 0.00001,
            "sol": 0.0001,
            "ton": 0.001,
            "doge": 0.01,
            "trx": 0.1,
            "hashrate": "16 TH/s",
            "power": "1400 W",
            "description": "Базовый майнер для начинающих"
        },
        "S19": {
            "price": 25000,
            "coins": 150,
            "btc": 0.00005,
            "sol": 0.0005,
            "ton": 0.005,
            "doge": 0.05,
            "trx": 0.5,
            "hashrate": "95 TH/s",
            "power": "3250 W",
            "description": "Профессиональный майнер"
        },
        "S21": {
            "price": 100000,
            "coins": 400,
            "btc": 0.0002,
            "sol": 0.002,
            "ton": 0.02,
            "doge": 0.2,
            "trx": 2.0,
            "hashrate": "200 TH/s",
            "power": "3500 W",
            "description": "Продвинутый майнер"
        },
        "S29": {
            "price": 400000,
            "coins": 1000,
            "btc": 0.001,
            "sol": 0.01,
            "ton": 0.1,
            "doge": 1.0,
            "trx": 10.0,
            "hashrate": "500 TH/s",
            "power": "5000 W",
            "description": "Элитный майнер"
        },
        "S39": {
            "price": 1500000,
            "coins": 3000,
            "btc": 0.005,
            "sol": 0.05,
            "ton": 0.5,
            "doge": 5.0,
            "trx": 50.0,
            "hashrate": "1 PH/s",
            "power": "8000 W",
            "description": "Легендарный майнер"
        },
    }
    
    # Бизнесы: {название: {цена, доход/день, профессия}}
    BUSINESSES = {
        "киоск": {
            "price": 100000,
            "income": 4000,
            "profession": "Владелец киоска",
            "icon": "🏪",
            "description": "Маленький ларек с товарами"
        },
        "кафе": {
            "price": 200000,
            "income": 8000,
            "profession": "Владелец кафе",
            "icon": "☕",
            "description": "Уютное кафе в центре города"
        },
        "магазин": {
            "price": 400000,
            "income": 16000,
            "profession": "Владелец магазина",
            "icon": "🏬",
            "description": "Продуктовый магазин"
        },
        "ресторан": {
            "price": 800000,
            "income": 32000,
            "profession": "Владелец ресторана",
            "icon": "🍽️",
            "description": "Престижный ресторан"
        },
        "сеть": {
            "price": 1600000,
            "income": 64000,
            "profession": "Владелец сети",
            "icon": "🏢",
            "description": "Сеть магазинов по всему городу"
        },
    }
    
    # Вклады: {дни: процент}
    DEPOSIT_RATES = {
        1: 0.005,    # 0.5%
        7: 0.03,     # 3%
        30: 0.15,    # 15%
        90: 0.50,    # 50%
        180: 1.00,   # 100%
        365: 2.50,   # 250%
    }
    
    # Кредиты
    CREDIT_RATE = 0.20  # 20%
    CREDIT_DAYS = 30
    PENALTY_RATE = 0.02  # 2% в день просрочки
    
    # Криптовалюты: {символ: {название, цена, иконка}}
    CRYPTO = {
        "btc": {
            "name": "Bitcoin",
            "price": 50000,
            "icon": "₿",
            "volatility": 0.15,  # Волатильность 15%
        },
        "sol": {
            "name": "Solana",
            "price": 100,
            "icon": "◎",
            "volatility": 0.25,
        },
        "ton": {
            "name": "Toncoin",
            "price": 5,
            "icon": "💎",
            "volatility": 0.20,
        },
        "doge": {
            "name": "Dogecoin",
            "price": 0.1,
            "icon": "🐕",
            "volatility": 0.40,
        },
        "trx": {
            "name": "TRON",
            "price": 0.08,
            "icon": "▲",
            "volatility": 0.30,
        },
    }
    
    # Недвижимость
    REAL_ESTATE = {
        "студия": {"price": 500000, "income": 5000, "icon": "🏠"},
        "1-комнатная": {"price": 1000000, "income": 10000, "icon": "🏡"},
        "2-комнатная": {"price": 2000000, "income": 20000, "icon": "🏘️"},
        "3-комнатная": {"price": 4000000, "income": 40000, "icon": "🏚️"},
        "пентхаус": {"price": 10000000, "income": 100000, "icon": "🏰"},
        "коттедж": {"price": 15000000, "income": 150000, "icon": "🏛️"},
        "вилла": {"price": 30000000, "income": 300000, "icon": "🌴"},
        "особняк": {"price": 50000000, "income": 500000, "icon": "🏯"},
        "замок": {"price": 100000000, "income": 1000000, "icon": "🏰"},
    }
    
    # Транспорт
    VEHICLES = {
        "велосипед": {"price": 500, "speed_bonus": 0.05, "icon": "🚲"},
        "самокат": {"price": 1000, "speed_bonus": 0.08, "icon": "🛴"},
        "мотоцикл": {"price": 5000, "speed_bonus": 0.12, "icon": "🏍️"},
        "лада": {"price": 10000, "speed_bonus": 0.15, "icon": "🚗"},
        "kia": {"price": 25000, "speed_bonus": 0.18, "icon": "🚙"},
        "toyota": {"price": 50000, "speed_bonus": 0.20, "icon": "🚘"},
        "bmw": {"price": 100000, "speed_bonus": 0.25, "icon": "🏎️"},
        "mercedes": {"price": 200000, "speed_bonus": 0.30, "icon": "🚗"},
        "tesla": {"price": 500000, "speed_bonus": 0.35, "icon": "⚡"},
        "lamborghini": {"price": 1000000, "speed_bonus": 0.40, "icon": "🏎️"},
        "bugatti": {"price": 5000000, "speed_bonus": 0.50, "icon": "💎"},
        "вертолёт": {"price": 10000000, "speed_bonus": 0.60, "icon": "🚁"},
        "самолёт": {"price": 50000000, "speed_bonus": 0.80, "icon": "✈️"},
    }
    
    # Уровни и опыт
    LEVELS = {
        level: {
            "exp_required": level * 1000,
            "title": title
        }
        for level, title in enumerate([
            "Новичок", "Ученик", "Любитель", "Специалист", "Эксперт",
            "Мастер", "Профессионал", "Гуру", "Магнат", "Олигарх"
        ], start=1)
    }

config = Config()

# ============================================================
# БАЗА ДАННЫХ
# ============================================================

Base = declarative_base()
engine = create_engine(config.DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# ============================================================
# МОДЕЛИ ТАБЛИЦ
# ============================================================

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(100))
    first_name = Column(String(100))
    balance = Column(Float, default=config.START_BALANCE)
    profession = Column(String(50), default="Безработный")
    level = Column(Integer, default=1)
    experience = Column(Float, default=0)
    total_earned = Column(Float, default=0)  # Всего заработано
    total_spent = Column(Float, default=0)  # Всего потрачено
    warnings = Column(Integer, default=0)
    mute_until = Column(DateTime, nullable=True)
    is_premium = Column(Boolean, default=False)
    prestige = Column(Integer, default=0)  # Престиж
    referral_id = Column(BigInteger, nullable=True)  # Кто пригласил
    referral_code = Column(String(20), unique=True)  # Свой код
    skin = Column(String(50), default='default')
    title = Column(String(50), default='')
    created_at = Column(DateTime, default=func.now())
    last_work = Column(DateTime, nullable=True)
    last_daily = Column(DateTime, nullable=True)

class Miner(Base):
    __tablename__ = 'miners'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False, index=True)
    model = Column(String(10), nullable=False)
    quantity = Column(Integer, default=1)
    purchase_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)

class Business(Base):
    __tablename__ = 'businesses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False, index=True)
    business_type = Column(String(50), nullable=False)
    quantity = Column(Integer, default=1)
    income_collected = Column(Boolean, default=False)
    last_income = Column(DateTime, nullable=True)
    purchase_date = Column(DateTime, default=func.now())

class Deposit(Base):
    __tablename__ = 'deposits'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    amount = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    days = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    early_withdraw = Column(Boolean, default=False)

class Loan(Base):
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    amount = Column(Float, nullable=False)
    debt = Column(Float, nullable=False)  # Остаток долга
    rate = Column(Float, default=config.CREDIT_RATE)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    overdue_days = Column(Integer, default=0)

class CryptoHolding(Base):
    __tablename__ = 'crypto_holdings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False, index=True)
    symbol = Column(String(10), nullable=False)
    amount = Column(Float, default=0)
    total_invested = Column(Float, default=0)  # Сколько потрачено на покупку

class Promocode(Base):
    __tablename__ = 'promocodes'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    reward = Column(Float, nullable=False)
    max_uses = Column(Integer, nullable=False)
    used = Column(Integer, default=0)
    created_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=func.now())
    active = Column(Boolean, default=True)

class UsedPromocode(Base):
    __tablename__ = 'used_promocodes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    code = Column(String(50), nullable=False)
    used_at = Column(DateTime, default=func.now())

class AuctionLot(Base):
    __tablename__ = 'auction_lots'
    
    id = Column(Integer, primary_key=True)
    seller_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    item_type = Column(String(50), nullable=False)  # miner, business, crypto, vehicle, real_estate
    item_name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)
    start_price = Column(Float, nullable=False)
    current_bid = Column(Float, nullable=True)
    buyer_id = Column(BigInteger, nullable=True)
    end_time = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class Corporation(Base):
    __tablename__ = 'corporations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    owner_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    fund = Column(Float, default=0)
    level = Column(Integer, default=1)
    members_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())

class CorporationMember(Base):
    __tablename__ = 'corporation_members'
    
    id = Column(Integer, primary_key=True)
    corp_id = Column(Integer, ForeignKey('corporations.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    contribution = Column(Float, default=0)
    joined_at = Column(DateTime, default=func.now())

class InflationLog(Base):
    __tablename__ = 'inflation_log'
    
    id = Column(Integer, primary_key=True)
    total_supply = Column(Float, nullable=False)
    rate = Column(Float, default=1.0)
    action = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=func.now())

# Новые таблицы для расширенных функций
class RealEstate(Base):
    __tablename__ = 'real_estate'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    estate_type = Column(String(50), nullable=False)
    quantity = Column(Integer, default=1)
    purchase_date = Column(DateTime, default=func.now())

class Vehicle(Base):
    __tablename__ = 'vehicles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    vehicle_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    purchase_date = Column(DateTime, default=func.now())

class Achievement(Base):
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    icon = Column(String(10), nullable=False)
    is_hidden = Column(Boolean, default=False)
    tiers = Column(Text)  # JSON строка
    order = Column(Integer, default=0)

class UserAchievement(Base):
    __tablename__ = 'user_achievements'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    achievement_code = Column(String(50), nullable=False)
    tier = Column(Integer, default=1)
    progress = Column(Float, default=0)
    goal = Column(Float, default=0)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    is_new = Column(Boolean, default=True)

class Clan(Base):
    __tablename__ = 'clans'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    tag = Column(String(10), unique=True, nullable=False)
    description = Column(String(500))
    owner_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Float, default=0)
    balance = Column(Float, default=0)
    max_members = Column(Integer, default=20)
    created_at = Column(DateTime, default=func.now())
    is_open = Column(Boolean, default=True)

class ClanMember(Base):
    __tablename__ = 'clan_members'
    
    id = Column(Integer, primary_key=True)
    clan_id = Column(Integer, ForeignKey('clans.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    role = Column(String(20), default='member')
    contribution = Column(Float, default=0)
    joined_at = Column(DateTime, default=func.now())

class Robbery(Base):
    __tablename__ = 'robberies'
    
    id = Column(Integer, primary_key=True)
    robber_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    victim_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    amount_stolen = Column(Float, default=0)
    success = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=func.now())

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    type = Column(String(50), nullable=False)  # income, expense, transfer
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)  # work, mining, business, casino, etc.
    description = Column(String(255))
    timestamp = Column(DateTime, default=func.now())

# ============================================================
# ФУНКЦИИ РАБОТЫ С БАЗОЙ ДАННЫХ
# ============================================================

@asynccontextmanager
async def get_session():
    """Контекстный менеджер для сессий БД"""
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()

async def init_db():
    """Создание всех таблиц"""
    Base.metadata.create_all(engine)
    print("✅ База данных создана")

async def get_user(user_id: int) -> Optional[User]:
    """Получить пользователя по ID"""
    async with get_session() as session:
        user = await session.query(User).filter(User.user_id == user_id).first()
        return user

async def register_user(user_id: int, username: str, first_name: str) -> User:
    """Регистрация нового пользователя"""
    async with get_session() as session:
        # Генерируем реферальный код
        import secrets
        ref_code = secrets.token_hex(4).upper()
        
        user = User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            balance=config.START_BALANCE,
            referral_code=ref_code
        )
        session.add(user)
        await session.flush()
        return user

async def update_balance(user_id: int, amount: float, operation: str = 'add') -> User:
    """Обновление баланса пользователя"""
    async with get_session() as session:
        user = await session.query(User).filter(User.user_id == user_id).first()
        if user:
            if operation == 'add':
                user.balance += amount
                user.total_earned += amount if amount > 0 else 0
            elif operation == 'subtract':
                user.balance -= amount
                user.total_spent += amount
            elif operation == 'set':
                user.balance = amount
            
            # Обновление опыта
            user.experience += abs(amount) * 0.01
            
            # Проверка повышения уровня
            await check_level_up(user)
            
            return user
        return None

async def check_level_up(user: User):
    """Проверка и повышение уровня"""
    next_level = user.level + 1
    if next_level in config.LEVELS:
        required = config.LEVELS[next_level]['exp_required']
        if user.experience >= required:
            user.level = next_level
            user.experience -= required
            # Отправляем уведомление
            try:
                from aiogram import Bot
                bot = Bot.get_current()
                await bot.send_message(
                    user.user_id,
                    f"🎉 ПОЗДРАВЛЯЕМ!\n"
                    f"Вы достигли {next_level} уровня!\n"
                    f"🏅 Новый титул: {config.LEVELS[next_level]['title']}"
                )
            except:
                pass

async def add_miner(user_id: int, model: str) -> Miner:
    """Добавление майнера"""
    async with get_session() as session:
        miner = Miner(user_id=user_id, model=model)
        session.add(miner)
        await session.flush()
        return miner

async def get_miners(user_id: int) -> List[Miner]:
    """Получить майнеры пользователя"""
    async with get_session() as session:
        miners = await session.query(Miner).filter(Miner.user_id == user_id).all()
        return miners

async def add_business(user_id: int, business_type: str) -> Business:
    """Добавление бизнеса"""
    async with get_session() as session:
        business = Business(user_id=user_id, business_type=business_type)
        session.add(business)
        await session.flush()
        return business

async def get_businesses(user_id: int) -> List[Business]:
    """Получить бизнесы пользователя"""
    async with get_session() as session:
        businesses = await session.query(Business).filter(Business.user_id == user_id).all()
        return businesses

async def get_user_crypto(user_id: int) -> List[CryptoHolding]:
    """Получить криптовалюты пользователя"""
    async with get_session() as session:
        crypto = await session.query(CryptoHolding).filter(CryptoHolding.user_id == user_id).all()
        return crypto

async def update_crypto(user_id: int, symbol: str, amount: float, operation: str = 'add') -> CryptoHolding:
    """Обновление криптовалюты пользователя"""
    async with get_session() as session:
        holding = await session.query(CryptoHolding).filter(
            CryptoHolding.user_id == user_id,
            CryptoHolding.symbol == symbol
        ).first()
        
        if not holding and operation == 'add':
            holding = CryptoHolding(user_id=user_id, symbol=symbol, amount=0)
            session.add(holding)
        
        if holding:
            if operation == 'add':
                holding.amount += amount
            elif operation == 'subtract':
                holding.amount -= amount
            elif operation == 'set':
                holding.amount = amount
            
            if holding.amount <= 0:
                await session.delete(holding)
        
        return holding

async def get_total_money_supply() -> float:
    """Получить общее количество монет в системе"""
    async with get_session() as session:
        result = await session.query(func.sum(User.balance)).scalar()
        return result or 0

async def add_transaction(user_id: int, type_: str, amount: float, category: str, description: str = ""):
    """Добавление транзакции в историю"""
    async with get_session() as session:
        transaction = Transaction(
            user_id=user_id,
            type=type_,
            amount=amount,
            category=category,
            description=description
        )
        session.add(transaction)

print("📦 config.py загружен")
print(f"   База данных: {config.DB_NAME}")
print(f"   Лимит монет: {config.TOTAL_MONEY_LIMIT:,}")
print(f"   Профессий: {len(config.SALARIES)}")
print(f"   Майнеров: {len(config.MINERS)}")
print(f"   Бизнесов: {len(config.BUSINESSES)}")
print(f"   Криптовалют: {len(config.CRYPTO)}")
print(f"   Недвижимости: {len(config.REAL_ESTATE)}")
print(f"   Транспорта: {len(config.VEHICLES)}")
# ============================================================
# game_mechanics.py - ИГРОВАЯ МЕХАНИКА И КАЗИНО
# ============================================================

import random
import asyncio
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from aiogram import types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import *

# ============================================================
# ГЛОБАЛЬНЫЕ ХРАНИЛИЩА
# ============================================================
mining_buffers = {}       # {user_id: {currency: amount, last_mine: datetime}}
active_crash_games = {}   # {user_id: {bet, multiplier, active, start_time}}
active_blackjack = {}     # {user_id: {deck, player_hand, dealer_hand, bet, game_over}}
active_poker_tables = {}  # {table_id: {players, deck, pot, community_cards, phase}}
active_mines_games = {}   # {user_id: {bet, grid, mines_count, revealed, multiplier, game_over}}
active_redblack = {}      # {user_id: {bet, deck, current_card, multiplier, game_over, history}}
robbery_cooldowns = {}    # {user_id: last_robbery_time}
work_cooldowns = {}       # {user_id: last_work_time}
lottery_pool = 0          # Джекпот лотереи
lottery_tickets = {}      # {user_id: [ticket_numbers]}

# ============================================================
# КЛАССЫ ИГР
# ============================================================

class CasinoGames:
    """Все игры казино"""
    
    # ============================================================
    # РУЛЕТКА
    # ============================================================
    
    ROULETTE_NUMBERS = list(range(37))  # 0-36
    RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    
    @staticmethod
    def spin_roulette() -> int:
        """Крутить рулетку, возвращает число 0-36"""
        return random.randint(0, 36)
    
    @staticmethod
    def get_color(number: int) -> str:
        """Получить цвет числа"""
        if number == 0:
            return 'green'
        return 'red' if number in CasinoGames.RED_NUMBERS else 'black'
    
    @staticmethod
    def calculate_roulette_payout(bet_type: str, bet_amount: float, 
                                  number: int, bet_value: str = None) -> float:
        """Рассчитать выплату в рулетке"""
        color = CasinoGames.get_color(number)
        is_even = number % 2 == 0
        
        payouts = {
            'число': lambda: bet_amount * 36 if str(number) == bet_value else 0,
            'цвет': lambda: bet_amount * 2 if color == bet_value else 0,
            'чёт': lambda: bet_amount * 2 if is_even and number != 0 else 0,
            'нечет': lambda: bet_amount * 2 if not is_even and number != 0 else 0,
            'малое': lambda: bet_amount * 2 if 1 <= number <= 18 else 0,
            'большое': lambda: bet_amount * 2 if 19 <= number <= 36 else 0,
            'дюжина1': lambda: bet_amount * 3 if 1 <= number <= 12 else 0,
            'дюжина2': lambda: bet_amount * 3 if 13 <= number <= 24 else 0,
            'дюжина3': lambda: bet_amount * 3 if 25 <= number <= 36 else 0,
        }
        
        payout_func = payouts.get(bet_type)
        return payout_func() if payout_func else 0
    
    @staticmethod
    def roulette_board_visual(number: int) -> str:
        """Визуализация рулетки"""
        color = CasinoGames.get_color(number)
        color_emoji = {'red': '🔴', 'black': '⚫', 'green': '🟢'}
        
        board = f"""
╔══════════════════════════╗
║     🎰 РУЛЕТКА 🎰      ║
╠══════════════════════════╣
║                          ║
║       {color_emoji[color]}  {number:2d}  {color_emoji[color]}      ║
║                          ║
╠══════════════════════════╣
║ {color_emoji['red']} КРАСНЫЕ  ⚫ ЧЁРНЫЕ ║
║ 1 3 5 7 9  2 4 6 8 10  ║
║ 12 14 16  11 13 15 17   ║
║ 18 19 21  20 22 24 26   ║
║ 23 25 27  28 29 31 33   ║
║ 30 32 34  35 36         ║
║ {color_emoji['green']} 0 - ЗЕРО            ║
╚══════════════════════════╝
"""
        return board
    
    # ============================================================
    # КУБЫ (DICE)
    # ============================================================
    
    @staticmethod
    def roll_dice(count: int = 1) -> List[int]:
        """Бросок кубиков"""
        return [random.randint(1, 6) for _ in range(count)]
    
    @staticmethod
    def dice_visual(values: List[int]) -> str:
        """Визуализация кубиков"""
        dice_faces = {
            1: "⚀", 2: "⚁", 3: "⚂",
            4: "⚃", 5: "⚄", 6: "⚅"
        }
        
        dice_art = {
            1: ["┌─────┐", "│     │", "│  ●  │", "│     │", "└─────┘"],
            2: ["┌─────┐", "│ ●   │", "│     │", "│   ● │", "└─────┘"],
            3: ["┌─────┐", "│ ●   │", "│  ●  │", "│   ● │", "└─────┘"],
            4: ["┌─────┐", "│ ● ● │", "│     │", "│ ● ● │", "└─────┘"],
            5: ["┌─────┐", "│ ● ● │", "│  ●  │", "│ ● ● │", "└─────┘"],
            6: ["┌─────┐", "│ ● ● │", "│ ● ● │", "│ ● ● │", "└─────┘"],
        }
        
        result = ""
        for line in range(5):
            for value in values:
                result += dice_art[value][line] + " "
            result += "\n"
        
        result += f"Сумма: {sum(values)} {' '.join(dice_faces[v] for v in values)}"
        return result
    
    # ============================================================
    # СЛОТЫ
    # ============================================================
    
    SLOT_SYMBOLS = {
        '🍒': {'multiplier': 2, 'weight': 30},   # Частый
        '🍋': {'multiplier': 2, 'weight': 25},
        '🍊': {'multiplier': 2, 'weight': 20},
        '🍇': {'multiplier': 3, 'weight': 15},
        '💎': {'multiplier': 10, 'weight': 5},    # Редкий
        '🔔': {'multiplier': 5, 'weight': 8},
        '⭐': {'multiplier': 20, 'weight': 2},    # Очень редкий
        '7️⃣': {'multiplier': 50, 'weight': 1},   # Джекпот
    }
    
    @staticmethod
    def spin_slots() -> List[str]:
        """Крутить слоты (3x3)"""
        symbols = []
        weights = []
        for symbol, data in CasinoGames.SLOT_SYMBOLS.items():
            symbols.append(symbol)
            weights.append(data['weight'])
        
        # Генерируем 3x3 поле
        grid = []
        for _ in range(3):
            row = random.choices(symbols, weights=weights, k=3)
            grid.append(row)
        
        return grid
    
    @staticmethod
    def calculate_slot_payout(grid: List[List[str]], bet: float) -> Tuple[float, str]:
        """Рассчитать выплату в слотах"""
        total_payout = 0
        win_lines = []
        
        # Проверяем горизонтальные линии
        for i, row in enumerate(grid):
            if len(set(row)) == 1:  # Все 3 одинаковые
                symbol = row[0]
                multiplier = CasinoGames.SLOT_SYMBOLS[symbol]['multiplier']
                payout = bet * multiplier
                total_payout += payout
                win_lines.append(f"Линия {i+1}: {symbol}x3 = x{multiplier}")
            elif len(set(row)) == 2:  # 2 одинаковые
                for symbol in set(row):
                    if row.count(symbol) == 2:
                        payout = bet * 2  # x2 за пару
                        total_payout += payout
                        win_lines.append(f"Линия {i+1}: {symbol}x2 = x2")
        
        # Проверяем диагонали
        diag1 = [grid[0][0], grid[1][1], grid[2][2]]
        diag2 = [grid[0][2], grid[1][1], grid[2][0]]
        
        for diag_name, diag in [("Диагональ 1", diag1), ("Диагональ 2", diag2)]:
            if len(set(diag)) == 1:
                symbol = diag[0]
                multiplier = CasinoGames.SLOT_SYMBOLS[symbol]['multiplier'] * 1.5
                payout = bet * multiplier
                total_payout += payout
                win_lines.append(f"{diag_name}: {symbol}x3 = x{multiplier:.1f}")
        
        return total_payout, "\n".join(win_lines) if win_lines else "Нет выигрышных линий"
    
    @staticmethod
    def slots_visual(grid: List[List[str]], spinning: bool = False) -> str:
        """Визуализация слотов"""
        if spinning:
            frames = [
                ["🍒", "🍋", "🍊"],
                ["🍇", "💎", "🔔"],
                ["⭐", "7️⃣", "🍒"],
            ]
            import random as rnd
            grid = [[rnd.choice(list(CasinoGames.SLOT_SYMBOLS.keys())) for _ in range(3)] for _ in range(3)]
        
        border_top = "╔═══════╦═══════╦═══════╗"
        border_mid = "╠═══════╬═══════╬═══════╣"
        border_bot = "╚═══════╩═══════╩═══════╝"
        
        rows = []
        for row in grid:
            rows.append(f"║   {row[0]}   ║   {row[1]}   ║   {row[2]}   ║")
        
        return f"{border_top}\n{rows[0]}\n{border_mid}\n{rows[1]}\n{border_mid}\n{rows[2]}\n{border_bot}"
    
    # ============================================================
    # КРАШ (CRASH)
    # ============================================================
    
    @staticmethod
    def generate_crash_point() -> float:
        """Генерация точки краша"""
        # Используем формулу: шанс краша = 1 / (множитель * 0.99)
        r = random.random()
        if r < 0.01:  # 1% шанс мгновенного краша
            return 1.0
        
        crash_point = math.floor(0.99 / (1 - r) * 100) / 100
        return max(1.0, min(crash_point, 1000.0))
    
    @staticmethod
    async def crash_animation(message: types.Message, bet: float, bot: Bot) -> float:
        """Анимация игры Краш"""
        user_id = message.from_user.id
        crash_point = CasinoGames.generate_crash_point()
        current_multiplier = 1.0
        
        active_crash_games[user_id] = {
            'bet': bet,
            'multiplier': current_multiplier,
            'crash_point': crash_point,
            'active': True,
            'cashed_out': False
        }
        
        # Отправляем начальное сообщение
        progress_bar = CasinoGames.crash_progress_bar(current_multiplier, crash_point)
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="💰 ЗАБРАТЬ!", callback_data="crash_cashout")
        
        msg = await message.answer(
            f"📈 КРАШ\n"
            f"💰 Ставка: {bet:,.0f} монет\n"
            f"📊 Множитель: x{current_multiplier:.2f}\n"
            f"💵 Потенциальный выигрыш: {bet * current_multiplier:,.0f}\n"
            f"{progress_bar}",
            reply_markup=keyboard.as_markup()
        )
        
        # Обновляем каждую секунду
        while current_multiplier < crash_point and current_multiplier < 60:
            await asyncio.sleep(1)
            current_multiplier += 0.1 * random.uniform(0.5, 2.0)
            current_multiplier = round(current_multiplier, 2)
            
            if user_id in active_crash_games and not active_crash_games[user_id].get('cashed_out'):
                active_crash_games[user_id]['multiplier'] = current_multiplier
                
                progress_bar = CasinoGames.crash_progress_bar(current_multiplier, crash_point)
                
                try:
                    await msg.edit_text(
                        f"📈 КРАШ\n"
                        f"💰 Ставка: {bet:,.0f} монет\n"
                        f"📊 Множитель: x{current_multiplier:.2f}\n"
                        f"💵 Потенциальный выигрыш: {bet * current_multiplier:,.0f}\n"
                        f"{progress_bar}",
                        reply_markup=keyboard.as_markup()
                    )
                except:
                    break
        
        # Краш или авто-кэшаут
        if user_id in active_crash_games:
            if not active_crash_games[user_id].get('cashed_out'):
                if current_multiplier >= 60:
                    # Авто-кэшаут на 60 секундах
                    final_multiplier = 60.0
                    winnings = bet * final_multiplier
                    active_crash_games[user_id]['cashed_out'] = True
                    
                    await msg.edit_text(
                        f"🎉 АВТО-ЗАБОР!\n"
                        f"📊 Множитель: x{final_multiplier:.2f}\n"
                        f"💰 Выигрыш: {winnings:,.0f} монет",
                        reply_markup=None
                    )
                    
                    return winnings
                else:
                    # КРАШ!
                    await msg.edit_text(
                        f"💥 КРАШ на x{crash_point:.2f}!\n"
                        f"💸 Потеряно: {bet:,.0f} монет",
                        reply_markup=None
                    )
                    return 0
        
        return 0
    
    @staticmethod
    def crash_progress_bar(current: float, crash_point: float, length: int = 20) -> str:
        """Прогресс-бар для Краш"""
        progress = min(current / crash_point, 1.0)
        filled = int(progress * length)
        
        if progress < 0.3:
            color_start, color_end = "🟢", "🟢"
        elif progress < 0.6:
            color_start, color_end = "🟡", "🟡"
        elif progress < 0.8:
            color_start, color_end = "🟠", "🟠"
        else:
            color_start, color_end = "🔴", "🔴"
        
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}] x{current:.2f}"
    
    # ============================================================
    # БЛЭКДЖЕК (21 ОЧКО)
    # ============================================================
    
    @staticmethod
    def create_deck() -> List[str]:
        """Создание колоды из 52 карт"""
        suits = ['♥', '♦', '♠', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck
    
    @staticmethod
    def card_value(card: str) -> int:
        """Получить значение карты"""
        rank = card[:-1]
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        else:
            return int(rank)
    
    @staticmethod
    def hand_value(hand: List[str]) -> int:
        """Подсчёт очков в руке"""
        value = sum(CasinoGames.card_value(card) for card in hand)
        # Учитываем тузы
        aces = sum(1 for card in hand if card[:-1] == 'A')
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value
    
    @staticmethod
    def hand_visual(hand: List[str], hidden: bool = False) -> str:
        """Визуализация карт"""
        if not hand:
            return "Пусто"
        
        if hidden:
            return f"{hand[0]} 🂠"
        
        return " ".join(hand)
    
    @staticmethod
    def blackjack_keyboard(game_over: bool = False, can_split: bool = False) -> InlineKeyboardMarkup:
        """Клавиатура для блэкджека"""
        builder = InlineKeyboardBuilder()
        
        if not game_over:
            builder.row(
                InlineKeyboardButton(text="👊 ВЗЯТЬ", callback_data="bj_hit"),
                InlineKeyboardButton(text="✋ ХВАТИТ", callback_data="bj_stand"),
                width=2
            )
            builder.row(
                InlineKeyboardButton(text="📈 УДВОИТЬ", callback_data="bj_double")
            )
            if can_split:
                builder.row(
                    InlineKeyboardButton(text="✂️ СПЛИТ", callback_data="bj_split")
                )
        else:
            builder.row(
                InlineKeyboardButton(text="🔄 НОВАЯ ИГРА", callback_data="bj_new")
            )
        
        return builder.as_markup()
    
    # ============================================================
    # САПЁР (MINES)
    # ============================================================
    
    @staticmethod
    def generate_mines_grid(mines_count: int) -> List[List[int]]:
        """Генерация поля сапёра 5x5"""
        cells = [0] * 25
        mine_positions = random.sample(range(25), mines_count)
        for pos in mine_positions:
            cells[pos] = -1
        
        grid = []
        for i in range(0, 25, 5):
            grid.append(cells[i:i+5])
        
        return grid
    
    @staticmethod
    def mines_keyboard(grid: List[List[int]], revealed: Set[Tuple[int, int]], 
                       game_over: bool = False) -> InlineKeyboardMarkup:
        """Клавиатура для сапёра"""
        builder = InlineKeyboardBuilder()
        
        for i in range(5):
            row_buttons = []
            for j in range(5):
                pos = (i, j)
                
                if game_over:
                    text = "💣" if grid[i][j] == -1 else "💎" if pos in revealed else "⬜"
                    callback = "mine_gameover"
                elif pos in revealed:
                    text = "💎"
                    callback = "mine_revealed"
                else:
                    text = "🟦"
                    callback = f"mine_{i}_{j}"
                
                row_buttons.append(InlineKeyboardButton(text=text, callback_data=callback))
            
            builder.row(*row_buttons, width=5)
        
        if not game_over:
            builder.row(InlineKeyboardButton(text="💰 ЗАБРАТЬ", callback_data="mine_cashout"))
        else:
            builder.row(InlineKeyboardButton(text="🔄 НОВАЯ ИГРА", callback_data="mine_new"))
        
        return builder.as_markup()
    
    # ============================================================
    # КРАСНЫЙ / ЧЁРНЫЙ
    # ============================================================
    
    @staticmethod
    def redblack_keyboard(can_continue: bool = True) -> InlineKeyboardMarkup:
        """Клавиатура для Красный/Чёрный"""
        builder = InlineKeyboardBuilder()
        
        if can_continue:
            builder.row(
                InlineKeyboardButton(text="🔴 КРАСНЫЙ", callback_data="rb_red"),
                InlineKeyboardButton(text="⚫ ЧЁРНЫЙ", callback_data="rb_black"),
                width=2
            )
            builder.row(InlineKeyboardButton(text="💰 ЗАБРАТЬ", callback_data="rb_cashout"))
        else:
            builder.row(InlineKeyboardButton(text="🔄 НОВАЯ ИГРА", callback_data="rb_new"))
        
        return builder.as_markup()
    
    # ============================================================
    # ЛОТЕРЕЯ
    # ============================================================
    
    @staticmethod
    def generate_lottery_numbers(count: int = 6) -> List[int]:
        """Генерация чисел для лотереи"""
        return sorted(random.sample(range(1, 46), count))
    
    @staticmethod
    def check_lottery_wins(player_numbers: List[int], winning_numbers: List[int]) -> Tuple[int, float]:
        """Проверка выигрыша в лотерее"""
        matches = len(set(player_numbers) & set(winning_numbers))
        
        payouts = {
            3: 0.5,   # 50% возврат
            4: 2.0,   # x2
            5: 10.0,  # x10
            6: 100.0, # x100 (джекпот)
        }
        
        return matches, payouts.get(matches, 0)

# ============================================================
# СИСТЕМА КЕЙСОВ
# ============================================================

class CaseSystem:
    """Система кейсов (как в CS:GO)"""
    
    CASES = {
        "обычный кейс": {
            "price": 1000,
            "icon": "📦",
            "drops": {
                "💩 Мусор": {"chance": 40, "value": 100},
                "🔧 Инструмент": {"chance": 30, "value": 500},
                "⛏ Майнер S9": {"chance": 15, "value": 5000},
                "💎 Бриллиант": {"chance": 10, "value": 5000},
                "🏪 Киоск": {"chance": 4, "value": 100000},
                "👑 Золотой майнер": {"chance": 1, "value": 500000},
            }
        },
        "редкий кейс": {
            "price": 10000,
            "icon": "🎁",
            "drops": {
                "🔧 Инструмент": {"chance": 30, "value": 500},
                "⛏ Майнер S21": {"chance": 25, "value": 100000},
                "💎 Бриллиант": {"chance": 20, "value": 5000},
                "🏎️ BMW": {"chance": 12, "value": 100000},
                "🏠 Коттедж": {"chance": 8, "value": 15000000},
                "👑 Легендарный майнер": {"chance": 4, "value": 1500000},
                "🔥 Мистический предмет": {"chance": 1, "value": 10000000},
            }
        },
        "элитный кейс": {
            "price": 100000,
            "icon": "💎",
            "drops": {
                "⛏ Майнер S29": {"chance": 30, "value": 400000},
                "🏰 Замок": {"chance": 20, "value": 100000000},
                "✈️ Самолёт": {"chance": 18, "value": 50000000},
                "💎 Алмаз": {"chance": 15, "value": 100000},
                "👑 Золотой бизнес": {"chance": 10, "value": 10000000},
                "🔥 Легендарный предмет": {"chance": 5, "value": 50000000},
                "🌟 Мифический дроп": {"chance": 2, "value": 100000000},
            }
        }
    }
    
    @staticmethod
    def open_case(case_type: str) -> Tuple[str, float]:
        """Открыть кейс, возвращает (предмет, стоимость)"""
        if case_type not in CaseSystem.CASES:
            return None, 0
        
        case = CaseSystem.CASES[case_type]
        drops = case['drops']
        
        # Рулетка выбора предмета
        items = list(drops.keys())
        weights = [drops[item]['chance'] for item in items]
        
        chosen = random.choices(items, weights=weights, k=1)[0]
        value = drops[chosen]['value']
        
        return chosen, value
    
    @staticmethod
    def case_opening_animation(case_type: str) -> str:
        """Анимация открытия кейса"""
        frames = [
            "📦 Открываем...",
            "📦✨ Вскрываем...",
            "📦💫 Смотрим...",
            "📦🌟 Почти...",
        ]
        
        case = CaseSystem.CASES[case_type]
        items = list(case['drops'].keys())
        
        # Прокрутка предметов
        scroll_items = random.sample(items, min(5, len(items)))
        scroll_text = "\n".join(f"➤ {item}" for item in scroll_items)
        
        return f"""
╔══════════════════════╗
║  {case['icon']} {case_type.upper()}  ║
╠══════════════════════╣
║                      ║
{scroll_text}
║                      ║
║  ⬇ Открытие... ⬇   ║
╚══════════════════════╝
"""

# ============================================================
# СИСТЕМА ТУРНИРОВ
# ============================================================

class TournamentSystem:
    """Система турниров"""
    
    ACTIVE_TOURNAMENTS = {}  # {tournament_id: {info}}
    
    TOURNAMENT_TYPES = {
        "покер": {
            "name": "♠️ Покерный турнир",
            "buy_in": 10000,
            "max_players": 9,
            "duration": 3600,  # 1 час
            "prize_distribution": [0.50, 0.30, 0.20],  # 1-е, 2-е, 3-е места
        },
        "рулетка": {
            "name": "🎰 Турнир по рулетке",
            "buy_in": 5000,
            "max_players": 16,
            "duration": 1800,  # 30 минут
            "prize_distribution": [0.60, 0.25, 0.15],
        },
        "краш": {
            "name": "📈 Краш-турнир",
            "buy_in": 2000,
            "max_players": 100,
            "duration": 900,  # 15 минут
            "prize_distribution": [0.40, 0.25, 0.15, 0.10, 0.10],
        },
        "слоты": {
            "name": "🎰 Слот-турнир",
            "buy_in": 3000,
            "max_players": 50,
            "duration": 1200,  # 20 минут
            "prize_distribution": [0.50, 0.30, 0.20],
        },
    }
    
    @staticmethod
    def create_tournament(tournament_type: str) -> Dict:
        """Создание турнира"""
        import uuid
        
        if tournament_type not in TournamentSystem.TOURNAMENT_TYPES:
            return None
        
        config = TournamentSystem.TOURNAMENT_TYPES[tournament_type]
        tournament_id = str(uuid.uuid4())[:8]
        
        tournament = {
            'id': tournament_id,
            'type': tournament_type,
            'config': config,
            'players': [],
            'prize_pool': 0,
            'start_time': datetime.now() + timedelta(minutes=5),
            'end_time': None,
            'status': 'registration',  # registration, active, completed
            'results': {},
        }
        
        TournamentSystem.ACTIVE_TOURNAMENTS[tournament_id] = tournament
        return tournament
    
    @staticmethod
    def join_tournament(tournament_id: str, user_id: int, username: str) -> Tuple[bool, str]:
        """Присоединиться к турниру"""
        if tournament_id not in TournamentSystem.ACTIVE_TOURNAMENTS:
            return False, "Турнир не найден"
        
        tournament = TournamentSystem.ACTIVE_TOURNAMENTS[tournament_id]
        
        if tournament['status'] != 'registration':
            return False, "Регистрация закрыта"
        
        if len(tournament['players']) >= tournament['config']['max_players']:
            return False, "Турнир заполнен"
        
        if user_id in [p['user_id'] for p in tournament['players']]:
            return False, "Вы уже в турнире"
        
        tournament['players'].append({
            'user_id': user_id,
            'username': username,
            'score': 0,
            'rank': 0,
        })
        
        tournament['prize_pool'] += tournament['config']['buy_in']
        
        return True, f"✅ Вы зарегистрированы! Игроков: {len(tournament['players'])}/{tournament['config']['max_players']}"
    
    @staticmethod
    def tournament_status_visual(tournament_id: str) -> str:
        """Визуализация статуса турнира"""
        if tournament_id not in TournamentSystem.ACTIVE_TOURNAMENTS:
            return "Турнир не найден"
        
        t = TournamentSystem.ACTIVE_TOURNAMENTS[tournament_id]
        config = t['config']
        
        status_emoji = {
            'registration': '📝',
            'active': '🎮',
            'completed': '🏆',
        }
        
        players_list = "\n".join(
            f"{'🥇' if i == 0 else '🥈' if i == 1 else '🥉' if i == 2 else '  '} "
            f"{p['username']}: {p['score']} очков"
            for i, p in enumerate(sorted(t['players'], key=lambda x: x['score'], reverse=True)[:10])
        )
        
        return f"""
╔══════════════════════════════╗
║ {status_emoji[t['status']]} {config['name']} ║
╠══════════════════════════════╣
║ ID: {t['id']}              ║
║ Статус: {t['status']}       ║
║ Игроков: {len(t['players'])}/{config['max_players']} ║
║ Призовой фонд: {t['prize_pool']:,.0f} 🪙 ║
╠══════════════════════════════╣
║ ТОП-10 ИГРОКОВ:            ║
{players_list}
╚══════════════════════════════╝
"""

# ============================================================
# ПРОГРЕСС-БАРЫ И АНИМАЦИИ
# ============================================================

class ProgressBars:
    """Коллекция прогресс-баров"""
    
    @staticmethod
    def standard(current: float, maximum: float, length: int = 20, 
                 filled_char: str = '█', empty_char: str = '░') -> str:
        """Стандартный прогресс-бар"""
        percent = min(current / maximum, 1.0) if maximum > 0 else 0
        filled = int(percent * length)
        bar = filled_char * filled + empty_char * (length - filled)
        return f"[{bar}] {percent*100:.1f}%"
    
    @staticmethod
    def rainbow(current: float, maximum: float, length: int = 20) -> str:
        """Радужный прогресс-бар"""
        percent = min(current / maximum, 1.0) if maximum > 0 else 0
        filled = int(percent * length)
        
        colors = ['🟥', '🟧', '🟨', '🟩', '🟦', '🟪']
        bar = ''
        for i in range(filled):
            bar += colors[i % len(colors)]
        bar += '⬛' * (length - filled)
        
        return f"[{bar}] {percent*100:.1f}%"
    
    @staticmethod
    def animated_loading(text: str = "Загрузка", duration: float = 2.0) -> List[str]:
        """Анимированный индикатор загрузки"""
        frames = []
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        steps = 20
        
        for i in range(steps):
            progress = int((i / steps) * 20)
            bar = '█' * progress + '░' * (20 - progress)
            frame = f"{chars[i % len(chars)]} {text} {bar} {int((i/steps)*100)}%"
            frames.append(frame)
        
        return frames
    
    @staticmethod
    def pulse(text: str, cycles: int = 3) -> str:
        """Пульсирующий текст"""
        pulse_chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', '▂', '▁']
        result = ''
        for i in range(cycles * len(pulse_chars)):
            char = pulse_chars[i % len(pulse_chars)]
            result += f"\r{char} {text} {char}"
        return result

# ============================================================
# ФУНКЦИИ ДЛЯ МАЙНИНГА
# ============================================================

async def start_mining(user_id: int, currency: str) -> str:
    """Запуск майнинга"""
    if user_id not in mining_buffers:
        mining_buffers[user_id] = {
            'coins': 0, 'btc': 0, 'sol': 0, 'ton': 0, 'doge': 0, 'trx': 0,
            'start_time': datetime.now()
        }
    
    miners = await get_miners(user_id)
    if not miners:
        return "❌ У вас нет майнеров! Купите их командой: купить майнер S9"
    
    total_hashrate = 0
    for miner in miners:
        miner_config = config.MINERS.get(miner.model)
        if miner_config:
            total_hashrate += miner_config['coins'] * miner.quantity
    
    mining_buffers[user_id]['start_time'] = datetime.now()
    
    # Визуализация
    miner_list = "\n".join(
        f"  ⛏ {miner.model} x{miner.quantity}"
        for miner in miners
    )
    
    return f"""
⛏ МАЙНИНГ ЗАПУЩЕН!

Ваши майнеры:
{miner_list}

⚡ Общий хешрейт: {total_hashrate} монет/час
💎 Доступная валюта: {currency.upper()}

⏳ Добыча началась! Заберите через час командой "забрать"
"""

async def collect_mining(user_id: int) -> str:
    """Забрать добычу из майнинг-буфера"""
    if user_id not in mining_buffers:
        return "❌ У вас нет активной добычи. Напишите: майнить монеты"
    
    buffer = mining_buffers[user_id]
    start_time = buffer.get('start_time')
    
    if not start_time:
        return "❌ Ошибка времени майнинга"
    
    elapsed = (datetime.now() - start_time).total_seconds() / 3600  # Часы
    
    if elapsed < 1:
        remaining = int((1 - elapsed) * 60)
        return f"⏳ Добыча ещё не завершена! Осталось ~{remaining} минут"
    
    # Рассчитываем добычу
    miners = await get_miners(user_id)
    total_rewards = {'coins': 0, 'btc': 0, 'sol': 0, 'ton': 0, 'doge': 0, 'trx': 0}
    
    for miner in miners:
        miner_config = config.MINERS.get(miner.model)
        if miner_config:
            for currency in total_rewards:
                total_rewards[currency] += miner_config[currency] * miner.quantity * elapsed
    
    # Начисляем
    user = await get_user(user_id)
    user.balance += total_rewards['coins']
    await update_balance(user_id, total_rewards['coins'])
    
    for currency in ['btc', 'sol', 'ton', 'doge', 'trx']:
        if total_rewards[currency] > 0:
            await update_crypto(user_id, currency, total_rewards[currency])
    
    # Визуализация
    rewards_text = "\n".join(
        f"  {currency.upper()}: +{amount:.4f}"
        for currency, amount in total_rewards.items()
        if amount > 0
    )
    
    # Очищаем буфер
    del mining_buffers[user_id]
    
    return f"""
⛏ ДОБЫЧА СОБРАНА!

Время майнинга: {elapsed:.1f} часов

Найдено:
{rewards_text}

💰 Баланс обновлён!
"""

# ============================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ
# ============================================================

async def do_work(user_id: int) -> str:
    """Выполнение работы"""
    if user_id in work_cooldowns:
        last_work = work_cooldowns[user_id]
        if (datetime.now() - last_work).total_seconds() < 3600:
            remaining = 3600 - (datetime.now() - last_work).total_seconds()
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            return f"⏳ Вы уже работали! Отдыхайте {minutes}м {seconds}с"
    
    user = await get_user(user_id)
    profession = user.profession
    salary = config.SALARIES.get(profession, 125)
    
    # Бонус от транспорта
    vehicles = await get_user_vehicles(user_id)
    if vehicles:
        active_vehicle = next((v for v in vehicles if v.is_active), None)
        if active_vehicle:
            vehicle_config = config.VEHICLES.get(active_vehicle.vehicle_type)
            if vehicle_config:
                salary *= (1 + vehicle_config['speed_bonus'])
    
    # Бонус от премиума
    if user.is_premium:
        salary *= 1.10
    
    # Начисляем
    await update_balance(user_id, salary)
    work_cooldowns[user_id] = datetime.now()
    
    # Визуализация
    profession_icons = {
        "Грузчик": "📦", "Курьер": "🛵", "Таксист": "🚕",
        "Продавец": "🛍️", "Водитель фуры": "🚛",
        "Владелец киоска": "🏪", "Владелец кафе": "☕",
        "Владелец магазина": "🏬", "Владелец ресторана": "🍽️",
        "Владелец сети": "🏢"
    }
    
    icon = profession_icons.get(profession, '💼')
    
    return f"""
{icon} РАБОТА ВЫПОЛНЕНА!

Профессия: {profession}
Зарплата: {salary:,.0f} монет
💰 Баланс: {user.balance:,.0f} монет

⏳ Следующая работа через 1 час
"""

# ============================================================
# ФУНКЦИИ ДЛЯ ОГРАБЛЕНИЙ
# ============================================================

async def attempt_robbery(robber_id: int, victim_id: int, bot: Bot) -> str:
    """Попытка ограбления"""
    # Проверка кулдауна
    if robber_id in robbery_cooldowns:
        last_rob = robbery_cooldowns[robber_id]
        if (datetime.now() - last_rob).total_seconds() < 14400:  # 4 часа
            remaining = 14400 - (datetime.now() - last_rob).total_seconds()
            hours = int(remaining // 3600)
            return f"⏳ Кулдаун! Следующее ограбление через {hours} ч."
    
    robber = await get_user(robber_id)
    victim = await get_user(victim_id)
    
    if not victim:
        return "❌ Игрок не найден"
    
    if victim.balance < 1000:
        return "💰 У жертвы меньше 1000 монет"
    
    # Расчёт шанса
    base_chance = 0.40
    robber_vehicles = await get_user_vehicles(robber_id)
    victim_vehicles = await get_user_vehicles(victim_id)
    
    if robber_vehicles:
        active_v = next((v for v in robber_vehicles if v.is_active), None)
        if active_v:
            vehicle_bonuses = {"bmw": 0.05, "tesla": 0.10, "lamborghini": 0.15, "bugatti": 0.20}
            base_chance += vehicle_bonuses.get(active_v.vehicle_type, 0)
    
    if victim_vehicles:
        active_v = next((v for v in victim_vehicles if v.is_active), None)
        if active_v:
            defense = {"tesla": 0.15, "lamborghini": 0.10, "вертолёт": 0.25}
            base_chance -= defense.get(active_v.vehicle_type, 0)
    
    success = random.random() < base_chance
    
    if success:
        stolen_percent = random.uniform(0.05, 0.15)
        stolen_amount = victim.balance * stolen_percent
        
        await update_balance(victim_id, stolen_amount, 'subtract')
        await update_balance(robber_id, stolen_amount, 'add')
        
        robbery_cooldowns[robber_id] = datetime.now()
        
        # Логируем
        from config import add_transaction
        await add_transaction(robber_id, 'income', stolen_amount, 'robbery', f'Ограбление @{victim.username}')
        await add_transaction(victim_id, 'expense', stolen_amount, 'robbery', f'Ограблен @{robber.username}')
        
        # Визуализация
        return f"""
🔫 ОГРАБЛЕНИЕ УДАЛОСЬ!

Жертва: @{victim.username}
Украдено: {stolen_amount:,.0f} монет ({stolen_percent*100:.0f}%)
Шанс успеха: {base_chance*100:.0f}%

💰 Ваш баланс: {robber.balance:,.0f} монет
"""
    else:
        # Штраф за провал
        fine = robber.balance * 0.10
        await update_balance(robber_id, fine, 'subtract')
        await update_balance(victim_id, fine * 0.5, 'add')  # 50% штрафа жертве
        
        robbery_cooldowns[robber_id] = datetime.now()
        
        return f"""
🚔 ОГРАБЛЕНИЕ ПРОВАЛЕНО!

Шанс успеха: {base_chance*100:.0f}%
Штраф: {fine:,.0f} монет (10% баланса)

💸 Потеряно: {fine:,.0f} монет
"""

print("🎮 game_mechanics.py загружен")
print(f"   Игр казино: рулетка, кубы, слоты, краш, блэкджек, сапёр, красно-чёрный")
print(f"   Кейсов: {len(CaseSystem.CASES)}")
print(f"   Турниров: {len(TournamentSystem.TOURNAMENT_TYPES)}")
print(f"   Систем: майнинг, работа, ограбления, прогресс-бары")
# ============================================================
# handlers.py - ОБРАБОТЧИКИ КОМАНД, КЛАВИАТУРЫ, МЕНЮ
# ============================================================

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from aiogram import types, Bot, F
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, 
                           ReplyKeyboardMarkup, KeyboardButton, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters import Command
import asyncio

from config import *
from game_mechanics import *

# ============================================================
# ГЛАВНОЕ МЕНЮ (Reply Keyboard)
# ============================================================

def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню с кнопками"""
    builder = ReplyKeyboardBuilder()
    
    # Ряд 1
    builder.row(
        KeyboardButton(text="💼 РАБОТА"),
        KeyboardButton(text="⛏ МАЙНИНГ"),
        width=2
    )
    
    # Ряд 2
    builder.row(
        KeyboardButton(text="🏪 БИЗНЕС"),
        KeyboardButton(text="🏦 БАНК"),
        KeyboardButton(text="📈 КРИПТА"),
        width=3
    )
    
    # Ряд 3
    builder.row(
        KeyboardButton(text="🏛 КОРПОРАЦИЯ"),
        KeyboardButton(text="🔨 АУКЦИОН"),
        KeyboardButton(text="🏠 НЕДВИЖИМОСТЬ"),
        width=3
    )
    
    # Ряд 4
    builder.row(
        KeyboardButton(text="🚗 ТРАНСПОРТ"),
        KeyboardButton(text="🎰 КАЗИНО"),
        KeyboardButton(text="🔫 ОГРАБЛЕНИЕ"),
        width=3
    )
    
    # Ряд 5
    builder.row(
        KeyboardButton(text="👥 КЛАНЫ"),
        KeyboardButton(text="🏆 ДОСТИЖЕНИЯ"),
        KeyboardButton(text="📊 ТОП"),
        width=3
    )
    
    # Ряд 6
    builder.row(
        KeyboardButton(text="🎁 ПРОМОКОД"),
        KeyboardButton(text="📖 ПОМОЩЬ"),
        KeyboardButton(text="👤 ПРОФИЛЬ"),
        width=3
    )
    
    return builder.as_markup(resize_keyboard=True)

# ============================================================
# ИНЛАЙН-КЛАВИАТУРЫ ДЛЯ ПОДМЕНЮ
# ============================================================

def get_mining_menu() -> InlineKeyboardMarkup:
    """Меню майнинга"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="💰 Майнить монеты", callback_data="mine_coins"),
        InlineKeyboardButton(text="₿ Майнить BTC", callback_data="mine_btc"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="◎ Майнить SOL", callback_data="mine_sol"),
        InlineKeyboardButton(text="💎 Майнить TON", callback_data="mine_ton"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="🐕 Майнить DOGE", callback_data="mine_doge"),
        InlineKeyboardButton(text="▲ Майнить TRX", callback_data="mine_trx"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="🛒 Купить майнер", callback_data="buy_miner"),
        InlineKeyboardButton(text="📦 Забрать добычу", callback_data="collect_mining"),
        width=2
    )
    
    return builder.as_markup()

def get_casino_menu() -> InlineKeyboardMarkup:
    """Меню казино"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🎰 Рулетка", callback_data="casino_roulette"),
        InlineKeyboardButton(text="🎲 Кубы", callback_data="casino_dice"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="🎰 Слоты", callback_data="casino_slots"),
        InlineKeyboardButton(text="📈 Краш", callback_data="casino_crash"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="🃏 Блэкджек", callback_data="casino_blackjack"),
        InlineKeyboardButton(text="💣 Сапёр", callback_data="casino_mines"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="🔴 Красно-чёрный", callback_data="casino_redblack"),
        InlineKeyboardButton(text="🎁 Кейсы", callback_data="casino_cases"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Турниры", callback_data="casino_tournaments"),
        InlineKeyboardButton(text="🎟 Лотерея", callback_data="casino_lottery"),
        width=2
    )
    
    return builder.as_markup()

def get_bank_menu() -> InlineKeyboardMarkup:
    """Меню банка"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="💰 Открыть вклад", callback_data="bank_deposit"),
        InlineKeyboardButton(text="📥 Забрать вклад", callback_data="bank_withdraw"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="💳 Взять кредит", callback_data="bank_loan"),
        InlineKeyboardButton(text="✅ Погасить кредит", callback_data="bank_repay"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="📊 Мои вклады", callback_data="bank_my_deposits"),
        InlineKeyboardButton(text="📋 Мои кредиты", callback_data="bank_my_loans"),
        width=2
    )
    
    return builder.as_markup()

def get_business_menu() -> InlineKeyboardMarkup:
    """Меню бизнеса"""
    builder = InlineKeyboardBuilder()
    
    for biz_type, biz_data in config.BUSINESSES.items():
        builder.row(
            InlineKeyboardButton(
                text=f"{biz_data['icon']} {biz_type.title()} - {biz_data['price']:,} 🪙",
                callback_data=f"buy_business_{biz_type}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="📊 Мои бизнесы", callback_data="my_businesses"),
        InlineKeyboardButton(text="💰 Собрать доход", callback_data="collect_business"),
        width=2
    )
    
    return builder.as_markup()

def get_clan_menu() -> InlineKeyboardMarkup:
    """Меню кланов"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🏰 Создать клан", callback_data="clan_create"),
        InlineKeyboardButton(text="📋 Список кланов", callback_data="clan_list"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="👤 Мой клан", callback_data="clan_my"),
        InlineKeyboardButton(text="💰 Внести в казну", callback_data="clan_donate"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="📊 Рейтинг кланов", callback_data="clan_rating"),
        InlineKeyboardButton(text="❌ Покинуть клан", callback_data="clan_leave"),
        width=2
    )
    
    return builder.as_markup()

def get_profile_menu() -> InlineKeyboardMarkup:
    """Меню профиля"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🎨 Сменить скин", callback_data="change_skin"),
        InlineKeyboardButton(text="🏅 Сменить титул", callback_data="change_title"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="💎 Премиум", callback_data="buy_premium"),
        InlineKeyboardButton(text="🔄 Престиж", callback_data="prestige"),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="profile_stats"),
        InlineKeyboardButton(text="🔗 Реферальный код", callback_data="referral_code"),
        width=2
    )
    
    return builder.as_markup()

# ============================================================
# ОБРАБОТЧИКИ КОМАНД
# ============================================================

async def cmd_start(message: types.Message, bot: Bot):
    """Обработчик команды /start и кнопки Старт"""
    user_id = message.from_user.id
    user = await get_user(user_id)
    
    if not user:
        # Регистрация нового пользователя
        user = await register_user(
            user_id=user_id,
            username=message.from_user.username or "Unknown",
            first_name=message.from_user.first_name or "Игрок"
        )
        
        # Проверяем реферальный код если есть
        if message.text and len(message.text.split()) > 1:
            ref_code = message.text.split()[1]
            # Логика реферала
        
        welcome_text = f"""
🎉 ДОБРО ПОЖАЛОВАТЬ В ECONOMY BOT!

👤 Игрок: {user.first_name}
💰 Стартовый баланс: {config.START_BALANCE:,} монет
💼 Профессия: Безработный

📖 Напишите "помощь" для списка команд
💡 Начните с команды "работа"

Удачи в построении империи! 🏰
"""
        await message.answer(welcome_text, reply_markup=get_main_menu())
        
        # Логируем
        await log_action(bot, config.ADMIN_ID, 
                        f"🆕 Новый игрок: @{user.username} (ID: {user_id})")
    else:
        await message.answer(
            f"👋 С возвращением, {user.first_name}!\n"
            f"💰 Баланс: {user.balance:,.0f} монет\n"
            f"💼 Профессия: {user.profession}\n"
            f"⭐ Уровень: {user.level}",
            reply_markup=get_main_menu()
        )

async def cmd_help(message: types.Message):
    """Помощь по командам"""
    help_text = """
📖 ПОМОЩЬ ПО КОМАНДАМ

💼 РАБОТА:
  работа — получить зарплату (раз в час)
  
⛏ МАЙНИНГ:
  майнить монеты — запустить майнинг
  майнить btc — майнить Bitcoin
  майнить sol — майнить Solana
  забрать — забрать добычу
  купить майнер [модель] — купить майнер

🏪 БИЗНЕС:
  купить киоск — купить бизнес
  купить кафе — купить бизнес
  купить магазин — купить бизнес
  купить ресторан — купить бизнес
  купить сеть — купить бизнес

🏦 БАНК:
  вклад [дни] [сумма] — открыть вклад
  забрать вклад — закрыть вклад
  кредит [сумма] — взять кредит
  погасить кредит — вернуть кредит

📈 КРИПТА:
  крипта — показать курсы
  купить btc [кол-во] — купить крипту
  продать btc [кол-во] — продать крипту

🎰 КАЗИНО:
  рулетка красный 500 — ставка на цвет
  рулетка 7 500 — ставка на число
  кубы 100 — бросить кубы
  кубы 4 100 — угадать число
  слоты 200 — играть в слоты
  кнб 50 — камень-ножницы-бумага
  краш 100 — игра Краш
  блэкджек 500 — 21 очко
  сапёр 5 1000 — игра Сапёр
  красно-чёрный 500 — угадать цвет

🏠 НЕДВИЖИМОСТЬ:
  купить студию — купить недвижимость
  моя недвижимость — список
  
🚗 ТРАНСПОРТ:
  купить bmw — купить транспорт
  мой транспорт — список

🔫 ОГРАБЛЕНИЯ:
  ограбить @username — попытка ограбления

👥 КЛАНЫ:
  создать клан [название] — создать клан
  вступить в клан [id] — вступить
  мой клан — информация

🏆 ДОСТИЖЕНИЯ:
  достижения — показать все
  задания — ежедневные задания

🔨 АУКЦИОН:
  выставить [лот] [цена] — создать лот
  аукцион — список лотов
  ставка [id] [сумма] — сделать ставку

📊 ТОП:
  топ — топ-10 по балансу
  топ майнеры — топ по майнерам
  топ бизнес — топ по бизнесам

🎁 ПРОМОКОД:
  промокод [код] — активировать код

👤 ПРОФИЛЬ:
  профиль — ваш профиль
  мой код — реферальный код
"""
    await message.answer(help_text)

# ============================================================
# ОБРАБОТЧИКИ ТЕКСТОВЫХ КОМАНД
# ============================================================

async def handle_text_commands(message: types.Message, bot: Bot):
    """Обработка текстовых команд"""
    text = message.text.lower().strip()
    user_id = message.from_user.id
    user = await get_user(user_id)
    
    if not user:
        await message.answer("❌ Сначала зарегистрируйтесь: /start")
        return
    
    # ========== РАБОТА ==========
    if text == "работа":
        result = await do_work(user_id)
        await message.answer(result)
        await log_action(bot, config.ADMIN_ID, f"💼 @{user.username}: работа (+{config.SALARIES.get(user.profession, 125)})")
    
    # ========== МАЙНИНГ ==========
    elif text.startswith("майнить"):
        parts = text.split()
        currency = parts[1] if len(parts) > 1 else 'монеты'
        result = await start_mining(user_id, currency)
        await message.answer(result, reply_markup=get_mining_menu())
        await log_action(bot, config.ADMIN_ID, f"⛏ @{user.username}: майнинг {currency}")
    
    elif text == "забрать":
        result = await collect_mining(user_id)
        await message.answer(result)
        await log_action(bot, config.ADMIN_ID, f"📦 @{user.username}: собрал добычу")
    
    elif text.startswith("купить майнер"):
        model = text.replace("купить майнер ", "").strip().upper()
        if model in config.MINERS:
            miner_config = config.MINERS[model]
            if user.balance >= miner_config['price']:
                await update_balance(user_id, miner_config['price'], 'subtract')
                await add_miner(user_id, model)
                
                miner_visual = f"""
✅ МАЙНЕР КУПЛЕН!

⛏ Модель: {model}
⚡ Хешрейт: {miner_config['hashrate']}
🔌 Потребление: {miner_config['power']}
💰 Цена: {miner_config['price']:,} монет

📊 Доход в час:
  Монеты: {miner_config['coins']}
  BTC: {miner_config['btc']}
  SOL: {miner_config['sol']}
  TON: {miner_config['ton']}
  DOGE: {miner_config['doge']}
  TRX: {miner_config['trx']}

💵 Остаток на балансе: {user.balance:,.0f} монет
"""
                await message.answer(miner_visual)
                await log_action(bot, config.ADMIN_ID, f"⛏ @{user.username}: купил {model}")
            else:
                await message.answer(f"❌ Недостаточно средств! Нужно {miner_config['price']:,}, у вас {user.balance:,.0f}")
        else:
            miners_list = "\n".join(f"  {m} — {d['price']:,} монет" for m, d in config.MINERS.items())
            await message.answer(f"❌ Майнер не найден!\n\nДоступные:\n{miners_list}")
    
    # ========== БИЗНЕС ==========
    elif text.startswith("купить ") and text.replace("купить ", "") in config.BUSINESSES:
        biz_type = text.replace("купить ", "")
        biz_config = config.BUSINESSES[biz_type]
        
        if user.balance >= biz_config['price']:
            await update_balance(user_id, biz_config['price'], 'subtract')
            await add_business(user_id, biz_type)
            
            # Меняем профессию
            async with get_session() as session:
                usr = await session.query(User).filter(User.user_id == user_id).first()
                usr.profession = biz_config['profession']
                await session.commit()
            
            biz_visual = f"""
{biz_config['icon']} БИЗНЕС КУПЛЕН!

Тип: {biz_type.title()}
Цена: {biz_config['price']:,} монет
Доход: {biz_config['income']:,} монет/день
Новая профессия: {biz_config['profession']}

💰 Баланс: {user.balance:,.0f} монет
"""
            await message.answer(biz_visual)
            await log_action(bot, config.ADMIN_ID, f"🏪 @{user.username}: купил {biz_type}")
        else:
            await message.answer(f"❌ Недостаточно средств! Нужно {biz_config['price']:,}")
    
    # ========== БАНК ==========
    elif text.startswith("вклад"):
        parts = text.split()
        if len(parts) >= 3:
            days = int(parts[1])
            amount = float(parts[2])
            
            if days in config.DEPOSIT_RATES:
                if user.balance >= amount:
                    rate = config.DEPOSIT_RATES[days]
                    await update_balance(user_id, amount, 'subtract')
                    
                    # Создаём вклад
                    async with get_session() as session:
                        deposit = Deposit(
                            user_id=user_id,
                            amount=amount,
                            rate=rate,
                            days=days,
                            start_date=datetime.now(),
                            end_date=datetime.now() + timedelta(days=days)
                        )
                        session.add(deposit)
                        await session.commit()
                    
                    profit = amount * rate
                    
                    deposit_visual = f"""
🏦 ВКЛАД ОТКРЫТ!

💰 Сумма: {amount:,.0f} монет
📅 Срок: {days} дней
📈 Ставка: {rate*100:.1f}%
💵 Ожидаемый доход: {profit:,.0f} монет
🏁 Дата окончания: {(datetime.now() + timedelta(days=days)).strftime('%d.%m.%Y')}

⚠️ Досрочное снятие — с штрафом!
"""
                    await message.answer(deposit_visual)
                    await log_action(bot, config.ADMIN_ID, f"🏦 @{user.username}: вклад {amount} на {days} дн.")
                else:
                    await message.answer("❌ Недостаточно средств!")
            else:
                rates_text = "\n".join(f"  {d} дн. — {r*100:.1f}%" for d, r in config.DEPOSIT_RATES.items())
                await message.answer(f"❌ Неверный срок!\n\nДоступные:\n{rates_text}")
        else:
            await message.answer("❌ Формат: вклад [дни] [сумма]\nПример: вклад 30 10000")
    
    elif text == "забрать вклад":
        # Получаем активный вклад
        async with get_session() as session:
            deposit = await session.query(Deposit).filter(
                Deposit.user_id == user_id,
                Deposit.active == True
            ).first()
            
            if deposit:
                now = datetime.now()
                elapsed = (now - deposit.start_date).total_seconds()
                total_duration = deposit.days * 86400
                progress = elapsed / total_duration
                
                if now >= deposit.end_date:
                    # Полный срок — полная выплата
                    payout = deposit.amount * (1 + deposit.rate)
                    await update_balance(user_id, payout)
                    deposit.active = False
                    
                    await message.answer(
                        f"✅ ВКЛАД ЗАКРЫТ!\n"
                        f"Сумма: {deposit.amount:,.0f}\n"
                        f"Проценты: {deposit.amount * deposit.rate:,.0f}\n"
                        f"💵 Итого: {payout:,.0f} монет"
                    )
                else:
                    # Досрочное закрытие — штраф
                    if progress < 0.25:
                        refund = 0
                    elif progress < 0.50:
                        refund = deposit.amount * 0.20
                    elif progress < 0.75:
                        refund = deposit.amount * 0.50
                    else:
                        refund = deposit.amount * 0.80
                    
                    await update_balance(user_id, refund)
                    deposit.active = False
                    penalty = deposit.amount - refund
                    
                    await message.answer(
                        f"⚠️ ДОСРОЧНОЕ ЗАКРЫТИЕ!\n"
                        f"Возврат: {refund:,.0f} монет ({progress*100:.0f}% срока)\n"
                        f"Штраф: {penalty:,.0f} монет"
                    )
                
                await log_action(bot, config.ADMIN_ID, f"🏦 @{user.username}: закрыл вклад")
            else:
                await message.answer("❌ У вас нет активных вкладов!")
    
    elif text.startswith("кредит"):
        parts = text.split()
        if len(parts) >= 2:
            amount = float(parts[1])
            
            # Проверка существующих кредитов
            async with get_session() as session:
                active_loan = await session.query(Loan).filter(
                    Loan.user_id == user_id,
                    Loan.active == True
                ).first()
                
                if active_loan:
                    await message.answer("❌ Сначала погасите текущий кредит!")
                    return
            
            max_loan = user.total_earned * 0.5  # Максимум 50% от общего заработка
            if amount > max_loan:
                await message.answer(f"❌ Максимальный кредит: {max_loan:,.0f} монет")
                return
            
            debt = amount * (1 + config.CREDIT_RATE)
            
            async with get_session() as session:
                loan = Loan(
                    user_id=user_id,
                    amount=amount,
                    debt=debt,
                    end_date=datetime.now() + timedelta(days=config.CREDIT_DAYS)
                )
                session.add(loan)
                await session.commit()
            
            await update_balance(user_id, amount)
            
            await message.answer(
                f"💳 КРЕДИТ ВЫДАН!\n"
                f"Сумма: {amount:,.0f} монет\n"
                f"К возврату: {debt:,.0f} монет ({config.CREDIT_RATE*100:.0f}%)\n"
                f"Дата погашения: {(datetime.now() + timedelta(days=config.CREDIT_DAYS)).strftime('%d.%m.%Y')}"
            )
            await log_action(bot, config.ADMIN_ID, f"💳 @{user.username}: кредит {amount}")
    
    elif text == "погасить кредит":
        async with get_session() as session:
            loan = await session.query(Loan).filter(
                Loan.user_id == user_id,
                Loan.active == True
            ).first()
            
            if loan:
                if user.balance >= loan.debt:
                    await update_balance(user_id, loan.debt, 'subtract')
                    loan.active = False
                    
                    await message.answer(
                        f"✅ КРЕДИТ ПОГАШЕН!\n"
                        f"Выплачено: {loan.debt:,.0f} монет\n"
                        f"💰 Остаток: {user.balance:,.0f} монет"
                    )
                else:
                    await message.answer(
                        f"❌ Недостаточно средств!\n"
                        f"Долг: {loan.debt:,.0f}\n"
                        f"Баланс: {user.balance:,.0f}"
                    )
            else:
                await message.answer("❌ У вас нет активных кредитов!")
    
    # ========== КРИПТОВАЛЮТА ==========
    elif text == "крипта":
        crypto_text = "📈 КУРСЫ КРИПТОВАЛЮТ\n\n"
        for symbol, data in config.CRYPTO.items():
            crypto_text += f"{data['icon']} {data['name']} ({symbol.upper()}): {data['price']:,.2f} монет\n"
        
        await message.answer(crypto_text)
    
    elif text.startswith("купить ") and text.split()[1] in config.CRYPTO:
        parts = text.split()
        symbol = parts[1].lower()
        amount = float(parts[2]) if len(parts) > 2 else 0
        
        if amount > 0:
            crypto_data = config.CRYPTO[symbol]
            total_cost = crypto_data['price'] * amount
            
            if user.balance >= total_cost:
                await update_balance(user_id, total_cost, 'subtract')
                await update_crypto(user_id, symbol, amount)
                
                await message.answer(
                    f"✅ КУПЛЕНО!\n"
                    f"{crypto_data['icon']} {amount} {symbol.upper()}\n"
                    f"💵 Потрачено: {total_cost:,.2f} монет"
                )
            else:
                await message.answer("❌ Недостаточно средств!")
    
    elif text.startswith("продать "):
        parts = text.split()
        symbol = parts[1].lower()
        amount = float(parts[2]) if len(parts) > 2 else 0
        
        if amount > 0:
            holdings = await get_user_crypto(user_id)
            holding = next((h for h in holdings if h.symbol == symbol), None)
            
            if holding and holding.amount >= amount:
                crypto_data = config.CRYPTO[symbol]
                total_revenue = crypto_data['price'] * amount
                
                await update_crypto(user_id, symbol, amount, 'subtract')
                await update_balance(user_id, total_revenue)
                
                await message.answer(
                    f"✅ ПРОДАНО!\n"
                    f"{crypto_data['icon']} {amount} {symbol.upper()}\n"
                    f"💵 Получено: {total_revenue:,.2f} монет"
                )
            else:
                await message.answer("❌ Недостаточно криптовалюты!")
    
    # ========== КАЗИНО ==========
    elif text == "казино" or text == "🎰 казино":
        await message.answer(
            "🎰 КАЗИНО\n\nВыберите игру:",
            reply_markup=get_casino_menu()
        )
    
    elif text.startswith("рулетка"):
        parts = text.split()
        if len(parts) >= 3:
            bet_type = parts[1]
            bet_amount = float(parts[2])
            
            if bet_amount > user.balance:
                await message.answer("❌ Недостаточно средств!")
                return
            
            await update_balance(user_id, bet_amount, 'subtract')
            
            number = CasinoGames.spin_roulette()
            color = CasinoGames.get_color(number)
            
            # Определяем тип ставки
            if bet_type.isdigit():
                payout = CasinoGames.calculate_roulette_payout('число', bet_amount, number, bet_type)
            elif bet_type in ['красный', 'красное', 'red']:
                payout = CasinoGames.calculate_roulette_payout('цвет', bet_amount, number, 'red')
            elif bet_type in ['чёрный', 'черное', 'black']:
                payout = CasinoGames.calculate_roulette_payout('цвет', bet_amount, number, 'black')
            else:
                payout = 0
            
            await update_balance(user_id, payout)
            
            board = CasinoGames.roulette_board_visual(number)
            result_text = "🎉 ВЫИГРЫШ!" if payout > 0 else "😢 ПРОИГРЫШ"
            
            await message.answer(
                f"{board}\n\n"
                f"{result_text}\n"
                f"Ставка: {bet_amount:,.0f}\n"
                f"Выпало: {number} {color}\n"
                f"Выплата: {payout:,.0f} монет"
            )
    
    elif text.startswith("слоты"):
        parts = text.split()
        bet = float(parts[1]) if len(parts) > 1 else 100
        
        if bet > user.balance:
            await message.answer("❌ Недостаточно средств!")
            return
        
        await update_balance(user_id, bet, 'subtract')
        
        # Отправляем "крутящиеся" слоты
        spinning_msg = await message.answer(
            "🎰 Крутим барабаны...\n" + CasinoGames.slots_visual([], True)
        )
        
        # Пауза для эффекта
        await asyncio.sleep(1.5)
        
        # Финальный результат
        grid = CasinoGames.spin_slots()
        payout, win_info = CasinoGames.calculate_slot_payout(grid, bet)
        
        await update_balance(user_id, payout)
        
        # Обновляем сообщение
        await spinning_msg.edit_text(
            f"🎰 СЛОТЫ\n\n"
            f"{CasinoGames.slots_visual(grid)}\n\n"
            f"Ставка: {bet:,.0f}\n"
            f"Выплата: {payout:,.0f}\n"
            f"{win_info}"
        )
    
    elif text.startswith("краш"):
        parts = text.split()
        bet = float(parts[1]) if len(parts) > 1 else 100
        
        if bet > user.balance:
            await message.answer("❌ Недостаточно средств!")
            return
        
        await update_balance(user_id, bet, 'subtract')
        
        winnings = await CasinoGames.crash_animation(message, bet, bot)
        
        if winnings > 0:
            await update_balance(user_id, winnings)
    
    elif text.startswith("блэкджек"):
        parts = text.split()
        bet = float(parts[1]) if len(parts) > 1 else 500
        
        if bet > user.balance:
            await message.answer("❌ Недостаточно средств!")
            return
        
        await update_balance(user_id, bet, 'subtract')
        
        # Создаём игру
        deck = CasinoGames.create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        
        active_blackjack[user_id] = {
            'bet': bet,
            'deck': deck,
            'player_hand': player_hand,
            'dealer_hand': dealer_hand,
            'game_over': False
        }
        
        player_value = CasinoGames.hand_value(player_hand)
        
        # Проверка на блэкджек
        if player_value == 21:
            payout = bet * 2.5
            await update_balance(user_id, payout)
            active_blackjack[user_id]['game_over'] = True
            
            await message.answer(
                f"🃏 БЛЭКДЖЕК!\n\n"
                f"Ваша рука: {CasinoGames.hand_visual(player_hand)} ({player_value})\n"
                f"Дилер: {CasinoGames.hand_visual(dealer_hand)} ({CasinoGames.hand_value(dealer_hand)})\n\n"
                f"🎉 ВЫИГРЫШ! +{payout:,.0f} монет",
                reply_markup=CasinoGames.blackjack_keyboard(True)
            )
        else:
            await message.answer(
                f"🃏 БЛЭКДЖЕК\n\n"
                f"Ваша рука: {CasinoGames.hand_visual(player_hand)} ({player_value})\n"
                f"Дилер: {CasinoGames.hand_visual(dealer_hand, hidden=True)}\n\n"
                f"Ставка: {bet:,.0f} монет",
                reply_markup=CasinoGames.blackjack_keyboard(False)
            )
    
    elif text.startswith("сапёр"):
        parts = text.split()
        mines = int(parts[1]) if len(parts) > 1 else 5
        bet = float(parts[2]) if len(parts) > 2 else 1000
        
        if mines < 1 or mines > 24:
            await message.answer("❌ Количество мин: 1-24")
            return
        
        if bet > user.balance:
            await message.answer("❌ Недостаточно средств!")
            return
        
        await update_balance(user_id, bet, 'subtract')
        
        grid = CasinoGames.generate_mines_grid(mines)
        revealed = set()
        
        active_mines_games[user_id] = {
            'bet': bet,
            'grid': grid,
            'mines_count': mines,
            'revealed': revealed,
            'multiplier': 1.0,
            'game_over': False
        }
        
        await message.answer(
            f"💣 САПЁР\n"
            f"Мины: {mines}/25\n"
            f"Ставка: {bet:,.0f}\n"
            f"Множитель: x1.00\n\n"
            f"Открывай клетки!",
            reply_markup=CasinoGames.mines_keyboard(grid, revealed)
        )
    
    # ========== ОГРАБЛЕНИЯ ==========
    elif text.startswith("ограбить"):
        parts = text.split()
        if len(parts) >= 2:
            target = parts[1]
            
            # Извлекаем username или ID
            if target.startswith("@"):
                async with get_session() as session:
                    victim = await session.query(User).filter(User.username == target[1:]).first()
                    if victim:
                        result = await attempt_robbery(user_id, victim.user_id, bot)
                        await message.answer(result)
                    else:
                        await message.answer("❌ Игрок не найден!")
    
    # ========== ТОП ==========
    elif text == "топ":
        async with get_session() as session:
            top_users = await session.query(User).order_by(User.balance.desc()).limit(10).all()
            
            top_text = "📊 ТОП-10 ПО БАЛАНСУ\n\n"
            medals = ["🥇", "🥈", "🥉"] + ["  "] * 7
            
            for i, u in enumerate(top_users):
                top_text += f"{medals[i]}{i+1}. {u.first_name} — {u.balance:,.0f} 🪙\n"
            
            await message.answer(top_text)
    
    # ========== ПРОМОКОД ==========
    elif text.startswith("промокод"):
        parts = text.split()
        code = parts[1] if len(parts) > 1 else ""
        
        if code:
            async with get_session() as session:
                promo = await session.query(Promocode).filter(
                    Promocode.code == code,
                    Promocode.active == True
                ).first()
                
                if promo and promo.used < promo.max_uses:
                    used = await session.query(UsedPromocode).filter(
                        UsedPromocode.user_id == user_id,
                        UsedPromocode.code == code
                    ).first()
                    
                    if not used:
                        await update_balance(user_id, promo.reward)
                        promo.used += 1
                        
                        used_entry = UsedPromocode(user_id=user_id, code=code)
                        session.add(used_entry)
                        await session.commit()
                        
                        await message.answer(
                            f"🎁 ПРОМОКОД АКТИВИРОВАН!\n"
                            f"💰 Награда: {promo.reward:,.0f} монет\n"
                            f"📊 Осталось использований: {promo.max_uses - promo.used}"
                        )
                    else:
                        await message.answer("❌ Вы уже использовали этот код!")
                else:
                    await message.answer("❌ Промокод недействителен!")
    
    # ========== ПРОФИЛЬ ==========
    elif text == "профиль":
        profile_text = f"""
👤 ПРОФИЛЬ

Имя: {user.first_name}
@{user.username}
⭐ Уровень: {user.level}
💼 Профессия: {user.profession}
💰 Баланс: {user.balance:,.0f} монет

📊 Статистика:
  Заработано: {user.total_earned:,.0f}
  Потрачено: {user.total_spent:,.0f}

🏅 Престиж: {user.prestige}
💎 Премиум: {'Да' if user.is_premium else 'Нет'}
"""
        await message.answer(profile_text, reply_markup=get_profile_menu())

# ============================================================
# ОБРАБОТЧИКИ CALLBACK-ЗАПРОСОВ
# ============================================================

async def process_callback(callback: types.CallbackQuery, bot: Bot):
    """Обработка всех callback-запросов"""
    data = callback.data
    user_id = callback.from_user.id
    
    # ========== КАЗИНО МЕНЮ ==========
    if data == "casino_roulette":
        await callback.message.edit_text(
            "🎰 РУЛЕТКА\n\n"
            "Ставки:\n"
            "• рулетка красный 500\n"
            "• рулетка чёрный 500\n"
            "• рулетка 7 500 (на число)\n"
            "• рулетка чёт 500\n"
            "• рулетка дюжина1 500",
            reply_markup=get_casino_menu()
        )
    elif data == "casino_slots":
        await callback.message.edit_text(
            "🎰 СЛОТЫ\n\n"
            "Команда: слоты [ставка]\n"
            "Пример: слоты 200",
            reply_markup=get_casino_menu()
        )
    elif data == "casino_crash":
        await callback.message.edit_text(
            "📈 КРАШ\n\n"
            "Команда: краш [ставка]\n"
            "Пример: краш 100\n"
            "Нажмите ЗАБРАТЬ до краша!",
            reply_markup=get_casino_menu()
        )
    
    # ========== БЛЭКДЖЕК ==========
    elif data.startswith("bj_"):
        if user_id not in active_blackjack:
            await callback.answer("❌ Игра не найдена!")
            return
        
        game = active_blackjack[user_id]
        
        if data == "bj_hit":
            # Взять карту
            new_card = game['deck'].pop()
            game['player_hand'].append(new_card)
            player_value = CasinoGames.hand_value(game['player_hand'])
            
            if player_value > 21:
                # Перебор
                game['game_over'] = True
                await callback.message.edit_text(
                    f"💥 ПЕРЕБОР!\n\n"
                    f"Ваша рука: {CasinoGames.hand_visual(game['player_hand'])} ({player_value})\n"
                    f"Дилер: {CasinoGames.hand_visual(game['dealer_hand'])} ({CasinoGames.hand_value(game['dealer_hand'])})\n\n"
                    f"😢 Проигрыш! -{game['bet']:,.0f} монет",
                    reply_markup=CasinoGames.blackjack_keyboard(True)
                )
            else:
                await callback.message.edit_text(
                    f"🃏 БЛЭКДЖЕК\n\n"
                    f"Ваша рука: {CasinoGames.hand_visual(game['player_hand'])} ({player_value})\n"
                    f"Дилер: {CasinoGames.hand_visual(game['dealer_hand'], hidden=True)}\n\n"
                    f"Ставка: {game['bet']:,.0f}",
                    reply_markup=CasinoGames.blackjack_keyboard(False, len(game['player_hand']) == 2)
                )
        
        elif data == "bj_stand":
            # Дилер добирает
            game['game_over'] = True
            dealer_value = CasinoGames.hand_value(game['dealer_hand'])
            
            while dealer_value < 17:
                game['dealer_hand'].append(game['deck'].pop())
                dealer_value = CasinoGames.hand_value(game['dealer_hand'])
            
            player_value = CasinoGames.hand_value(game['player_hand'])
            
            if dealer_value > 21 or player_value > dealer_value:
                payout = game['bet'] * 2
                await update_balance(user_id, payout)
                result = f"🎉 ВЫИГРЫШ! +{payout:,.0f}"
            elif player_value == dealer_value:
                await update_balance(user_id, game['bet'])
                result = "🤝 НИЧЬЯ! Ставка возвращена"
            else:
                result = f"😢 ПРОИГРЫШ! -{game['bet']:,.0f}"
            
            await callback.message.edit_text(
                f"🃏 БЛЭКДЖЕК\n\n"
                f"Ваша рука: {CasinoGames.hand_visual(game['player_hand'])} ({player_value})\n"
                f"Дилер: {CasinoGames.hand_visual(game['dealer_hand'])} ({dealer_value})\n\n"
                f"{result}",
                reply_markup=CasinoGames.blackjack_keyboard(True)
            )
    
    # ========== САПЁР ==========
    elif data.startswith("mine_"):
        if user_id not in active_mines_games:
            await callback.answer("❌ Игра не найдена!")
            return
        
        game = active_mines_games[user_id]
        
        if data == "mine_cashout":
            # Забираем выигрыш
            winnings = game['bet'] * game['multiplier']
            await update_balance(user_id, winnings)
            game['game_over'] = True
            
            # Показываем все мины
            all_mines = set()
            for i in range(5):
                for j in range(5):
                    if game['grid'][i][j] == -1:
                        all_mines.add((i, j))
            
            await callback.message.edit_text(
                f"💰 ЗАБРАНО!\n"
                f"Множитель: x{game['multiplier']:.2f}\n"
                f"Выигрыш: {winnings:,.0f} монет\n\n"
                f"Расположение мин показано:",
                reply_markup=CasinoGames.mines_keyboard(game['grid'], game['revealed'] | all_mines, True)
            )
            del active_mines_games[user_id]
        
        elif data.startswith("mine_") and data != "mine_gameover" and data != "mine_revealed":
            _, i, j = data.split("_")
            i, j = int(i), int(j)
            pos = (i, j)
            
            if pos in game['revealed']:
                await callback.answer("Уже открыто!")
                return
            
            game['revealed'].add(pos)
            
            if game['grid'][i][j] == -1:
                # МИНА!
                game['game_over'] = True
                
                all_mines = set()
                for row in range(5):
                    for col in range(5):
                        if game['grid'][row][col] == -1:
                            all_mines.add((row, col))
                
                await callback.message.edit_text(
                    f"💥 МИНА!\n"
                    f"Потеряно: {game['bet']:,.0f} монет",
                    reply_markup=CasinoGames.mines_keyboard(game['grid'], game['revealed'] | all_mines, True)
                )
                del active_mines_games[user_id]
            else:
                # Безопасная клетка
                revealed_count = len(game['revealed'])
                # Логика множителя
                
                await callback.message.edit_text(
                    f"💎 БЕЗОПАСНО!\n"
                    f"Открыто: {revealed_count}/25\n"
                    f"Множитель: x{game['multiplier']:.2f}\n"
                    f"Потенциальный выигрыш: {game['bet'] * game['multiplier']:,.0f}",
                    reply_markup=CasinoGames.mines_keyboard(game['grid'], game['revealed'])
                )
    
    # ========== КРАШ ==========
    elif data == "crash_cashout":
        if user_id in active_crash_games:
            game = active_crash_games[user_id]
            if game['active'] and not game.get('cashed_out'):
                game['cashed_out'] = True
                winnings = game['bet'] * game['multiplier']
                await update_balance(user_id, winnings)
                
                await callback.message.edit_text(
                    f"💰 ЗАБРАНО!\n"
                    f"Множитель: x{game['multiplier']:.2f}\n"
                    f"Выигрыш: {winnings:,.0f} монет"
                )
    
    await callback.answer()

# ============================================================
# ФУНКЦИЯ ЛОГИРОВАНИЯ
# ============================================================

async def log_action(bot: Bot, admin_id: int, action: str):
    """Логирование действий в ЛС админа"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_message = f"[{timestamp}] {action}"
    
    try:
        await bot.send_message(admin_id, log_message)
    except Exception as e:
        print(f"Log error: {e}")

print("📱 handlers.py загружен")
print(f"   Меню: главное, майнинг, казино, банк, бизнес, кланы, профиль")
print(f"   Обработчики: текст, callback")
# ============================================================
# admin_panel.py - АДМИН-ПАНЕЛЬ, ЭКОНОМИКА, ФОНОВЫЕ ЗАДАЧИ
# ============================================================

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from aiogram import types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import *
from game_mechanics import CasinoGames, CaseSystem, TournamentSystem

# ============================================================
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ============================================================
inflation_multiplier = 1.0  # Мультипликатор цен
crisis_active = False        # Режим кризиса
boom_active = False          # Режим бума
crisis_end_time = None       # Время окончания кризиса
boom_end_time = None         # Время окончания бума
current_tax_rate = 0.05      # Текущий налог (5%)

# ============================================================
# АДМИН-КОМАНДЫ
# ============================================================

async def handle_admin_commands(message: types.Message, bot: Bot):
    """Обработка админ-команд (только в ЛС)"""
    if message.from_user.id != config.ADMIN_ID:
        return False  # Не админ
    
    if message.chat.type != 'private':
        await message.answer("❌ Админ-команды работают только в ЛС!")
        return True
    
    text = message.text.lower().strip()
    
    # ========== СТАТИСТИКА ==========
    if text == "админ статистика":
        await admin_statistics(message)
        return True
    
    # ========== ВЫДАТЬ МОНЕТЫ ==========
    elif text.startswith("админ выдать"):
        parts = text.split()
        if len(parts) >= 3:
            target = parts[2]  # @username или ID
            amount = float(parts[3]) if len(parts) > 3 else 0
            
            # Извлекаем username
            if target.startswith("@"):
                async with get_session() as session:
                    user = await session.query(User).filter(User.username == target[1:]).first()
                    if user:
                        await update_balance(user.user_id, amount)
                        await message.answer(f"✅ Выдано {amount:,.0f} монет игроку @{user.username}")
                        
                        try:
                            await bot.send_message(
                                user.user_id,
                                f"🎁 Администратор выдал вам {amount:,.0f} монет!"
                            )
                        except:
                            pass
                    else:
                        await message.answer("❌ Игрок не найден!")
        return True
    
    # ========== НАЛОГ ==========
    elif text.startswith("админ налог"):
        parts = text.split()
        if len(parts) >= 2:
            global current_tax_rate
            new_tax = float(parts[2]) / 100
            if 0 <= new_tax <= 0.50:
                current_tax_rate = new_tax
                await message.answer(f"✅ Налог установлен: {new_tax*100:.1f}%")
            else:
                await message.answer("❌ Налог должен быть от 0% до 50%")
        return True
    
    # ========== КРИЗИС ==========
    elif text == "админ кризис":
        global crisis_active, crisis_end_time
        crisis_active = True
        crisis_end_time = datetime.now() + timedelta(hours=24)
        
        await message.answer(
            "📉 КРИЗИС АКТИВИРОВАН!\n\n"
            "Эффекты на 24 часа:\n"
            "• Налоги +10%\n"
            "• Доходы -20%\n"
            "• Цены на крипту -15%\n"
            "• Шанс ограблений +10%"
        )
        
        # Уведомляем всех игроков
        await broadcast_message(bot, 
            "📉 ЭКОНОМИЧЕСКИЙ КРИЗИС!\n\n"
            "Срочные новости:\n"
            "• Налоги повышены на 10%\n"
            "• Доходы снижены на 20%\n"
            "• Криптовалюты падают\n"
            "• Участились ограбления!\n\n"
            "Длительность: 24 часа"
        )
        return True
    
    # ========== БУМ ==========
    elif text == "админ бум":
        global boom_active, boom_end_time
        boom_active = True
        boom_end_time = datetime.now() + timedelta(hours=24)
        
        await message.answer(
            "📈 ЭКОНОМИЧЕСКИЙ БУМ!\n\n"
            "Эффекты на 24 часа:\n"
            "• Доходы +50%\n"
            "• Цены крипты +25%\n"
            "• Майнинг ускорен\n"
            "• Бонусные монеты за работу"
        )
        
        await broadcast_message(bot,
            "📈 ЭКОНОМИЧЕСКИЙ БУМ!\n\n"
            "Отличные новости:\n"
            "• Все доходы +50%\n"
            "• Криптовалюты растут\n"
            "• Майнинг приносит больше\n"
            "• Зарплаты повышены!\n\n"
            "Длительность: 24 часа"
        )
        return True
    
    # ========== ПРОМОКОДЫ ==========
    elif text.startswith("админ создать код"):
        parts = text.split()
        if len(parts) >= 4:
            code_name = parts[3]
            reward = float(parts[4]) if len(parts) > 4 else 0
            max_uses = int(parts[5]) if len(parts) > 5 else 100
            
            async with get_session() as session:
                existing = await session.query(Promocode).filter(Promocode.code == code_name).first()
                if existing:
                    await message.answer("❌ Такой код уже существует!")
                    return True
                
                promo = Promocode(
                    code=code_name,
                    reward=reward,
                    max_uses=max_uses,
                    created_by=config.ADMIN_ID
                )
                session.add(promo)
                await session.commit()
                
                await message.answer(
                    f"✅ ПРОМОКОД СОЗДАН!\n\n"
                    f"Код: {code_name}\n"
                    f"Награда: {reward:,.0f} монет\n"
                    f"Лимит: {max_uses} использований"
                )
        return True
    
    elif text.startswith("админ удалить код"):
        parts = text.split()
        if len(parts) >= 4:
            code_name = parts[3]
            async with get_session() as session:
                promo = await session.query(Promocode).filter(Promocode.code == code_name).first()
                if promo:
                    promo.active = False
                    await session.commit()
                    await message.answer(f"✅ Промокод {code_name} деактивирован")
                else:
                    await message.answer("❌ Код не найден!")
        return True
    
    # ========== БРОADCAST ==========
    elif text.startswith("админ рассылка"):
        broadcast_text = text.replace("админ рассылка ", "")
        if broadcast_text:
            await broadcast_message(bot, broadcast_text)
            await message.answer(f"✅ Рассылка отправлена!")
        return True
    
    # ========== ИНФОРМАЦИЯ ОБ ИГРОКЕ ==========
    elif text.startswith("админ инфо"):
        parts = text.split()
        if len(parts) >= 3:
            target = parts[2]
            if target.startswith("@"):
                async with get_session() as session:
                    user = await session.query(User).filter(User.username == target[1:]).first()
                    if user:
                        miners = await get_miners(user.user_id)
                        businesses = await get_businesses(user.user_id)
                        crypto = await get_user_crypto(user.user_id)
                        
                        info_text = f"""
📊 ИНФОРМАЦИЯ ОБ ИГРОКЕ

👤 Имя: {user.first_name}
🆔 ID: {user.user_id}
💼 Профессия: {user.profession}
⭐ Уровень: {user.level}
💰 Баланс: {user.balance:,.0f}
💎 Премиум: {'Да' if user.is_premium else 'Нет'}

📊 Статистика:
  Заработано: {user.total_earned:,.0f}
  Потрачено: {user.total_spent:,.0f}

⛏ Майнеров: {len(miners)}
🏪 Бизнесов: {len(businesses)}
🪙 Криптовалют: {len(crypto)}

📅 Регистрация: {user.created_at.strftime('%d.%m.%Y')}
"""
                        await message.answer(info_text)
                    else:
                        await message.answer("❌ Игрок не найден!")
        return True
    
    # ========== СБРОС ИГРОКА ==========
    elif text.startswith("админ сброс"):
        parts = text.split()
        if len(parts) >= 3:
            target = parts[2]
            if target.startswith("@"):
                async with get_session() as session:
                    user = await session.query(User).filter(User.username == target[1:]).first()
                    if user:
                        user.balance = config.START_BALANCE
                        user.profession = "Безработный"
                        user.level = 1
                        user.experience = 0
                        
                        # Удаляем майнеры
                        await session.query(Miner).filter(Miner.user_id == user.user_id).delete()
                        # Удаляем бизнесы
                        await session.query(Business).filter(Business.user_id == user.user_id).delete()
                        # Удаляем крипту
                        await session.query(CryptoHolding).filter(CryptoHolding.user_id == user.user_id).delete()
                        
                        await session.commit()
                        await message.answer(f"✅ Игрок @{user.username} сброшен!")
                    else:
                        await message.answer("❌ Игрок не найден!")
        return True
    
    # ========== ПОМОЩЬ АДМИНА ==========
    elif text == "админ помощь" or text == "админ":
        admin_help = """
👑 АДМИН-КОМАНДЫ

📊 Статистика:
  админ статистика — общая статистика

💰 Управление монетами:
  админ выдать @user 10000
  админ сброс @user

📈 Экономика:
  админ налог 10 — установить налог 10%
  админ кризис — запустить кризис
  админ бум — запустить бум

🎁 Промокоды:
  админ создать код TEST 5000 100
  админ удалить код TEST

📢 Рассылка:
  админ рассылка [текст]

👤 Игроки:
  админ инфо @user
  админ сброс @user
"""
        await message.answer(admin_help)
        return True
    
    return False  # Не админ-команда


async def admin_statistics(message: types.Message):
    """Показать общую статистику бота"""
    async with get_session() as session:
        total_users = await session.query(func.count(User.id)).scalar()
        total_balance = await session.query(func.sum(User.balance)).scalar() or 0
        total_miners = await session.query(func.count(Miner.id)).scalar()
        total_businesses = await session.query(func.count(Business.id)).scalar()
        total_deposits = await session.query(func.sum(Deposit.amount)).filter(Deposit.active == True).scalar() or 0
        total_loans = await session.query(func.sum(Loan.debt)).filter(Loan.active == True).scalar() or 0
        
        # Топ-5 богачей
        top_rich = await session.query(User).order_by(User.balance.desc()).limit(5).all()
        top_text = "\n".join(f"  {i+1}. {u.first_name} — {u.balance:,.0f}" for i, u in enumerate(top_rich))
        
        # Активность за 24 часа
        yesterday = datetime.now() - timedelta(days=1)
        active_users = await session.query(func.count(func.distinct(Transaction.user_id))).filter(
            Transaction.timestamp >= yesterday
        ).scalar() or 0
        
        stats_text = f"""
📊 СТАТИСТИКА БОТА

👥 Игроков: {total_users}
👤 Активных за 24ч: {active_users}

💰 Общий баланс: {total_balance:,.0f} 🪙
📊 Лимит монет: {config.TOTAL_MONEY_LIMIT:,}
📈 Заполненность: {(total_balance/config.TOTAL_MONEY_LIMIT*100):.1f}%

⛏ Майнеров: {total_miners}
🏪 Бизнесов: {total_businesses}

🏦 В депозитах: {total_deposits:,.0f}
💳 Кредитов выдано: {total_loans:,.0f}

💎 Инфляция: {inflation_multiplier:.3f}
🚨 Кризис: {'Да' if crisis_active else 'Нет'}
🎉 Бум: {'Да' if boom_active else 'Нет'}

🏆 ТОП-5 БОГАЧЕЙ:
{top_text}
"""
        await message.answer(stats_text)


# ============================================================
# СИСТЕМА ИНФЛЯЦИИ / ДЕФЛЯЦИИ
# ============================================================

async def check_inflation(bot: Bot):
    """Проверка и корректировка инфляции (каждые 6 часов)"""
    global inflation_multiplier
    
    total_money = await get_total_money_supply()
    total_percentage = (total_money / config.TOTAL_MONEY_LIMIT) * 100
    
    action = ""
    
    if total_percentage > 95:
        # ИНФЛЯЦИЯ
        inflation_multiplier *= 1.02
        action = "ИНФЛЯЦИЯ"
        
        # Влияние на цены криптовалют
        for symbol in config.CRYPTO:
            config.CRYPTO[symbol]['price'] *= 1.02
        
        # Отключаем эмиссию (уменьшаем зарплаты)
        for prof in config.SALARIES:
            config.SALARIES[prof] *= 0.98
    
    elif total_percentage < 30:
        # ДЕФЛЯЦИЯ
        inflation_multiplier *= 0.99
        action = "ДЕФЛЯЦИЯ"
        
        # Снижаем цены
        for symbol in config.CRYPTO:
            config.CRYPTO[symbol]['price'] *= 0.99
        
        # Ускоряем эмиссию
        for prof in config.SALARIES:
            config.SALARIES[prof] *= 1.02
    
    else:
        action = "СТАБИЛЬНОСТЬ"
    
    # Логируем
    async with get_session() as session:
        log = InflationLog(
            total_supply=total_money,
            rate=inflation_multiplier,
            action=action
        )
        session.add(log)
        await session.commit()
    
    # Уведомляем админа
    await bot.send_message(
        config.ADMIN_ID,
        f"📊 ЭКОНОМИКА: {action}\n"
        f"💰 В обращении: {total_money:,.0f} / {config.TOTAL_MONEY_LIMIT:,} ({total_percentage:.1f}%)\n"
        f"📈 Мультипликатор: {inflation_multiplier:.4f}"
    )


# ============================================================
# ОБНОВЛЕНИЕ КУРСОВ КРИПТОВАЛЮТ
# ============================================================

async def update_crypto_prices():
    """Обновление курсов криптовалют (каждые 10 минут)"""
    for symbol, data in config.CRYPTO.items():
        volatility = data['volatility']
        
        # Случайное изменение в пределах волатильности
        change = random.uniform(-volatility, volatility)
        
        # Учитываем инфляцию
        change *= inflation_multiplier
        
        # Учитываем кризис/бум
        if crisis_active:
            change -= 0.05  # Падение на 5%
        elif boom_active:
            change += 0.05  # Рост на 5%
        
        new_price = data['price'] * (1 + change)
        new_price = max(0.0001, new_price)  # Минимальная цена
        
        config.CRYPTO[symbol]['price'] = round(new_price, 4)


# ============================================================
# ПАССИВНЫЙ ДОХОД ОТ БИЗНЕСОВ
# ============================================================

async def process_business_income(bot: Bot):
    """Начисление пассивного дохода от бизнесов (каждые 24 часа)"""
    async with get_session() as session:
        businesses = await session.query(Business).all()
        
        total_paid = 0
        users_paid = set()
        
        for biz in businesses:
            biz_config = config.BUSINESSES.get(biz.business_type)
            if not biz_config:
                continue
            
            income = biz_config['income'] * biz.quantity
            
            # Учитываем кризис/бум
            if crisis_active:
                income *= 0.80  # -20%
            elif boom_active:
                income *= 1.50  # +50%
            
            user = await get_user(biz.user_id)
            if user:
                user.balance += income
                total_paid += income
                users_paid.add(biz.user_id)
                
                # Уведомляем игрока
                try:
                    await bot.send_message(
                        biz.user_id,
                        f"💼 ПАССИВНЫЙ ДОХОД!\n"
                        f"🏪 {biz.business_type.title()} x{biz.quantity}\n"
                        f"💰 Доход: {income:,.0f} монет"
                    )
                except:
                    pass
        
        await session.commit()
        
        # Логируем
        await log_action(bot, config.ADMIN_ID,
            f"💼 Пассивный доход начислен\n"
            f"Выплачено: {total_paid:,.0f}\n"
            f"Получателей: {len(users_paid)}"
        )


# ============================================================
# ПРОВЕРКА КРЕДИТОВ
# ============================================================

async def check_overdue_loans(bot: Bot):
    """Проверка просроченных кредитов (каждые 6 часов)"""
    async with get_session() as session:
        overdue_loans = await session.query(Loan).filter(
            Loan.active == True,
            Loan.end_date < datetime.now()
        ).all()
        
        for loan in overdue_loans:
            days_overdue = (datetime.now() - loan.end_date).days
            
            # Начисляем пеню 2% в день
            penalty = loan.debt * (config.PENALTY_RATE * days_overdue)
            loan.debt += penalty
            loan.overdue_days = days_overdue
            
            # Если просрочка > 7 дней — арест имущества
            if days_overdue > 7:
                user = await get_user(loan.user_id)
                if user:
                    # Обнуляем баланс
                    user.balance = 0
                    # Удаляем майнеры
                    await session.query(Miner).filter(Miner.user_id == loan.user_id).delete()
                    # Удаляем бизнесы
                    await session.query(Business).filter(Business.user_id == loan.user_id).delete()
                    
                    loan.active = False
                    
                    try:
                        await bot.send_message(
                            loan.user_id,
                            "🚨 АРЕСТ ИМУЩЕСТВА!\n\n"
                            f"Кредит просрочен на {days_overdue} дней.\n"
                            "Всё имущество конфисковано!\n"
                            "Баланс обнулён."
                        )
                    except:
                        pass
                    
                    await log_action(bot, config.ADMIN_ID,
                        f"🚨 Арест имущества: @{user.username}\n"
                        f"Просрочка: {days_overdue} дней\n"
                        f"Долг: {loan.debt:,.0f}"
                    )
            
            await session.commit()
            
            # Уведомляем о просрочке
            if days_overdue <= 7:
                try:
                    await bot.send_message(
                        loan.user_id,
                        f"⚠️ ПРОСРОЧКА ПО КРЕДИТУ!\n\n"
                        f"Дней просрочки: {days_overdue}\n"
                        f"Текущий долг: {loan.debt:,.0f}\n"
                        f"Пеня: {penalty:,.0f} монет\n\n"
                        f"Погасите кредит в течение {7 - days_overdue} дней!"
                    )
                except:
                    pass


# ============================================================
# АУКЦИОН — ПРОВЕРКА ЛОТОВ
# ============================================================

async def check_auction_lots(bot: Bot):
    """Проверка и закрытие истекших лотов (каждую минуту)"""
    async with get_session() as session:
        expired_lots = await session.query(AuctionLot).filter(
            AuctionLot.active == True,
            AuctionLot.end_time <= datetime.now()
        ).all()
        
        for lot in expired_lots:
            lot.active = False
            
            if lot.current_bid and lot.buyer_id:
                # Лот продан
                commission = lot.current_bid * 0.03  # 3% комиссия
                seller_amount = lot.current_bid - commission
                
                seller = await get_user(lot.seller_id)
                if seller:
                    seller.balance += seller_amount
                
                buyer = await get_user(lot.buyer_id)
                
                # Передаём предмет покупателю
                if lot.item_type == 'miner':
                    await add_miner(lot.buyer_id, lot.item_name)
                elif lot.item_type == 'business':
                    await add_business(lot.buyer_id, lot.item_name)
                
                # Уведомления
                try:
                    await bot.send_message(
                        lot.seller_id,
                        f"🔨 ЛОТ ПРОДАН!\n"
                        f"Предмет: {lot.item_name}\n"
                        f"Сумма: {lot.current_bid:,.0f}\n"
                        f"Комиссия: {commission:,.0f}\n"
                        f"💵 Получено: {seller_amount:,.0f}"
                    )
                except:
                    pass
                
                try:
                    await bot.send_message(
                        lot.buyer_id,
                        f"🎉 ЛОТ ВЫИГРАН!\n"
                        f"Предмет: {lot.item_name}\n"
                        f"Сумма: {lot.current_bid:,.0f}"
                    )
                except:
                    pass
            
            await session.commit()


# ============================================================
# ВЫПЛАТА ДИВИДЕНДОВ КОРПОРАЦИЙ
# ============================================================

async def pay_corporation_dividends(bot: Bot):
    """Выплата дивидендов корпораций (раз в неделю)"""
    async with get_session() as session:
        corporations = await session.query(Corporation).all()
        
        for corp in corporations:
            members = await session.query(CorporationMember).filter(
                CorporationMember.corp_id == corp.id
            ).all()
            
            if not members or corp.fund <= 0:
                continue
            
            total_contribution = sum(m.contribution for m in members)
            if total_contribution == 0:
                continue
            
            # Распределяем 30% прибыли
            dividend_pool = corp.fund * 0.30
            
            for member in members:
                share = (member.contribution / total_contribution) * dividend_pool
                user = await get_user(member.user_id)
                if user:
                    user.balance += share
                    
                    try:
                        await bot.send_message(
                            member.user_id,
                            f"💰 ДИВИДЕНДЫ!\n"
                            f"🏛 Корпорация: {corp.name}\n"
                            f"💵 Сумма: {share:,.0f} монет"
                        )
                    except:
                        pass
            
            corp.fund -= dividend_pool
            await session.commit()


# ============================================================
# ЕЖЕДНЕВНЫЙ БОНУС
# ============================================================

async def reset_daily_bonuses():
    """Сброс ежедневных бонусов (в полночь)"""
    async with get_session() as session:
        # Сбрасываем флаг last_daily для всех
        pass


# ============================================================
# ОЧИСТКА СТАРЫХ ДАННЫХ
# ============================================================

async def cleanup_old_data():
    """Очистка старых логов и данных (раз в неделю)"""
    async with get_session() as session:
        week_ago = datetime.now() - timedelta(days=7)
        
        # Удаляем старые логи транзакций
        await session.query(Transaction).filter(
            Transaction.timestamp < week_ago
        ).delete()
        
        # Удаляем старые логи инфляции
        await session.query(InflationLog).filter(
            InflationLog.timestamp < week_ago
        ).delete()
        
        await session.commit()


# ============================================================
# РАССЫЛКА
# ============================================================

async def broadcast_message(bot: Bot, text: str):
    """Отправка сообщения всем пользователям"""
    async with get_session() as session:
        users = await session.query(User).all()
        
        sent_count = 0
        failed_count = 0
        
        for user in users:
            try:
                await bot.send_message(user.user_id, text)
                sent_count += 1
                await asyncio.sleep(0.05)  # Задержка для избежания флуда
            except:
                failed_count += 1
        
        await bot.send_message(
            config.ADMIN_ID,
            f"📢 Рассылка завершена\n"
            f"✅ Отправлено: {sent_count}\n"
            f"❌ Не доставлено: {failed_count}"
        )


# ============================================================
# ФОНОВЫЕ ЗАДАЧИ (ШЕДУЛЕР)
# ============================================================

async def scheduler_loop(bot: Bot):
    """Главный цикл фоновых задач"""
    print("🔄 Шедулер запущен")
    
    last_business_income = datetime.now()
    last_crypto_update = datetime.now()
    last_inflation_check = datetime.now()
    last_loan_check = datetime.now()
    last_dividend_pay = datetime.now()
    last_cleanup = datetime.now()
    
    while True:
        now = datetime.now()
        
        # Каждую минуту — проверка аукционов
        try:
            await check_auction_lots(bot)
        except Exception as e:
            print(f"Ошибка аукциона: {e}")
        
        # Каждые 10 минут — обновление крипты
        if (now - last_crypto_update).total_seconds() >= 600:
            try:
                await update_crypto_prices()
                last_crypto_update = now
            except Exception as e:
                print(f"Ошибка крипты: {e}")
        
        # Каждые 6 часов — проверка инфляции
        if (now - last_inflation_check).total_seconds() >= 21600:
            try:
                await check_inflation(bot)
                last_inflation_check = now
            except Exception as e:
                print(f"Ошибка инфляции: {e}")
        
        # Каждые 6 часов — проверка кредитов
        if (now - last_loan_check).total_seconds() >= 21600:
            try:
                await check_overdue_loans(bot)
                last_loan_check = now
            except Exception as e:
                print(f"Ошибка кредитов: {e}")
        
        # Каждые 24 часа — пассивный доход
        if (now - last_business_income).total_seconds() >= 86400:
            try:
                await process_business_income(bot)
                last_business_income = now
            except Exception as e:
                print(f"Ошибка бизнеса: {e}")
        
        # Раз в неделю — дивиденды
        if (now - last_dividend_pay).total_seconds() >= 604800:
            try:
                await pay_corporation_dividends(bot)
                last_dividend_pay = now
            except Exception as e:
                print(f"Ошибка дивидендов: {e}")
        
        # Раз в неделю — очистка
        if (now - last_cleanup).total_seconds() >= 604800:
            try:
                await cleanup_old_data()
                last_cleanup = now
            except Exception as e:
                print(f"Ошибка очистки: {e}")
        
        # Проверка окончания кризиса
        global crisis_active, crisis_end_time
        if crisis_active and crisis_end_time and now >= crisis_end_time:
            crisis_active = False
            await bot.send_message(config.ADMIN_ID, "📊 Кризис завершён!")
            await broadcast_message(bot, "📈 Кризис завершён! Экономика восстанавливается.")
        
        # Проверка окончания бума
        global boom_active, boom_end_time
        if boom_active and boom_end_time and now >= boom_end_time:
            boom_active = False
            await bot.send_message(config.ADMIN_ID, "📊 Бум завершён!")
        
        await asyncio.sleep(60)  # Проверка каждую минуту

print("👑 admin_panel.py загружен")
print(f"   Админ-команд: 10+")
print(f"   Шедулер: аукцион, крипта, инфляция, кредиты, бизнес, дивиденды")
# ============================================================
# main.py - ГЛАВНЫЙ ФАЙЛ, ЗАПУСК БОТА, ДИСПЕТЧЕР
# ============================================================

import asyncio
import sys
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (Message, CallbackQuery, BotCommand, 
                           BotCommandScopeDefault, Update)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Импорт всех модулей
from config import *
from game_mechanics import *
from handlers import *
from admin_panel import *

# ============================================================
# НАСТРОЙКА ЛОГГИРОВАНИЯ
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ============================================================
# ИНИЦИАЛИЗАЦИЯ БОТА И ДИСПЕТЧЕРА
# ============================================================

# Создаём бота с настройками по умолчанию
bot = Bot(
    token=config.TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# ============================================================
# КОМАНДЫ БОТА (ОТОБРАЖЕНИЕ В МЕНЮ)
# ============================================================

async def set_bot_commands():
    """Установка команд бота в меню Telegram"""
    commands = [
        BotCommand(command="start", description="🔄 Начать игру / Главное меню"),
        BotCommand(command="help", description="📖 Помощь по командам"),
        BotCommand(command="menu", description="📱 Показать главное меню"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

# ============================================================
# MIDDLEWARE
# ============================================================

class UserMiddleware:
    """
    Middleware для автоматической регистрации пользователя
    и проверки мута
    """
    
    async def __call__(self, handler, event, data):
        # Проверяем, есть ли сообщение
        if hasattr(event, 'from_user') and event.from_user:
            user_id = event.from_user.id
            
            # Проверяем мут
            user = await get_user(user_id)
            if user and user.mute_until:
                if datetime.now() < user.mute_until:
                    # Игрок в муте — игнорируем сообщение
                    if hasattr(event, 'answer'):
                        remaining = (user.mute_until - datetime.now()).seconds
                        minutes = remaining // 60
                        await event.answer(f"🔇 Вы в муте ещё {minutes} мин.")
                    return
                else:
                    # Мут истёк — сбрасываем
                    async with get_session() as session:
                        usr = await session.query(User).filter(User.user_id == user_id).first()
                        if usr:
                            usr.mute_until = None
                            await session.commit()
        
        # Продолжаем обработку
        return await handler(event, data)

# Регистрируем middleware
dp.message.middleware(UserMiddleware())
dp.callback_query.middleware(UserMiddleware())

# ============================================================
# ОБРАБОТЧИКИ КОМАНД
# ============================================================

@dp.message(CommandStart())
async def command_start(message: Message):
    """Обработчик /start"""
    await cmd_start(message, bot)

@dp.message(Command("help"))
async def command_help(message: Message):
    """Обработчик /help"""
    await cmd_help(message)

@dp.message(Command("menu"))
async def command_menu(message: Message):
    """Показать главное меню"""
    await message.answer("📱 Главное меню:", reply_markup=get_main_menu())

# ============================================================
# ОБРАБОТЧИКИ ТЕКСТОВЫХ КОМАНД
# ============================================================

@dp.message(F.text)
async def handle_all_messages(message: Message):
    """
    Главный обработчик всех текстовых сообщений.
    Сначала проверяет админ-команды, потом игровые.
    """
    user_id = message.from_user.id
    text = message.text.strip() if message.text else ""
    
    # Логируем входящее сообщение
    logger.info(f"Сообщение от @{message.from_user.username} (ID:{user_id}): {text[:100]}")
    
    # Проверяем, не админ-команда ли это
    if message.chat.type == 'private':
        is_admin = await handle_admin_commands(message, bot)
        if is_admin:
            return
    
    # Проверяем регистрацию
    user = await get_user(user_id)
    if not user:
        # Авто-регистрация
        user = await register_user(
            user_id=user_id,
            username=message.from_user.username or f"user_{user_id}",
            first_name=message.from_user.first_name or "Игрок"
        )
        await message.answer(
            f"🎉 ДОБРО ПОЖАЛОВАТЬ, {user.first_name}!\n\n"
            f"💰 Стартовый баланс: {config.START_BALANCE:,} монет\n"
            f"💡 Напишите 'помощь' для списка команд\n"
            f"💼 Начните с команды 'работа'",
            reply_markup=get_main_menu()
        )
        await log_action(bot, config.ADMIN_ID, f"🆕 Новый игрок: @{user.username}")
        return
    
    # Обрабатываем игровые команды
    text_lower = text.lower().strip()
    
    # Быстрые команды (без аргументов)
    quick_commands = {
        "работа": lambda: do_work(user_id),
        "забрать": lambda: collect_mining(user_id),
        "крипта": lambda: "📈 КУРСЫ КРИПТОВАЛЮТ\n\n" + "\n".join(
            f"{d['icon']} {d['name']} ({s.upper()}): {d['price']:,.4f} 🪙"
            for s, d in config.CRYPTO.items()
        ),
        "профиль": lambda: get_profile_text(user),
        "помощь": lambda: get_help_text(),
        "топ": lambda: get_top_players(),
        "аукцион": lambda: get_active_auctions(),
        "казино": lambda: ("🎰 КАЗИНО\n\nВыберите игру:", get_casino_menu()),
        "бизнес": lambda: ("🏪 БИЗНЕС\n\nВыберите бизнес:", get_business_menu()),
        "меню": lambda: ("📱 Главное меню:", get_main_menu()),
    }
    
    if text_lower in quick_commands:
        result = quick_commands[text_lower]()
        if isinstance(result, tuple):
            await message.answer(result[0], reply_markup=result[1])
        else:
            await message.answer(result)
        return
    
    # Команды с аргументами
    try:
        await handle_text_commands(message, bot)
    except Exception as e:
        logger.error(f"Ошибка обработки команды: {e}", exc_info=True)
        await message.answer(
            "❌ Произошла ошибка! Попробуйте позже.\n"
            "📖 Напишите 'помощь' для списка команд."
        )

# ============================================================
# ОБРАБОТЧИКИ CALLBACK-ЗАПРОСОВ
# ============================================================

@dp.callback_query()
async def handle_all_callbacks(callback: CallbackQuery):
    """Главный обработчик всех callback-запросов"""
    user_id = callback.from_user.id
    data = callback.data
    
    logger.info(f"Callback от @{callback.from_user.username}: {data}")
    
    try:
        await process_callback(callback, bot)
    except Exception as e:
        logger.error(f"Ошибка callback: {e}", exc_info=True)
        await callback.answer("❌ Ошибка! Попробуйте снова.", show_alert=True)

# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

async def get_profile_text(user: User) -> str:
    """Текст профиля"""
    miners = await get_miners(user.user_id)
    businesses = await get_businesses(user.user_id)
    crypto = await get_user_crypto(user.user_id)
    
    # Считаем общую стоимость
    total_miners_value = sum(
        config.MINERS[m.model]['price'] * m.quantity 
        for m in miners 
        if m.model in config.MINERS
    )
    total_business_value = sum(
        config.BUSINESSES[b.business_type]['price'] * b.quantity 
        for b in businesses 
        if b.business_type in config.BUSINESSES
    )
    total_crypto_value = sum(
        config.CRYPTO[c.symbol]['price'] * c.amount 
        for c in crypto 
        if c.symbol in config.CRYPTO
    )
    
    net_worth = user.balance + total_miners_value + total_business_value + total_crypto_value
    
    level_config = config.LEVELS.get(user.level, {})
    title = level_config.get('title', 'Новичок')
    
    return f"""
👤 ПРОФИЛЬ ИГРОКА

🆔 ID: {user.user_id}
👤 Имя: {user.first_name}
📛 Username: @{user.username}
⭐ Уровень: {user.level} ({title})
💼 Профессия: {user.profession}
🏅 Престиж: {user.prestige}

💰 БАЛАНС: {user.balance:,.0f} 🪙

📊 АКТИВЫ:
  ⛏ Майнеры: {len(miners)} шт ({total_miners_value:,.0f} 🪙)
  🏪 Бизнесы: {len(businesses)} шт ({total_business_value:,.0f} 🪙)
  🪙 Крипта: {len(crypto)} видов ({total_crypto_value:,.0f} 🪙)

💎 ЧИСТЫЙ КАПИТАЛ: {net_worth:,.0f} 🪙

📈 Статистика:
  💵 Заработано: {user.total_earned:,.0f}
  💸 Потрачено: {user.total_spent:,.0f}
  📅 В игре с: {user.created_at.strftime('%d.%m.%Y') if user.created_at else 'Сегодня'}
"""

async def get_help_text() -> str:
    """Текст помощи"""
    return """
📖 ПОМОЩЬ ПО КОМАНДАМ

💼 РАБОТА:
  работа — получить зарплату (раз в час)

⛏ МАЙНИНГ:
  майнить монеты — начать майнинг
  забрать — забрать добычу
  купить майнер [модель] — купить майнер

🏪 БИЗНЕС:
  купить киоск / кафе / магазин / ресторан / сеть

🏦 БАНК:
  вклад [дни] [сумма] — открыть вклад
  забрать вклад — закрыть вклад
  кредит [сумма] — взять кредит
  погасить кредит — погасить кредит

📈 КРИПТА:
  крипта — курсы
  купить btc [кол-во]
  продать btc [кол-во]

🎰 КАЗИНО:
  рулетка [ставка] [сумма]
  кубы [сумма]
  слоты [сумма]
  краш [сумма]
  блэкджек [сумма]
  сапёр [мины] [сумма]

🏠 НЕДВИЖИМОСТЬ:
  купить студию / 1-комнатную / пентхаус / замок

🚗 ТРАНСПОРТ:
  купить bmw / tesla / lamborghini / вертолёт

🔫 ОГРАБЛЕНИЕ:
  ограбить @username

👥 КЛАНЫ:
  создать клан [название]
  вступить в клан [id]

🎁 ПРОМОКОД:
  промокод [код]

📊 ТОП:
  топ — топ-10 игроков
"""

async def get_top_players() -> str:
    """Топ-10 игроков"""
    async with get_session() as session:
        top_users = await session.query(User).order_by(User.balance.desc()).limit(10).all()
        
        text = "📊 ТОП-10 ИГРОКОВ\n\n"
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i, u in enumerate(top_users):
            text += f"{medals[i]} {u.first_name} — {u.balance:,.0f} 🪙\n"
        
        return text

async def get_active_auctions() -> str:
    """Активные аукционные лоты"""
    async with get_session() as session:
        lots = await session.query(AuctionLot).filter(
            AuctionLot.active == True,
            AuctionLot.end_time > datetime.now()
        ).order_by(AuctionLot.end_time).limit(10).all()
        
        if not lots:
            return "📊 Нет активных лотов"
        
        text = "🔨 АКТИВНЫЕ ЛОТЫ\n\n"
        for lot in lots:
            time_left = lot.end_time - datetime.now()
            hours = int(time_left.total_seconds() / 3600)
            current_bid = lot.current_bid or lot.start_price
            seller = await get_user(lot.seller_id)
            
            text += (
                f"🆔 Лот #{lot.id}\n"
                f"📦 {lot.item_name} x{lot.quantity}\n"
                f"💰 Текущая ставка: {current_bid:,.0f}\n"
                f"👤 Продавец: @{seller.username if seller else 'Unknown'}\n"
                f"⏳ Осталось: {hours} ч.\n\n"
            )
        
        return text

# ============================================================
# ОБРАБОТЧИК ОШИБОК
# ============================================================

@dp.errors()
async def error_handler(update: Update, exception: Exception):
    """Глобальный обработчик ошибок"""
    logger.error(f"Ошибка при обработке {update}: {exception}", exc_info=True)
    
    # Отправляем админу
    try:
        await bot.send_message(
            config.ADMIN_ID,
            f"🚨 ОШИБКА БОТА\n\n"
            f"Update: {update}\n"
            f"Error: {exception}"
        )
    except:
        pass
    
    return True  # Продолжаем работу

# ============================================================
# ЗАПУСК БОТА
# ============================================================

async def on_startup():
    """Действия при запуске бота"""
    print("=" * 50)
    print("🚀 ЗАПУСК ECONOMY BOT")
    print("=" * 50)
    
    # Инициализация БД
    print("📦 Инициализация базы данных...")
    await init_db()
    print("✅ База данных готова")
    
    # Установка команд
    print("📋 Установка команд бота...")
    await set_bot_commands()
    print("✅ Команды установлены")
    
    # Создаём админа если нет
    print("👑 Проверка администратора...")
    admin = await get_user(config.ADMIN_ID)
    if not admin:
        await register_user(
            user_id=config.ADMIN_ID,
            username="admin",
            first_name="Администратор"
        )
        print("✅ Администратор создан")
    else:
        print("✅ Администратор найден")
    
    # Запускаем шедулер
    print("🔄 Запуск фоновых задач...")
    asyncio.create_task(scheduler_loop(bot))
    print("✅ Шедулер запущен")
    
    # Отправляем уведомление админу
    try:
        await bot.send_message(
            config.ADMIN_ID,
            f"✅ БОТ ЗАПУЩЕН!\n\n"
            f"🕐 Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
            f"📦 База данных: PostgreSQL\n"
            f"👥 Игроков: {await get_users_count()}\n"
            f"💰 Монет в системе: {await get_total_money_supply():,.0f}"
        )
    except Exception as e:
        print(f"⚠️ Не удалось отправить уведомление админу: {e}")
    
    print("=" * 50)
    print("✅ БОТ ГОТОВ К РАБОТЕ!")
    print("=" * 50)

async def on_shutdown():
    """Действия при остановке бота"""
    print("\n" + "=" * 50)
    print("🛑 ОСТАНОВКА БОТА")
    print("=" * 50)
    
    try:
        await bot.send_message(
            config.ADMIN_ID,
            f"⚠️ БОТ ОСТАНОВЛЕН!\n"
            f"🕐 Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )
    except:
        pass
    
    print("👋 До свидания!")

async def get_users_count() -> int:
    """Количество пользователей"""
    async with get_session() as session:
        return await session.query(func.count(User.id)).scalar() or 0

# ============================================================
# ТОЧКА ВХОДА
# ============================================================

async def main():
    """Главная функция запуска"""
    # Регистрируем функции старта/остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Запускаем поллинг
    print("🔌 Подключение к Telegram API...")
    await dp.start_polling(
        bot,
        skip_updates=True,  # Пропускаем старые сообщения
        allowed_updates=["message", "callback_query"]
    )

if __name__ == "__main__":
    try:
        print("\n" + "🎮" * 25)
        print("ECONOMY BOT v2.0")
        print("Разработка: ИИ-Помощник")
        print("🎮" * 25 + "\n")
        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
