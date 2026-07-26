from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Property
from app.schemas.customer import CustomerNeed


async def find_matching_properties(
        customer_need:CustomerNeed,
         db: AsyncSession,

):
        statement = select(Property)

        if customer_need.budget is not None:
            statement = statement.where(
            Property.monthly_rent <= customer_need.budget
        )

        if customer_need.district is not None:
            statement = statement.where(
            Property.district == customer_need.district
        )

        if customer_need.bedroom_count is not None:
            statement = statement.where(
            Property.bedroom_count == customer_need.bedroom_count
        )

        if customer_need.has_pet is True:
            statement = statement.where(
            Property.allows_pet.is_(True)
        )

        if customer_need.max_commute_minutes is not None:
            statement = statement.where(
              Property.commute_minutes
            <= customer_need.max_commute_minutes
        )

        statement = statement.order_by(
        Property.monthly_rent.asc(),
        Property.commute_minutes.asc(),
    )

        result = await db.execute(statement)
        return result.scalars().all()     