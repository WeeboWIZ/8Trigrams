import gradio as gr
import random
import openai
import logging
from hexagrams import hexagrams

# 設定您的 OpenAI API 金鑰
openai.api_key = ""  # 請替換為您的實際 API 金鑰

# 設定日志
logging.basicConfig(
    filename='app.log',  # 日志文件名稱
    level=logging.INFO,  # 日志等級
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)

def generate_hexagram():
    hexagram = random.choice(hexagrams)
    hexagram_text = (
        f"卦象：{hexagram['name']} (第 {hexagram['number']} 卦)\n"
        f"卦辭：{hexagram['judgement']}\n"
        f"象曰：{hexagram['image']}"
    )
    return hexagram_text, hexagram

def interpret_hexagram(user_question, hexagram):
    prompt = (
        f"用戶問題：{user_question}\n"
        f"卦象：{hexagram['name']} (第 {hexagram['number']} 卦)\n"
        f"卦辭：{hexagram['judgement']}\n"
        f"象曰：{hexagram['image']}\n\n"
        "請結合上述卦象信息和用戶問題，生成詳細的内容完整的解卦分析。"
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一個專業的易經卦象解釋師，請根據用戶的問題深入結合卦象信息提供詳細的解釋。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        
        interpretation = response['choices'][0]['message']['content'].strip()
        return interpretation
    except Exception as e:
        return f"解卦時出現錯誤：{str(e)}"

def translate_text(text, target_language):
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3,
        )
        translation = response['choices'][0]['message']['content'].strip()
        return translation
    except Exception as e:
        return f"翻譯時出現錯誤：{str(e)}"

def detect_language(text):
    prompt = f"Please detect the language of the following text and respond with the language name in English:\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a language detection assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.0,
        )
        detected_language = response['choices'][0]['message']['content'].strip()
        return detected_language
    except Exception as e:
        return "Unknown Language"

# 定義 Gradio 的界面元素
with gr.Blocks() as demo:
    gr.Markdown("# ☯️Hexagram.AI☯️ - 卦象AI解析 - WIZ LAB")
    gr.Markdown("冥想，具象你的問題，點擊「卜卦」獲取卦象. Meditate & visualize your ask, click Divination to get Hexagrams")
    
    with gr.Row():
        with gr.Column():
            user_question = gr.Textbox(
                label="呼_呼_呼_吸_Deep breath",
                placeholder="記錄你的問題_Describe",
                lines=2
            )
            divination_btn = gr.Button("卜_卦_Divination")
            generated_hexagram = gr.Textbox(
                label="獲_取_卦_象_Ask_for_Hexagrams",
                interactive=False,
                lines=4
            )
        with gr.Column():
            interpret_btn = gr.Button("解_卦_結_果_Explanation")
            interpretation = gr.Textbox(
                label="解_卦_結_果_In the Hexagrams",
                interactive=False,
                lines=15
            )
    
    # 用於存儲當前會話的狀態
    state = gr.State({
        'hexagram': None,
        'interpretation': None
    })
    
    def on_divination_click(current_question, state_dict):
        if state_dict['hexagram'] is not None:
            # 已經卜卦過，返回已生成的卦象
            return state_dict['hexagram'], state_dict
        # 生成卦象
        hexagram_text, hexagram = generate_hexagram()
        # 更新狀態
        state_dict['hexagram'] = {
            'text': hexagram_text,
            'data': hexagram
        }
        # 記錄卜卦事件
        logging.info("用戶進行了一次卜卦操作。")
        return hexagram_text, state_dict
    
    def on_interpret_click(current_question, state_dict):
        if state_dict['hexagram'] is None:
            return "請先卜卦生成卦象 Divination first to get Hexagrams", state_dict
        if state_dict['interpretation'] is not None:
            # 已經解卦過，返回已生成的解卦結果
            return state_dict['interpretation'], state_dict
        # 進行解卦
        interpretation_text = interpret_hexagram(current_question, state_dict['hexagram']['data'])
        
        # 語言檢測和翻譯
        detected_language = detect_language(current_question)
        
        if detected_language not in ["Chinese", "中文"]:
            translated_interpretation = translate_text(interpretation_text, detected_language)
            full_interpretation = f"### 中文解卦\n{interpretation_text}\n\n### {detected_language} 版解卦\n{translated_interpretation}"
        else:
            full_interpretation = interpretation_text
        
        # 更新狀態
        state_dict['interpretation'] = full_interpretation
        # 記錄解卦事件
        logging.info("用戶進行了一次解卦操作。")
        return full_interpretation, state_dict
    
    def reset_states(new_question, state_dict):
        if new_question.strip() != "":
            # 當用戶更改問題時，重置狀態
            state_dict['hexagram'] = None
            state_dict['interpretation'] = None
            logging.info("用戶更改了問題，重置卜卦和解卦狀態。")
        return "", "", state_dict
    
    divination_btn.click(
        on_divination_click,
        inputs=[user_question, state],
        outputs=[generated_hexagram, state]
    )
    
    interpret_btn.click(
        on_interpret_click,
        inputs=[user_question, state],
        outputs=[interpretation, state]
    )

    user_question.change(
        reset_states,
        inputs=[user_question, state],
        outputs=[generated_hexagram, interpretation, state]
    )

# 啟動 Gradio 應用
if __name__ == "__main__":
    demo.launch()  # 將 share 設為 True 以生成公共 URL
