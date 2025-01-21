from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .BaseModel import BaseModel
import uuid

class PaymentModel(BaseModel):
    """
    Represents a unique payment for admission.
    """
    __tablename__ = "payments"

    payment_info_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("payment_infos.id"), default=None, nullable=True, index=True, comment="Foreign key referencing the related payment info")

    bank_unique_data: Mapped[str] = mapped_column(String, default=None, nullable=True, comment="Unique bank identifier or something")
    variable_symbol: Mapped[str] = mapped_column(String, default=None, nullable=True, comment="Variable symbol of transaction")
    amount: Mapped[float] = mapped_column(Float, default=None, nullable=True, comment="Paid amount of the transaction")

    payment_info = relationship("PaymentInfoModel", viewonly=True, lazy="joined")