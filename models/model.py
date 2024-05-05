import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'

    userId: Mapped[int] = mapped_column(primary_key=True, autoincrement='auto')
    email: Mapped[str]
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str]

    def __repr__(self) -> str:
        return f'User(userId={self.userId}, email={self.email}, name={self.name})'
    
class Camera(Base):
    __tablename__ = 'camera'

    cameraId: Mapped[int] = mapped_column(primary_key=True, autoincrement='auto')
    name: Mapped[str]

    def __repr__(self) -> str:
        return f'Camera(cameraId={self.cameraId}, name={self.name})'

class DetectedLicensePlate(Base):
    __tablename__ = 'detected_license_plate'

    detectionId: Mapped[int] = mapped_column(primary_key=True, autoincrement='auto')
    userId: Mapped[int] = relationship(ForeignKey('user.userId'))
    cameraId: Mapped[int] = relationship(ForeignKey('camera.cameraId'))
    licenseNumber: Mapped[str] = mapped_column(String(14))
    vehicleType: Mapped[str]
    dateTime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f'Detection(detectionId={self.detectionId}, userId={self.userId}, cameraId={self.cameraId}, licenseNumber={self.licenseNumber}, vehicleType={self.vehicleType}, dateTime={self.dateTime})'