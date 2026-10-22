import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
API_KEY = os.getenv("GEMINI_API_KEY", "")

def rule_answer(message):
    text = message.strip().lower()

    if any(word in text for word in ["你好", "嗨", "哈囉", "hello", "hi"]):
        return "你好！我是 AI 校園導師小幫手。你可以問我課業、學習方法或校園生活問題。"
    if any(word in text for word in ["python", "程式", "程式碼", "寫程式"]):
        return "學程式可以先把問題拆成小步驟，再練習變數、條件判斷、迴圈與函式。你也可以把錯誤訊息貼給我，我們一起找原因。"
    if any(word in text for word in ["作業", "考試", "讀書", "課業", "報告"]):
        return "可以先確認作業要求，再把任務拆成幾個小部分，安排完成時間。你可以告訴我科目和卡住的地方，我會陪你一步一步整理。"
    if any(word in text for word in ["壓力", "難過", "焦慮", "累", "煩"]):
        return "聽起來你最近不太輕鬆。可以先休息一下，試著把最困擾你的事情說清楚。如果情緒一直影響生活，也可以找信任的人或學校輔導資源聊聊。"
    return None

def fallback_answer(message):
    return (
        "目前我只提供職業資訊的查詢方向。你可以先把問題拆成幾個小部分，"
        "再查詢學校公告、課程大綱或可信的官方資料。如果你願意，也可以補充更多背景，讓我更了解你的問題。"
    )

def ai_answer(message):
    if not API_KEY:
        return None, "尚未設定 GEMINI_API_KEY"
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model=MODEL,
            contents=(
                "你是親切、清楚的繁體中文 AI 校園導師小幫手。"
                "請用適合大學生初學者的方式回答課業、學習與校園生活問題。"
                "不確定的資訊要坦白說明，不要捏造學校規定。"
                "若涉及危機或重大身心困擾，鼓勵尋求可信任的人或專業協助。\\n"
                f"使用者問題：{message}"
            ),
        )
        return (response.text or "").strip(), None
    except Exception as exc:
        return None, str(exc)

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "campus-mentor"})

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    mode = str(data.get("mode", "auto")).strip().lower()

    if not message:
        return jsonify({"answer": "請先輸入問題。", "source": "rule"}), 400

    if mode == "rule":
        return jsonify({"answer": rule_answer(message) or fallback_answer(message), "source": "rule"})
    if mode == "fallback":
        return jsonify({"answer": fallback_answer(message), "source": "fallback"})
    if mode == "ai":
        answer, error = ai_answer(message)
        if answer:
            return jsonify({"answer": answer, "source": "ai"})
        return jsonify({"answer": fallback_answer(message), "source": "fallback", "note": "AI 暫時無法使用，已切換備援回答。"})

    answer = rule_answer(message)
    if answer:
        return jsonify({"answer": answer, "source": "rule"})
    answer, error = ai_answer(message)
    if answer:
        return jsonify({"answer": answer, "source": "ai"})
    return jsonify({"answer": fallback_answer(message), "source": "fallback", "note": "AI 暫時無法使用，已切換備援回答。"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
