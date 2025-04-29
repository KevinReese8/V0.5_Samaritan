# 🌟 V0.5_Samaritan  

> **Let the one in our memories speak again — 让沉睡于回忆中的声音，再次响起**  

[![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![UI](https://img.shields.io/badge/UI-PySide6-lightgrey?logo=qt)](UI)
[![Chat Model](https://img.shields.io/badge/model-DeepSeek--Chat-red)](https://deepseek.com/)

---

## 🧭 Table of Contents | 目录  
- [📚 项目简介 | Overview](#-项目简介--overview)
- [✨ 核心功能 | Key Features](#-核心功能--key-features)
- [🚀 使用方法 | How to Use](#-使用方法--how-to-use)
- [📂 文件说明 | File Description](#-文件说明--file-description)
- [🌈 项目亮点 | Highlights](#-项目亮点--highlights)
- [🔮 未来展望 | Future Plans](#-未来展望--future-plans)


## 📚 项目简介 | Overview  

V0.5_Samaritan 是一个基于深度学习大模型（如 DeepSeek-Chat）与本地 UI 的智能陪伴对话系统。  
V0.5_Samaritan is an intelligent companion dialogue system based on deep learning large models (e.g., DeepSeek-Chat) combined with a local UI.

它能够模拟虚拟人物，进行自然、个性化的中英文对话，具备长期记忆、风格模仿、会话总结等能力。  
It simulates virtual characters engaging in natural and personalized conversations in Chinese or English, featuring long-term memory, style imitation, session summarization, and more.

适用于虚拟陪伴、角色扮演、心理疏导等场景。  
It is ideal for scenarios such as virtual companionship, role-playing, and psychological counseling.

---

## ✨ 核心功能 | Key Features  

- **🎭 虚拟人物设定 | Virtual Character Profile**  
  - 通过 `character_profile_V0.5.json` 文件定义姓名、性格、背景、兴趣等，系统自动加载并体现人物特色。
  - Define character settings (name, personality, background, hobbies, etc.) via `character_profile_V0.5.json`. The system automatically incorporates character traits into conversations.

- **🧠 长期记忆管理 | Long-term Memory Management**  
  - 会话重点摘要自动记录到 `long_term_memory_V0.5.jsonl`，实现持续性记忆。
  - Conversation highlights are automatically saved to `long_term_memory_V0.5.jsonl`, enabling memory retention across sessions.

- **🎨 对话风格模仿 | Dialogue Style Imitation**  
  - 分析历史聊天记录，生成风格提示，保证回复贴合人物语气、用词和表达习惯。
  - Analyzes historical conversations to build style prompts, ensuring AI consistently mimics the character's tone and speaking habits.

- **📝 多轮对话与历史保存 | Multi-turn Dialogue & History Logging**  
  - 支持连续对话，全部保存至 `chat_log_V0.5.jsonl`。
  - Supports continuous multi-turn conversations with automatic logging into `chat_log_V0.5.jsonl`.

- **📋 会话总结 | Session Summarization**  
  - 输入 `exit` 或 `quit` 自动总结本次对话，并更新至长期记忆。
  - When `exit` or `quit` is entered, the session is automatically summarized and saved to long-term memory.

- **🖥️ 本地 UI 界面 | Local UI**  
  - 使用 PySide6 制作简洁聊天窗口，支持文本输入与消息展示。
  - Built with PySide6, offering a simple chat window for input and message display.

- **🔧 可扩展性 | Extensibility**  
  - 代码结构清晰，方便未来集成语音、图片、视频等多模态功能。
  - Clean code structure allows easy integration of voice, image, video, and other multimodal features.

---

## 🚀 使用方法 | How to Use  

1. **环境准备 | Environment Setup**
   - 安装 Python  
   - Install Python
   - 安装依赖 Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **准备数据文件 | Prepare Data Files**
   - `character_profile_V0.5.json`：虚拟人物设定 / Character profile
   - `long_term_memory_V0.5.jsonl`：长期记忆（可为空）/ Long-term memory (can be empty)
   - `cleaned_chat_2.jsonl`：历史对话数据 / Historical conversation data
   - `chat_log_V0.5.jsonl`：对话日志（自动生成）/ Chat log (auto-generated)

3. **运行程序 | Run the Program**
   ```bash
   python V0.5_Samaritan.py
   ```
	•	启动后弹出聊天窗口，即可开始与虚拟人物对话。
	•	A chat window will pop up. Start chatting with your virtual character immediately!

4. **结束会话 | End the Session**
	•	输入 exit 或 quit，自动总结并保存本次会话。
	•	Input exit or quit to summarize and save the session.

⸻

📂 文件说明 | File Description
	•	V0.5_Samaritan.py — 主程序 / Main program (UI and core logic)
	•	character_profile_V0.5.json — 虚拟人物设定 / Character profile
	•	long_term_memory_V0.5.jsonl — 长期记忆 / Long-term memory
	•	cleaned_chat_2.jsonl — 历史对话数据 / Historical conversation data
	•	chat_log_V0.5.jsonl — 聊天日志 / Chat log

⸻

🌈 项目亮点 | Highlights
	•	支持个性化设定与风格模仿
Supports highly personalized character settings and style imitation
	•	具备长期记忆与会话总结功能
Equipped with long-term memory and session summarization
	•	本地 UI，保护隐私
Local UI ensuring privacy and data security
	•	代码清晰，方便二次开发
Clean and extensible codebase for secondary development

⸻

🔮 未来展望 | Future Plans
	•	集成语音合成与语音对话
Integration of voice synthesis and voice-based interactions
	•	支持图片、视频等多模态交互
Support for multimodal interactions including images and videos
	•	增强记忆管理与情感分析
Enhanced memory management and emotional analysis
