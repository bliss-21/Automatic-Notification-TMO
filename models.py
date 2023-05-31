from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Manga(Base):
    __tablename__ = 'manga'
    id = Column(Integer, primary_key=True)
    titulo_manga = Column(String)
    link_manga = Column(String)
    ultimo_capitulo = Column(String)
    fecha_agregado = Column(Date)
    fecha_actualizado = Column(Date)
    activo = Column(Boolean, default=True)

class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    link_capitulo = Column(String)
    titulo_manga = Column(String)
    nombre_capitulo = Column(String)
    fecha_creado = Column(Date)
    fecha_notificado = Column(Date, nullable=True)
    notificado = Column(Boolean, default=False)

    manga_id = Column(Integer, ForeignKey('manga.id'))
    manga = relationship("Manga")