import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = None
SessionLocal = None
Base = declarative_base()

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class FarmData(Base):
    __tablename__ = "farm_data"
    
    id = Column(Integer, primary_key=True, index=True)
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    ph = Column(Float)
    soil_type = Column(String(50))
    previous_crop = Column(String(100))
    season = Column(String(50))
    crop_duration = Column(String(20))
    recommended_crop = Column(String(100))
    predicted_yield = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class FertilizerRecommendation(Base):
    __tablename__ = "fertilizer_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100))
    growth_stage = Column(String(50))
    fertilizer_type = Column(String(20))
    fertilizer_name = Column(String(100))
    application_rate = Column(String(100))
    application_method = Column(Text)
    timing = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class MultiCropPlan(Base):
    __tablename__ = "multi_crop_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    main_crop = Column(String(100))
    companion_crops = Column(Text)
    spacing_main = Column(String(50))
    spacing_companion = Column(String(50))
    irrigation_schedule = Column(Text)
    benefits = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class CropHistory(Base):
    __tablename__ = "crop_history"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100))
    season = Column(String(50))
    year = Column(Integer)
    yield_amount = Column(Float)
    soil_type = Column(String(50))
    fertilizer_used = Column(String(100))
    organic = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    if engine is not None:
        Base.metadata.create_all(bind=engine)

def get_db():
    if SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        return db
    finally:
        pass
