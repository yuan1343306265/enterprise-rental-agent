from contextlib import asynccontextmanager
from app.services.property_service import find_matching_properties

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db, init_db
from app.database.models import Property
from app.schemas.property import PropertyCreate, PropertyUpdate
from app.schemas.customer import CustomerNeed

from app.agent.rental_agent import ask_rental_agent
from app.schemas.chat import ChatRequest, ChatResponse

from app.schemas.session import SessionHistoryResponse
from app.services.conversation_service import get_recent_messages

from fastapi import HTTPException

from app.logging_config import logger

import asyncio

from pathlib import Path

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="企业级租房顾问 ",
    lifespan=lifespan,
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

@app.get("/", include_in_schema=False)
async def get_home_page():
    return FileResponse(STATIC_DIR / "index.html")
agent_semaphore = asyncio.Semaphore(5)


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "租房顾问 服务运行正常",
    }


@app.get("/api/properties")
async def get_properties(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Property))
    properties = result.scalars().all()

    return {
        "success": True,
        "message": "房源列表查询成功",
        "data": properties,
    }


@app.get("/api/properties/{property_id}")
async def get_property_detail(
    property_id: int,
    db: AsyncSession = Depends(get_db),
):
    property_record = await db.get(Property, property_id)

    if property_record is None:
        return {
            "success": False,
            "message": "房源不存在",
            "data": None,
        }

    return {
        "success": True,
        "message": "房源详情查询成功",
        "data": property_record,
    }


@app.post("/api/properties/search")
async def search_properties(
    customer_need: CustomerNeed,
    db: AsyncSession = Depends(get_db),
):
    properties = await find_matching_properties(
    customer_need,
    db,
    )
    return {
        "success": True,
        "message": "符合条件的房源查询成功",
        "data": properties,
    }


@app.patch("/api/properties/{property_id}")
async def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
):
    property_record = await db.get(Property, property_id)

    if property_record is None:
        return {
            "success": False,
            "message": "房源不存在",
            "data": None,
        }

    update_data = property_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(property_record, field, value)

    await db.commit()
    await db.refresh(property_record)

    return {
        "success": True,
        "message": "房源修改成功",
        "data": property_record,
    }
@app.post("/api/properties/search")
async def search_properties(
    customer_need: CustomerNeed,
    db: AsyncSession = Depends(get_db),
):  
    statement  = select(Property)
    if customer_need.budget is not None:
        statement = statement.where(
            property.monthly_rent <= customer_need.budget
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
    result = await db.cexcute(statement)
    properties = result.scalars().all()


    return{
        "success": True,
        "message": "符合条件的房源查询成功",
        "data": properties,
    }
@app.delete("/api/properties/{property_id}")
async def delete_property(
    property_id: int,
    db: AsyncSession = Depends(get_db),
):
    property_record = await db.get(Property, property_id)

    if property_record is None:
        return {
            "success": False,
            "message": "房源不存在",
            "data": None,
        }

    await db.delete(property_record)
    await db.commit()

    return {
        "success": True,
        "message": "房源删除成功",
        "data": {
            "id": property_id,
        },
    }
@app.post("/api/chat",response_model=ChatResponse)
async def chat_with_agent(request:ChatRequest):
    try:
        async with agent_semaphore:
          reply = await asyncio.wait_for(
        ask_rental_agent(
        message=request.message,
        session_id=request.session_id,
        ),

        timeout=30,
        )

    except TimeoutError as error:
        logger.warning(
            "租房咨询处理超时,session_id=%s",
            request.session_id,
        )

        raise HTTPException(
            status_code=504,
            detail="租房顾问响应超时，请稍后重试。",
        ) from error
    
    except Exception as error:
        logger.exception(
            "租房咨询处理失败,session_id=%s",
            request.session_id,
        )

        raise HTTPException(
            status_code=500,
            detail="暂时无法处理请求，请稍后重试",
        ) from error

    return ChatResponse(
        success=True,
        reply=reply,
        session_id=request.session_id
    )

@app.get(
    "/api/sessions/{session_id}",
    response_model=SessionHistoryResponse,

)
async def get_session_history(
    session_id:str,
):
    messages=await get_recent_messages(
        session_id=session_id,
        limit=100,
    )

    return SessionHistoryResponse(
        session_id=session_id,
        messages=messages,
    )