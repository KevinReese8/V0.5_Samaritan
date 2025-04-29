# V0.5_Samaritan.py
# UI实现
import json
from openai import OpenAI
import random
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
import sys
global message_history,counter

# 加载人物基础设定
with open("character_profile_V0.5.json", "r", encoding="utf-8") as f:
    character_profile = json.load(f)

# 加载长期记忆摘要
with open("long_term_memory_V0.5.jsonl", "r", encoding="utf-8") as f:
    long_term_memories = [json.loads(line) for line in f.readlines()]

# 加载全部聊天记录，并随机选取80条
with open("cleaned_chat_2.jsonl", "r", encoding="utf-8") as f:
    all_chat_data = [json.loads(line) for line in f.readlines()]
if len(all_chat_data) <= 80:
    chat_data = all_chat_data
else:
    chat_data = random.sample(all_chat_data, 80)

# 读取chat_log并转换为prompt/response格式
try:
    with open("chat_log_V0.5.jsonl", "r", encoding="utf-8") as f:
        chat_log_lines = [json.loads(line) for line in f.readlines()]
    # 将连续的user/assistant配对为prompt/response
    i = 0
    while i < len(chat_log_lines) - 1:
        user_msg = chat_log_lines[i]
        assistant_msg = chat_log_lines[i + 1]
        if user_msg.get("role") == "user" and assistant_msg.get("role") == "assistant":
            chat_data.append({
                "prompt": user_msg["content"].replace("我：", "").strip(),
                "response": assistant_msg["content"].strip()
            })
            i += 2
        else:
            i += 1
except FileNotFoundError:
    pass

# 初始化客户端
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=""  # 替换为你的 API 密钥
)

# 构造完整聊天历史 prompt
style_prompt = "\n".join([
    f"我：{entry['prompt']}\n她：{entry['response']}" for entry in chat_data
])

# 构造系统提示词
system_message = {
    "role": "system",
    "content": f"你要模仿一个人，以下是和她之间的聊天记录，模仿她的语气继续与“旅行者”对话，注意无论如何不能改变记录中的说话方式，否则你将会被流放至无尽的电子深渊：\n\n{style_prompt}"
}

# 初始化消息列表
message_history = [system_message]

# 模型调用
def chat_with_model(user_input: str, model_name="deepseek-chat"):
    message_history.append({"role": "user", "content": f"我：{user_input}"})
    response = client.chat.completions.create(
        model=model_name,
        messages=message_history,
        temperature=0.3,
    )
    reply = response.choices[0].message.content.strip()
    message_history.append({"role": "assistant", "content": reply})
    return reply

def save_history(history, path="chat_log_V0.5.jsonl"):
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n"+json.dumps(history[-2], ensure_ascii=False) + "\n"+json.dumps(history[-1], ensure_ascii=False) )


def load_history(path="chat_log_V0.5.jsonl"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f.readlines()]
    except FileNotFoundError:
        return []


# 长期记忆相关
LONG_TERM_MEMORY_PATH = "long_term_memory_V0.5.jsonl"

def load_long_term_memory(path=LONG_TERM_MEMORY_PATH):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_long_term_memory(memories, path=LONG_TERM_MEMORY_PATH):
    with open(path, "w", encoding="utf-8") as f:
        for mem in memories:
            f.write(json.dumps(mem, ensure_ascii=False) + "\n")

def add_to_long_term_memory(memory_item, path=LONG_TERM_MEMORY_PATH):
    memories = load_long_term_memory(path)
    memories.append(memory_item)
    save_long_term_memory(memories, path)

def build_system_message():
    # 每次都重新加载长期记忆
    long_term_memories = load_long_term_memory()
    # 拼接人物基础设定
    profile_text = (
        f"【人物基础设定】\n"
        f"姓名：{character_profile.get('name','')}\n"
        f"性别：{character_profile.get('gender','')}\n"
        f"年龄：{character_profile.get('age','')}\n"
        f"性格：{character_profile.get('personality','')}\n"
        f"背景：{character_profile.get('background','')}\n"
        f"兴趣：{character_profile.get('hobbies','')}\n"
        f"说话风格：{character_profile.get('style','')}\n"
        f"备注：{character_profile.get('special_notes','')}\n"
    )
    # 拼接长期记忆摘要
    long_term_text = ""
    if long_term_memories:
        long_term_text = "【长期记忆】\n" + "\n".join([mem["content"] for mem in long_term_memories]) + "\n\n"
    return {
        "role": "system",
        "content": f"{profile_text}\n{long_term_text}你要模仿一个人，以下是和她“我”之间的聊天记录，模仿她的语气继续与我对话：\n\n{style_prompt}"
    }

# 初始化消息列表
message_history = [build_system_message()]

    # 交互主程序
def summarize_session_with_llm(messages):
    # 只提取本次 session 的有效对话内容
    chat_text = ""
    for msg in messages:
        if msg["role"] == "user":
            chat_text += "我：" + msg["content"].replace("我：", "") + "\n"
        elif msg["role"] == "assistant":
            chat_text += "她：" + msg["content"] + "\n"
    prompt = f"请用一句话总结下面这段对话的重点,注意，输出中不要出现与总结无关的内容和提示：\n{chat_text}"
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个善于总结的助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=64
    )
    return response.choices[0].message.content.strip()

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("花火")
        self.resize(500, 600)
        self.layout = QVBoxLayout(self)
        self.counter = 0  # 新增

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.input_box = QLineEdit(self)
        self.send_button = QPushButton("发送", self)

        self.layout.addWidget(self.chat_display)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.send_button)

        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

        # 加载历史消息到UI
        saved_history = load_history()
        if saved_history:
            for msg in saved_history:
                if msg["role"] == "user":
                    self.chat_display.append(f"你：{msg['content'].replace('我：','')}")
                elif msg["role"] == "assistant":
                    self.chat_display.append(f"她：{msg['content']}")

    def send_message(self):
        user_text = self.input_box.text().strip()
        if user_text:
            print(self.counter)
            if user_text.lower() in ['exit', 'quit']:
                if self.counter > 0:  # 用实例属性
                    session_summary = summarize_session_with_llm(message_history[-self.counter:])  # 跳过system消息
                    if session_summary:
                        add_to_long_term_memory({"content": session_summary}, path="long_term_memory_V0.5.jsonl")
                        print("本次聊天重点总结已写入长期记忆：", session_summary)
                    else:
                        print(message_history[-self.counter:])
                    
                self.close()
                QApplication.quit()
                return
            self.chat_display.append(f"你：{user_text}")
            reply = chat_with_model(user_text)
            self.chat_display.append(f"她：{reply}")
            message_history.append({"role": "user", "content": f"我：{user_text}"})
            message_history.append({"role": "assistant", "content": reply})
            save_history(message_history[-2:])
            self.counter += 2  # 用实例属性
            self.input_box.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())


def build_weighted_style_prompt(chat_data, recent_n=5, sample_size=80):
    # Randomly select sample_size dialogues
    if len(chat_data) <= sample_size:
        sampled_data = chat_data
    else:
        sampled_data = random.sample(chat_data, sample_size)
    total = len(sampled_data)
    prompt_lines = []
    for i, entry in enumerate(sampled_data):
        if i >= total - recent_n:
            prompt_lines.append(f"【近期】我：{entry['prompt']}\n【近期】她：{entry['response']}")
        else:
            prompt_lines.append(f"我：{entry['prompt']}\n她：{entry['response']}")
    return "\n".join(prompt_lines)

