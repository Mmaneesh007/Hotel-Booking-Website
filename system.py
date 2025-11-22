import uuid
from datetime import date, datetime
from typing import List, Optional
from sqlmodel import Session, SQLModel, create_engine, select
from models import Room, RoomType, RoomStatus, Guest, GuestType, Reservation, ReservationStatus

class HotelSystem:
    def __init__(self, db_url: Optional[str] = None):
        if db_url:
            self.engine = create_engine(db_url)
        else:
            self.engine = create_engine("sqlite:///hotel_inr.db")
        
        self._create_db_and_tables()
        self._initialize_mock_data()

    def _create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def _initialize_mock_data(self):
        with Session(self.engine) as session:
            # Check if rooms exist
            statement = select(Room)
            results = session.exec(statement).all()
            if not results:
                # Create some rooms
                # Define configurations: (Prefix, Count, Type, Price)
                configs = [
                    ("1", 8, RoomType.STANDARD, 800.0),
                    ("2", 6, RoomType.DELUXE, 1200.0),
                    ("3", 4, RoomType.SUITE, 2000.0),
                ]
                
                for prefix, count, r_type, price in configs:
                    for i in range(1, count + 1):
                        num = f"{prefix}{i:02d}" # e.g., 101, 102...
                        r_id = str(uuid.uuid4())
                        room = Room(id=r_id, number=num, type=r_type, price_per_night=price)
                        session.add(room)
                session.commit()

    def find_guest_by_name(self, name: str) -> Optional[Guest]:
        with Session(self.engine) as session:
            statement = select(Guest).where(Guest.name == name)
            return session.exec(statement).first()

    def create_guest(self, name: str, guest_type: GuestType = GuestType.WALK_IN) -> Guest:
        with Session(self.engine) as session:
            # Check if exists first to avoid dupes for demo
            existing = self.find_guest_by_name(name)
            if existing:
                return existing
                
            g_id = str(uuid.uuid4())
            guest = Guest(id=g_id, name=name, type=guest_type)
            session.add(guest)
            session.commit()
            session.refresh(guest)
            return guest

    def check_availability(self, check_in: date, check_out: date, room_type: Optional[RoomType] = None) -> List[Room]:
        with Session(self.engine) as session:
            statement = select(Room).where(Room.status == RoomStatus.AVAILABLE)
            if room_type:
                statement = statement.where(Room.type == room_type)
            
            rooms = session.exec(statement).all()
            available_rooms = []
            
            for room in rooms:
                # Check overlap with existing confirmed/checked-in reservations
                res_statement = select(Reservation).where(
                    Reservation.room_id == room.id,
                    Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.CHECKED_IN])
                )
                reservations = session.exec(res_statement).all()
                
                is_booked = False
                for res in reservations:
                    if not (check_out <= res.check_in or check_in >= res.check_out):
                        is_booked = True
                        break
                
                if not is_booked:
                    available_rooms.append(room)
            
            return available_rooms

    def create_reservation(self, guest_id: str, room_id: str, check_in: date, check_out: date) -> Reservation:
        with Session(self.engine) as session:
            room = session.get(Room, room_id)
            if not room:
                raise ValueError("Room not found")
            
            nights = (check_out - check_in).days
            if nights < 1:
                raise ValueError("Stay must be at least 1 night")

            total_price = room.price_per_night * nights
            res_id = str(uuid.uuid4())
            reservation = Reservation(
                id=res_id,
                guest_id=guest_id,
                room_id=room_id,
                check_in=check_in,
                check_out=check_out,
                total_price=total_price
            )
            session.add(reservation)
            session.commit()
            session.refresh(reservation)
            return reservation

    def get_checkouts(self, day: date) -> List[Reservation]:
        with Session(self.engine) as session:
            statement = select(Reservation).where(
                Reservation.check_out == day,
                Reservation.status == ReservationStatus.CHECKED_IN
            )
            return session.exec(statement).all()
            
    def get_all_reservations(self) -> List[Reservation]:
        with Session(self.engine) as session:
            return session.exec(select(Reservation)).all()

    def get_room_stats(self):
        with Session(self.engine) as session:
            total = session.exec(select(Room)).all()
            occupied = [r for r in total if r.status == RoomStatus.OCCUPIED] # Simplified logic
            return len(occupied), len(total)
