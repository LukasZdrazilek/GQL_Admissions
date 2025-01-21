from sqlalchemy import String, Float
from sqlalchemy.orm import mapped_column, Mapped
from .BaseModel import BaseModel

class PaymentInfoModel(BaseModel):
    """
    Represents a general payment information related to admission.
    """
    __tablename__ = "payment_infos"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the payment information")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="English name of the payment information")
    account_number: Mapped[str] = mapped_column(String, default=None, nullable=True, comment="Bank account number")
    specific_symbol: Mapped[str] = mapped_column(String, default=None, nullable=True, comment="Specific symbol for transaction")
    constant_symbol: Mapped[str] = mapped_column(String, default=None, nullable=True, comment="Constat symbol for transaction")
    IBAN: Mapped[str] = mapped_column(String, default=None, nullable=True, comment="International Bank Account Number")
    SWIFT: Mapped[str] = mapped_column(String, default=None, nullable=True, comment="Swift account number")

    amount: Mapped[float] = mapped_column(Float, default=None, nullable=True, comment="Amount to pay")