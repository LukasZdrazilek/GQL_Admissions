import asyncio
import dataclasses
import datetime
import typing
import strawberry
import uuid

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission,
    SimpleUpdatePermission,
    SimpleDeletePermission
)
from uoishelpers.resolvers import (
    getLoadersFromInfo,
    createInputs,

    InsertError,
    Insert,
    UpdateError,
    Update,
    DeleteError,
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver,
)


from .BaseGQLModel import BaseGQLModel

AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]


@strawberry.federation.type(
    keys=["id"], description="""Represents a general payment info for admission"""
)
class PaymentInfoGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).PaymentInfoModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="Name of the payment info",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="English name of the payment info",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    account_number: typing.Optional[str] = strawberry.field(
        default=None,
        description="Bank account number",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    specific_symbol: typing.Optional[str] = strawberry.field(
        default=None,
        description="Specific symbol for transaction",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    constant_symbol: typing.Optional[str] = strawberry.field(
        default=None,
        description="Constant symbol for transaction",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    IBAN: typing.Optional[str] = strawberry.field(
        default=None,
        description="International bank account number",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    SWIFT: typing.Optional[str] = strawberry.field(
        default=None,
        description="Swift account number",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    amount: typing.Optional[float] = strawberry.field(
        default=None,
        description="Amount to pay",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    admissions: typing.List["AdmissionGQLModel"] = strawberry.field(
        description="""Admissions related to this payment info""",
        resolver=VectorResolver["AdmissionGQLModel"](fkey_field_name="payment_info_id", whereType=None),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )


@createInputs
@dataclasses.dataclass
class PaymentInfoInputFilter:
    id: uuid.UUID
    name: str
    name_en: str
    account_number: str
    specific_symbol: str
    constant_symbol: str
    IBAN: str
    SWIFT: str
    amount: float

payment_info_by_id = strawberry.field(
    description = """Finds a Payment Info by its id""",
    graphql_type=typing.Optional[PaymentInfoGQLModel],
    resolver=PaymentInfoGQLModel.load_with_loader,
    permission_classes=[
        OnlyForAuthentized,
    ]
)

payment_info_page = strawberry.field(
    description="""Returns a list of Payment Infos""",
    resolver=PageResolver[PaymentInfoGQLModel](whereType=PaymentInfoInputFilter),
    permission_classes=[
        OnlyForAuthentized,
    ],
)


########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="Definition of a Payment Info used for creation")
class PaymentInfoInsertGQLModel:
    name: str = strawberry.field(description="Name of the Payment Info")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the Payment Info", default=None)
    account_number: typing.Optional[str] = strawberry.field(description="Bank account number", default=None)
    specific_symbol: typing.Optional[str] = strawberry.field(description="Specific symbol for transaction", default=None)
    constant_symbol: typing.Optional[str] = strawberry.field(description="Constant symbol for transaction", default=None)
    IBAN: typing.Optional[str] = strawberry.field(description="International bank account number", default=None)
    SWIFT: typing.Optional[str] = strawberry.field(description="Swift account number", default=None)
    amount: typing.Optional[float] = strawberry.field(description="Amount to pay")

    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Definition of a Payment Info used for update")
class PaymentInfoUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

    name: typing.Optional[str] = strawberry.field(description="Name of the Payment Info", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the Payment Info", default=None)
    amount: typing.Optional[float] = strawberry.field(description="Amount to pay")
    account_number: typing.Optional[str] = strawberry.field(description="Bank account number", default=None)
    specific_symbol: typing.Optional[str] = strawberry.field(description="Specific symbol for transaction", default=None)
    constant_symbol: typing.Optional[str] = strawberry.field(description="Constant symbol for transaction", default=None)
    IBAN: typing.Optional[str] = strawberry.field(description="International bank account number", default=None)
    SWIFT: typing.Optional[str] = strawberry.field(description="Swift account number", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Definition of a Payment Info used for delete")
class PaymentInfoDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

########################################################################################################################

@strawberry.mutation(
    description="Adds a new Payment Info",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[PaymentInfoGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def payment_info_insert(self, info: strawberry.types.Info, payment_info: PaymentInfoInsertGQLModel) -> typing.Union[PaymentInfoGQLModel, InsertError[PaymentInfoGQLModel]]:
    payment_info.rbacobject_id = payment_info.rbacobject_id # if admission.rbacobject_id else admission.group_id
    return await Insert[PaymentInfoGQLModel].DoItSafeWay(info=info, entity=payment_info)



@strawberry.mutation(
    description="Updates a Payment Info",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[PaymentInfoGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def payment_info_update(self, info: strawberry.types.Info, payment_info: typing.Annotated[PaymentInfoUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[PaymentInfoGQLModel, UpdateError[PaymentInfoGQLModel]]:
    return await Update[PaymentInfoGQLModel].DoItSafeWay(info=info, entity=payment_info)



@strawberry.mutation(
    description="Deletes a Payment Info",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[PaymentInfoGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def payment_info_delete(self, info: strawberry.types.Info, payment_info: PaymentInfoDeleteGQLModel) -> typing.Optional[DeleteError[PaymentInfoGQLModel]]:
    return await Delete[PaymentInfoGQLModel].DoItSafeWay(info=info, entity=payment_info)