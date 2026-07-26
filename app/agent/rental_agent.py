from app.logging_config import logger
from langchain_core.messages import(
      AIMessage,
      HumanMessage, 
      SystemMessage,
      ToolMessage,
)


from app.agent.model import llm
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import search_properties_tool
from app.services.conversation_service import(
    get_recent_messages,
    save_message,

)


llm_with_tools = llm.bind_tools(
    [search_properties_tool]
).with_retry(
    stop_after_attempt=3,
)
MAX_TOOL_CALLS = 3

async def ask_rental_agent(
        message: str,
        session_id:str = "default",
          ) -> str:
    logger.info(
        "开始处理咨询,session_id=%s",
        session_id,
    )
    message_records = await get_recent_messages(session_id)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]



    for message_record in message_records:
        if message_record.role =="user":
            messages.append(
                HumanMessage(content=message_record.content)
            )
        elif message_record.role == "assistant":
           messages.append(
           AIMessage(content=message_record.content)
    )
    messages.append(HumanMessage(content=message))

    await save_message(
        session_id=session_id,
        role="user",
        content=message,

    )
    response = await llm_with_tools.ainvoke(messages)
    if not response.tool_calls:
        answer = response.content

        await save_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        logger.info(
            "租房咨询处理完成,session_id=%s",
            session_id,
        )

        return answer


    if len(response.tool_calls) > MAX_TOOL_CALLS:
        logger.warning(
            "工具调用次数过多，session_id=%s,tool_calls=%s",
            session_id,
            len(response.tool_calls),
        )

        answer="本次请求需要执行的工具过多，请缩小查询范围"

        await save_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return answer

    
    messages.append(response)

    for tool_call in response.tool_calls:
        logger.info(
            "房源查询工具,session_id=%s", 
            session_id,
        )
        tool_result = await search_properties_tool.ainvoke(
            tool_call["args"]
        )

        messages.append(
            ToolMessage(
                content=tool_result,
                tool_call_id=tool_call["id"],
            )
        )

    final_response = await llm_with_tools.ainvoke(messages)
    answer = final_response.content

    await save_message(
        session_id=session_id,
        role="assistant",
        content=answer,
    )

    logger.info(
                "咨询处理完成,session_id=%s",
                session_id,
            )
    return answer