from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    '''
    User table with columns ID (PK), email, username, full name, is admin, and password.
    '''
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    username: Mapped[str] = mapped_column(String(50))
    fullName: Mapped[str] = mapped_column(String(80))
    isAdmin: Mapped[bool]
    password: Mapped[str]

    def __repr__(self) -> str:
        return f'User(userId={self.id}, email={self.email}, username={self.username}, fullName={self.fullName}, isAdmin={self.isAdmin})'
    
class Camera(Base):
    '''
    Camera table with columns ID (PK) and the camera name.
    '''
    __tablename__ = 'camera'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f'Camera(cameraId={self.id}, name={self.name})'
    
class Price(Base):
    '''
    Price table that associates a variable price with a corresponding vehicle type.
    '''
    __tablename__ = 'price'

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicleType: Mapped[str]
    price: Mapped[float]

    def __repr__(self) -> str:
        return f'Price(priceId={self.id}, vehicleType={self.vehicleType})'

class DetectedLicensePlate(Base):
    '''
    DetectedLicensePlate table with columns ID (PK), user ID (FK from User), camera ID (FK from Camera),
    license number, vehicle type, and datetime of detection.
    '''
    __tablename__ = 'detected_license_plate'

    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey('user.id'))
    cameraId: Mapped[int] = mapped_column(ForeignKey('camera.id'))
    priceId: Mapped[int] = mapped_column(ForeignKey('price.id'))
    licenseNumber: Mapped[str] = mapped_column(String(14))
    date: Mapped[Date] = mapped_column(Date())
    time: Mapped[Time] = mapped_column(Time(timezone=True))
    image: Mapped[str]

    def __repr__(self) -> str:
        return f'Detection(id={self.id}, userId={self.userId}, cameraId={self.cameraId}, priceId={self.priceId}, licenseNumber={self.licenseNumber}, date={self.date}, time={self.time}, image={self.image})'