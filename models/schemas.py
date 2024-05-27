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
    User table with columns ID (PK), email, username, full name, is admin, and privilege
    to change vehicles to detect, congestion prices, edit hours, and download CSV.
    '''
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    username: Mapped[str] = mapped_column(String(50))
    firstName: Mapped[str] = mapped_column(String(80))
    lastName: Mapped[str] = mapped_column(String(80))
    isAdmin: Mapped[bool]
    canChangeDetect: Mapped[bool]
    canChangePrice: Mapped[bool]
    canEditHours: Mapped[bool]
    canDownload: Mapped[bool]
    password: Mapped[str]

    def __repr__(self) -> str:
        return f'User(userId={self.id}, email={self.email}, username={self.username}, fullName={self.firstName} {self.lastName}, isAdmin={self.isAdmin})'
    
class Camera(Base):
    '''
    Camera table with columns ID containing the IP address (PK) and the camera name.
    '''
    __tablename__ = 'camera'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]

    def __repr__(self) -> str:
        return f'Camera(cameraId={self.id}, name={self.name}, location={self.location})'

class DetectedLicensePlate(Base):
    '''
    DetectedLicensePlate table with columns ID (PK), user ID (FK from User), camera ID (FK from Camera),
    license number, vehicle type, and datetime of detection.
    '''
    __tablename__ = 'detected_license_plate'

    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey('user.id'))
    cameraId: Mapped[int] = mapped_column(ForeignKey('camera.id'))
    settingId: Mapped[int] = mapped_column(ForeignKey('setting.id'))
    licenseNumber: Mapped[str] = mapped_column(String(14))
    vehicleType: Mapped[str]
    price: Mapped[float]
    date: Mapped[Date] = mapped_column(Date())
    time: Mapped[Time] = mapped_column(Time(timezone=True))
    image: Mapped[str]

    def __repr__(self) -> str:
        return f'Detection(id={self.id}, userId={self.userId}, cameraId={self.cameraId}, priceId={self.priceId}, licenseNumber={self.licenseNumber}, date={self.date}, time={self.time}, image={self.image})'
    
class Setting(Base):
    '''
    Setting table that contains different settings for the congestion pricing system.
    '''
    __tablename__ = 'setting'

    id: Mapped[int] = mapped_column(primary_key=True)
    hourFrom: Mapped[Time] = mapped_column(Time(timezone=True))
    hourTo: Mapped[Time] = mapped_column(Time(timezone=True))
    day: Mapped[str]
    startDate: Mapped[Date] = mapped_column(Date())
    startTime: Mapped[Time] = mapped_column(Time(timezone=True))
    detectCar: Mapped[bool]
    detectMotorcycle: Mapped[bool]
    detectBus: Mapped[bool]
    detectTruck: Mapped[bool]
    carPrice: Mapped[float]
    motorcyclePrice: Mapped[float]
    busPrice: Mapped[float]
    truckPrice: Mapped[float]

    def __repr__(self) -> str:
        return f'Setting(settingId={self.id}, hourFrom={self.hourFrom}, hourTo={self.hourTo}, day={self.day}, startDate={self.startDate}, detectCar={self.detectCar}, detectMotorcycle={self.detectMotorcycle}, detectBus={self.detectBus}, detectTruck={self.detectTruck}, carPrice={self.carPrice}, motorcyclePrice={self.motorcyclePrice}, busPrice={self.busPrice}, truckPrice={self.truckPrice})'