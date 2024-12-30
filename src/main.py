import sys,os
sys.path.append(os.getcwd())
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
from src.utils import SUPPORTED_FORMATS
from src.analyzer import AnalyzerContainer
# 初始化 AnalyzerContainer

import openai
from openai import OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY","")
openai.base_url = os.environ.get("OPENAI_BASE_URL","")
client = OpenAI(
    api_key=openai.api_key,
    base_url=openai.base_url
)
from src.utils import (
    get_all_supported_models,
    SUPPORTED_MODELS_DICT,
    convert_message_dict_to_user_input
)
conversation_history =[]

analyzer_container = AnalyzerContainer()

STAR_URL = os.environ.get("SHEILDS_START_URL","https://img.shields.io/github/stars/HuiyuanYan/gradio_ai_helper?style=plastic")


def predict(message, history,max_history_rounds,temperature,modality,model):
    print(f'Message:{message}\nHistory:{history}')
    assert model in SUPPORTED_MODELS_DICT[modality], f"model {model} not supported for modality {modality}"

    global conversation_history, client
    # 检查历史对话记录的长度是否超过最大允许的轮次
    if len(history) > max_history_rounds:
        # 如果超过，删除最早的对话记录，以保持对话记录的长度在最大轮次内
        conversation_history = conversation_history[len(history) - max_history_rounds:]
    
    if history:
        # 将历史对话记录添加到消息列表中
        conversation_history.append(history[-1])

    # 构建消息列表，将历史对话记录转换为openai格式
    user_content = convert_message_dict_to_user_input(message,model)
    
    # 将用户消息添加到消息列表中
    conversation_history.append({"role": "user", "content": user_content})

    # 调用openai的ChatCompletion接口，发送消息列表和其他参数，获取回复
    response = client.chat.completions.create(
        model=model,
        messages=conversation_history,
        temperature=temperature,
    )
    
    # 从回复中提取文本内容
    reply = response.choices[0].message.content
    return reply

def analyze(file):
    print(file)
    return analyzer_container.analyze(file)


js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';

    var text = '🤖 AI智能体助手';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 50);
            }, i * 250);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""

# 简化界面，移除手动选择文件类型
with gr.Blocks(js=js) as iface:
    iface.theme = gr.themes.Base()
    gr.Markdown(f"#     ![GitHub stars]({STAR_URL})")
    gr.Markdown("支持多模态对话，以及AI生成内容识别")
    with gr.Tab("🗣️ AI对话 "):
        gr.ChatInterface(
            fn=predict,
            type="messages",
            multimodal=True,
            additional_inputs=[
                gr.Slider(1, 10, value=1, label="最大历史交互轮次", step=1),
                gr.Slider(0,1,value=0.7,label="温度，越大越随机"),
                gr.Dropdown(SUPPORTED_MODELS_DICT.keys(),value='image',label="模态，对话开始后不要改变该参数！"),
                gr.Dropdown(get_all_supported_models(),value='qwen-vl-max-0809',label="模型，对话开始后不要改变，因为不同模型的传参格式可能不一样！"),
            ]
        )

    with gr.Tab("🔍 内容识别"):
        gr.Interface(
            fn=analyze,
            inputs=gr.File(label="上传文件，文本只支持utf-8格式", file_types=list(SUPPORTED_FORMATS.keys())),
            outputs="label",
        )

iface.launch()
