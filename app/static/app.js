const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messageList = document.getElementById("messageList");
const statusText = document.getElementById("statusText");
const sessionIdElement = document.getElementById("sessionId");
const newSessionButton = document.getElementById(
    "newSessionButton"
);


const sessionStorageKey = "rental-agent-session-id";

let sessionId = localStorage.getItem(sessionStorageKey);

if (!sessionId) {
    sessionId = `web-${Date.now()}`;
    localStorage.setItem(sessionStorageKey, sessionId);
}

sessionIdElement.textContent = sessionId;

function addMessage(role, content) {
    const messageElement = document.createElement("article");
    const roleElement = document.createElement("div");
    const contentElement = document.createElement("div");

    const isUser = role === "user";

    messageElement.className = isUser
        ? "message user-message"
        : "message assistant-message";

    roleElement.className = "message-role";
    roleElement.textContent = isUser ? "你" : "租房顾问";

    contentElement.className = "message-content";
    contentElement.textContent = content;

    messageElement.append(roleElement, contentElement);
    messageList.appendChild(messageElement);

    messageList.scrollTop = messageList.scrollHeight;
}

function setLoading(isLoading) {
    messageInput.disabled = isLoading;
    sendButton.disabled = isLoading;
    sendButton.textContent = isLoading
        ? "正在查询..."
        : "发送咨询";
}

async function loadHistory() {
    try {
        const response = await fetch(
            `/api/sessions/${encodeURIComponent(sessionId)}`
        );

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        if (data.messages.length === 0) {
            return;
        }

        messageList.innerHTML = "";

        for (const message of data.messages) {
            addMessage(message.role, message.content);
        }

        statusText.textContent = "已恢复之前的聊天记录";
    } catch (error) {
        statusText.textContent = "暂时无法读取历史记录";
    }
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        statusText.textContent = "请先输入租房需求";
        return;
    }

    addMessage("user", message);
    messageInput.value = "";

    setLoading(true);
    statusText.textContent = "Agent 正在分析需求并查询房源...";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "请求处理失败"
            );
        }

        addMessage("assistant", data.reply);
        statusText.textContent = "咨询完成";
    } catch (error) {
        addMessage(
            "assistant",
            `抱歉，本次请求失败：${error.message}`
        );

        statusText.textContent = "请求失败，请稍后重试";
    } finally {
        setLoading(false);
        messageInput.focus();
    }
});

messageInput.addEventListener("keydown", (event) => {
    if (event.ctrlKey && event.key === "Enter") {
        chatForm.requestSubmit();
    }
});

loadHistory();

newSessionButton.addEventListener("click", () => {
    const shouldCreateNewSession = window.confirm(
        "确定要开始一个新的租房咨询吗？"
    );

    if (!shouldCreateNewSession) {
        return;
    }

    localStorage.removeItem(sessionStorageKey);
    window.location.reload();
});