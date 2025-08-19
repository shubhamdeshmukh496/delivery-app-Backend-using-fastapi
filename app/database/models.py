import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, CheckConstraint,ARRAY, DateTime, func
from sqlalchemy import Enum as sa_enum
from sqlalchemy.orm import relationship
from app.database.database import Base
from enum import Enum
from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
class ShipmentStatus(str, Enum):
    PLACED = "placed"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"

class Shipment(Base):
    __tablename__ = "shipment"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    content = Column(String, nullable=False)
    weight = Column(Float,nullable=False)
    destination = Column(Integer, nullable=False)  # ForeignKey if needed
    status = Column(sa_enum(ShipmentStatus), nullable=False)
    estimated_delivery = Column(DateTime, nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("seller.id"), nullable=False)
    seller = relationship("Seller", back_populates="shipments")
    delivery_partner_id = Column(UUID(as_uuid=True), ForeignKey("delivery_partner.id"), nullable=True)
    delivery_partner = relationship("DeliveryPartner", back_populates="shipments")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
class Seller(Base):
    __tablename__ = "seller"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    shipments = relationship("Shipment", back_populates="seller")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class DeliveryPartner(Base):
    __tablename__ = "delivery_partner"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    serviceable_zip_codes = Column(ARRAY(Integer), nullable=False)
    max_handling_capacity = Column(Integer, nullable=False)
    shipments = relationship("Shipment", back_populates="delivery_partner")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    @property
    def active_shipments(self):
        return [shipment for shipment in self.shipments if shipment.status != ShipmentStatus.DELIVERED]

    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)
