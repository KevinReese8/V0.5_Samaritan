import json
import os
from openai import OpenAI

# 源聊天记录文件
SOURCE_FILE = "cleaned_chat_2.jsonl"
# 目标长期记忆文件
TARGET_FILE = "long_term_memory_V0.5.jsonl"

def import_full_history(source=SOURCE_FILE, target=TARGET_FILE, overwrite=False):
    # 读取源聊天记录
    with open(source, "r", encoding="utf-8") as f:
        chat_data = [json.loads(line) for line in f.readlines()]

    # 构造长期记忆条目
    memories = []
    for entry in chat_data:
        # 可根据需要自定义content格式
        content = f"我：{entry['prompt']}\n她：{entry['response']}"
        memories.append({"content": content})

    # 追加或覆盖写入
    if overwrite or not os.path.exists(target):
        mode = "w"
    else:
        # 追加模式先加载已有内容
        with open(target, "r", encoding="utf-8") as f:
            existing = [json.loads(line) for line in f.readlines()]
        memories = existing + memories
        mode = "w"

    with open(target, mode, encoding="utf-8") as f:
        for mem in memories:
            f.write(json.dumps(mem, ensure_ascii=False) + "\n")

    print(f"已导入 {len(memories)} 条对话到 {target}")

def summarize_history(source=SOURCE_FILE, target=TARGET_FILE):
    # 读取全部聊天记录
    with open(source, "r", encoding="utf-8") as f:
        chat_data = [json.loads(line) for line in f.readlines()]
    # 拼接为大段文本
    chat_text = "\n".join([f"我：{entry['prompt']}\n她：{entry['response']}" for entry in chat_data])
    # 构造摘要任务prompt
    prompt = (
        "请根据以下聊天记录，提炼出这个她这个人物的高质量长期记忆摘要，包括但不限于：人物性格、说话风格、重要事件、核心关系、典型表达等。"
        "请用简洁、条理清晰的方式总结，适合后续作为长期记忆注入到AI对话系统中。\n"
        "注意：请忽略”我“的内容，只保留”她“的内容。 \n"
        "聊天记录如下：\n"
        f"{chat_text}\n"
        "请直接输出高质量摘要，不要输出多余解释。"
    )
    # 调用大模型
    client = OpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key="" #!!!请替换为你的API密钥!!!
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    summary = response.choices[0].message.content.strip()
    # 写入长期记忆文件，只保存一条高质量摘要
    with open(target, "w", encoding="utf-8") as f:
        f.write(json.dumps({"content": summary}, ensure_ascii=False) + "\n")
    print(f"已生成高质量长期记忆摘要并写入 {target}")

if __name__ == "__main__":
    # 默认追加模式，如需覆盖请传入overwrite=True
    import_full_history(overwrite=False)
    summarize_history()