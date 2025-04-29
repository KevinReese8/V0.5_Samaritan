import re
import json

# 输入文件路径

input_path = ""
output_path = ""

# 设置两位角色名称（需根据实际对话修改）
role_you = ""
role_target = ""

# 用于存储句对数据
pairs = []

# 正则提取消息块
time_line_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.+?)\n")

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 当前说话人和内容缓存
current_speaker = None
current_text = ""
parsed_dialogues = []

for line in lines:
    match = time_line_pattern.match(line)
    if match:
        # 新的一行开始，保存上一条对话
        if current_speaker and current_text.strip():
            parsed_dialogues.append({"role": current_speaker, "text": current_text.strip()})

        current_speaker = match.group(2).strip()
        current_text = line[match.end():].strip()
    else:
        # 多行消息拼接
        current_text += " " + line.strip()

# 加入最后一条
if current_speaker and current_text.strip():
    parsed_dialogues.append({"role": current_speaker, "text": current_text.strip()})

# 提取“你说 -> 她回”的句对
for i in range(len(parsed_dialogues) - 1):
    a, b = parsed_dialogues[i], parsed_dialogues[i + 1]
    if a['role'] == role_you and b['role'] == role_target:
        pairs.append({"prompt": a['text'], "response": b['text']})

# 写入 JSONL 文件
with open(output_path, "w", encoding="utf-8") as out:
    for pair in pairs:
        out.write(json.dumps(pair, ensure_ascii=False) + "\n")

print(f"成功提取 {len(pairs)} 对话，保存为 {output_path}")
