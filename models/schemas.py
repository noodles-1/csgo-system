import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    username: Mapped[str] = mapped_column(String(50))
    fullName: Mapped[str] = mapped_column(String(80))
    isAdmin: Mapped[bool]
    password: Mapped[str]

    def __repr__(self) -> str:
        return f'User(userId={self.id}, email={self.email}, name={self.name})'
    
class Camera(Base):
    __tablename__ = 'camera'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f'Camera(cameraId={self.id}, name={self.name})'

class DetectedLicensePlate(Base):
    __tablename__ = 'detected_license_plate'

    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey('user.id'))
    cameraId: Mapped[int] = mapped_column(ForeignKey('camera.id'))
    licenseNumber: Mapped[str] = mapped_column(String(14))
    vehicleType: Mapped[str]
    dateTime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f'Detection(id={self.id}, userId={self.userId}, cameraId={self.cameraId}, licenseNumber={self.licenseNumber}, vehicleType={self.vehicleType}, dateTime={self.dateTime})'