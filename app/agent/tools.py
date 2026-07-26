import json

from langchain_core.tools import tool

from app.database.database import AsyncSessionLocal
from app.schemas.customer import CustomerNeed
from app.services.property_service import find_matching_properties

@tool 
async def search_properties_tool(
    budget: int | None = None,
    district: str | None = None,
    bedroom_count: int | None = None,
    has_pet: bool | None = None,
    max_commute_minutes: int | None = None,
) -> str:
     """根据客户的租房条件查询数据库中的真实房源。"""
     customer_need = CustomerNeed(
        budget=budget,
        district=district,
        bedroom_count=bedroom_count,
        has_pet=has_pet,
        max_commute_minutes=max_commute_minutes,
      )

     async with AsyncSessionLocal() as db:
      properties = await find_matching_properties(
          customer_need,
          db,
     )
      data=[
          {
                 "id": property_record.id,
                "title": property_record.title,
                "district": property_record.district,
                "address": property_record.address,
                "monthly_rent": property_record.monthly_rent,
                "bedroom_count": property_record.bedroom_count,
                "commute_minutes": property_record.commute_minutes,
                "allows_pet": property_record.allows_pet,
                } 
            for property_record in properties

      ]
      return json.dumps(data,ensure_ascii=False)