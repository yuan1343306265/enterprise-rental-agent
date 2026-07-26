from sqlalchemy import select

from app.database.database import AsyncSessionLocal
from app.database.models import ConversationMessage


async def save_message(
    session_id: str,
    role: str,
    content: str,
):
    async with AsyncSessionLocal() as db:
        message_record = ConversationMessage(
            session_id=session_id,
            role=role,
            content=content,
        )

        db.add(message_record)
        await db.commit()


async def get_recent_messages(
    session_id: str,
    limit: int = 10,
):
    async with AsyncSessionLocal() as db:
        statement = (
            select(ConversationMessage)
            .where(ConversationMessage.session_id == session_id)
            .order_by(ConversationMessage.id.desc())
            .limit(limit)
        )

        result = await db.execute(statement)
        message_records = result.scalars().all()

        return list(reversed(message_records)) 
