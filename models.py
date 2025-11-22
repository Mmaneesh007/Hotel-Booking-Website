from enum import Enum
from datetime import date, datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class RoomType(str, Enum):
    STANDARD = "Standard"
    DELUXE = "Deluxe"
    SUITE = "Suite"

class RoomStatus(str, Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    DIRTY = "Dirty"
    MAINTENANCE = "Maintenance"

class GuestType(str, Enum):
    WALK_IN = "Walk-in"
    CORPORATE = "Corporate"
    VIP = "VIP"
    LOYALTY = "Loyalty"

class Guest(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    type: GuestType = GuestType.WALK_IN
    loyalty_points: int = 0
    
    reservations: List["Reservation"] = Relationship(back_populates="guest")

class Room(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    number: str
    type: RoomType
    price_per_night: float
    status: RoomStatus = RoomStatus.AVAILABLE
    features: str = "" # Comma separated string for simplicity in SQLite

    reservations: List["Reservation"] = Relationship(back_populates="room")

class ReservationStatus(str, Enum):
    CONFIRMED = "Confirmed"
    CHECKED_IN = "Checked In"
    CHECKED_OUT = "Checked Out"
    CANCELLED = "Cancelled"

class Reservation(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    guest_id: str = Field(foreign_key="guest.id")
    room_id: str = Field(foreign_key="room.id")
    check_in: date
    check_out: date
    total_price: float
    status: ReservationStatus = ReservationStatus.CONFIRMED
    created_at: datetime = Field(default_factory=datetime.now)

    guest: Optional[Guest] = Relationship(back_populates="reservations")
    room: Optional[Room] = Relationship(back_populates="reservations")
