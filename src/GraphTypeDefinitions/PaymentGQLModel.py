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

StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]
PaymentInfoGQLModel = typing.Annotated["PaymentInfoGQLModel", strawberry.lazy(".PaymentInfoGQLModel")]


@strawberry.federation.type(
    keys=["id"], description="""Represents a unique payment for admission"""
)
class PaymentGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).PaymentModel

    payment_info_id: uuid.UUID = strawberry.field(
        description="The payment info id",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    bank_unique_data: typing.Optional[str] = strawberry.field(
        default=None,
        description="The bank unique data",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    variable_symbol: typing.Optional[str] = strawberry.field(
        default=None,
        description="Variable symbol of transaction",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    amount: typing.Optional[float] = strawberry.field(
        default=None,
        description="Paid amount of the transaction",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    payment_info: typing.Optional["PaymentInfoGQLModel"] = strawberry.field(
        description="""PaymentInfo associated with payment""",
        resolver=ScalarResolver['PaymentInfoGQLModel'](fkey_field_name="payment_info_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

    student_admissions: typing.List["StudentAdmissionGQLModel"] = strawberry.field(
        description="""Student Admissions related to this payment""",
        resolver=VectorResolver["StudentAdmissionGQLModel"](fkey_field_name="payment_id", whereType=None),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )


@createInputs
@dataclasses.dataclass
class PaymentInputFilter:
    id: uuid.UUID
    payment_info_id: uuid.UUID
    bank_unique_data: str
    variable_symbol: str
    amount: float

payment_by_id = strawberry.field(
    description = """Finds a Payment by its id""",
    graphql_type=typing.Optional[PaymentGQLModel],
    resolver=PaymentGQLModel.load_with_loader,
    permission_classes=[
        OnlyForAuthentized,
    ]
)

payment_page = strawberry.field(
    description="""Returns a list of Payments""",
    resolver=PageResolver[PaymentGQLModel](whereType=PaymentInputFilter),
    permission_classes=[
        OnlyForAuthentized,
    ],
)


########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="Definition of a Payment used for creation")
class PaymentInsertGQLModel:
    payment_info_id: uuid.UUID = strawberry.field(description="Payment id")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    bank_unique_data: typing.Optional[str] = strawberry.field(description="Unique bank identifier or something", default=None)
    variable_symbol: typing.Optional[str] = strawberry.field(description="Variable symbol of transaction", default=None)
    amount: typing.Optional[float] = strawberry.field(description="Paid amount of the transaction", default=None)

    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Definition of a Payment used for update")
class PaymentUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

    bank_unique_data: typing.Optional[str] = strawberry.field(description="Unique bank identifier or something", default=None)
    variable_symbol: typing.Optional[str] = strawberry.field(description="Variable symbol of transaction", default=None)
    amount: typing.Optional[float] = strawberry.field(description="Paid amount of the transaction", default=None)
    payment_info_id: typing.Optional[uuid.UUID] = strawberry.field(description="Payment info id", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Definition of a Payment used for delete")
class PaymentDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

########################################################################################################################

@strawberry.mutation(
    description="Adds a new Payment",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[PaymentGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def payment_insert(self, info: strawberry.types.Info, payment: PaymentInsertGQLModel) -> typing.Union[PaymentGQLModel, InsertError[PaymentGQLModel]]:
    payment.rbacobject_id = payment.rbacobject_id # if admission.rbacobject_id else admission.group_id
    return await Insert[PaymentGQLModel].DoItSafeWay(info=info, entity=payment)



@strawberry.mutation(
    description="Updates a Payment",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[PaymentGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def payment_update(self, info: strawberry.types.Info, payment: typing.Annotated[PaymentUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[PaymentGQLModel, UpdateError[PaymentGQLModel]]:
    return await Update[PaymentGQLModel].DoItSafeWay(info=info, entity=payment)



@strawberry.mutation(
    description="Deletes a Payment",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[PaymentGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def payment_delete(self, info: strawberry.types.Info, payment: PaymentDeleteGQLModel) -> typing.Optional[DeleteError[PaymentGQLModel]]:
    return await Delete[PaymentGQLModel].DoItSafeWay(info=info, entity=payment)