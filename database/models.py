from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Clase base declarativa de SQLAlchemy."""
    pass


class Usuario(Base):
    """Representa un usuario del sistema FocusMind."""
    
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo_plan: Mapped[str] = mapped_column(String(50), default="Free")  # 'Free' o 'Premium'
    
    # Relaciones relacionales (cascade delete asegura consistencia)
    habitos: Mapped[List["Habito"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )
    historial_dopamina: Mapped[List["HistorialDopamina"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )
    estado_entorno: Mapped[Optional["EstadoEntorno"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )


class Habito(Base):
    """Representa un hábito diario de un usuario."""
    
    __tablename__ = "habitos"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500))
    estado_actual: Mapped[bool] = mapped_column(Boolean, default=False)
    racha_actual: Mapped[int] = mapped_column(Integer, default=0)
    
    usuario: Mapped["Usuario"] = relationship(back_populates="habitos")


class HistorialDopamina(Base):
    """Métricas pre/post sesión de enfoque y dopamina."""
    
    __tablename__ = "historial_dopamina"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Las métricas cognitivas se limitan de 1 a 5 usando CheckConstraints
    energia_pre: Mapped[int] = mapped_column(
        Integer, CheckConstraint("energia_pre BETWEEN 1 AND 5"), nullable=False
    )
    motivacion_pre: Mapped[int] = mapped_column(
        Integer, CheckConstraint("motivacion_pre BETWEEN 1 AND 5"), nullable=False
    )
    energia_post: Mapped[int] = mapped_column(
        Integer, CheckConstraint("energia_post BETWEEN 1 AND 5"), nullable=False
    )
    motivacion_post: Mapped[int] = mapped_column(
        Integer, CheckConstraint("motivacion_post BETWEEN 1 AND 5"), nullable=False
    )
    bloques_completados: Mapped[int] = mapped_column(Integer, default=0)
    
    usuario: Mapped["Usuario"] = relationship(back_populates="historial_dopamina")


class EstadoEntorno(Base):
    """Nivel del entorno y estado serializado de los objetos de la habitación."""
    
    __tablename__ = "estado_entorno"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    habitacion_level: Mapped[int] = mapped_column(Integer, default=1)
    
    # items_ordenados_json almacena estados ej: {"bed": "clean", "desk": "messy"}
    items_ordenados_json: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    usuario: Mapped["Usuario"] = relationship(back_populates="estado_entorno")
