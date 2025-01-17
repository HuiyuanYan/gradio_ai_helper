import sys,os
sys.path.append(os.getcwd())
from src.settings import Settings
from src.utils import logger
import gradio as gr
from src.analyzer import AnalyzerContainer


from openai import OpenAI

from src.utils import (
    SUPPORTED_FORMATS,
    MAX_FILE_NUM,
    SUPPORTED_MODELS,
    get_all_supported_models,
    generate_html_for_file,
    convert_message_dict_to_user_input
)

client = OpenAI(
    api_key=Settings.basic_settings.env["OPENAI_API_KEY"],
    base_url=Settings.basic_settings.env["OPENAI_BASE_URL"]
)
conversation_history =[]

analyzer_container = AnalyzerContainer()


def predict(message, history,max_history_rounds,temperature,modality,model):
    logger.info(f"Message:{message}\nHistory:{history}Temperature:{temperature}\nModality:{modality}\nModel:{model}")
    assert model in SUPPORTED_MODELS[modality], f"model {model} not supported for modality {modality}"

    global conversation_history, client
    # 检查历史对话记录的长度是否超过最大允许的轮次
    if len(history) > max_history_rounds:
        # 如果超过，删除最早的对话记录，以保持对话记录的长度在最大轮次内
        conversation_history = conversation_history[len(history) - max_history_rounds:]
    
    if history:
        # 将历史对话记录添加到消息列表中
        conversation_history.append(history[-1])

    # 构建消息列表，将历史对话记录转换为openai格式
    user_content = convert_message_dict_to_user_input(message,modality)
    
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

def analyze(files):
    ret = []
    file_num = len(files) if files else 0
    for i in range(MAX_FILE_NUM):
        if i < file_num:
            ret.append(analyzer_container.analyze(files[i]))
        else:
            ret.append({})
    return ret


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
logger.info(f"Starting Gradio AI Helper_{Settings.basic_settings.version}...")
with gr.Blocks(js=js) as iface:
    gr.Markdown(f"#     ![GitHub stars]({Settings.basic_settings.shields_start_url})")
    gr.Markdown("支持多模态对话，以及AIGC伪造内容识别")
    with gr.Tab("🗣️ AI对话 "):
        gr.ChatInterface(
            fn=predict,
            type="messages",
            multimodal=True,
            additional_inputs=[
                gr.Slider(1, 10, value=Settings.llm_settings.default_history_len, label="最大历史交互轮次", step=1),
                gr.Slider(0,1,value=Settings.llm_settings.default_temperature,label="温度，越大越随机"),
                gr.Dropdown(SUPPORTED_MODELS.keys(),value=Settings.llm_settings.default_llm_type,label="模态，对话开始后不要改变该参数！"),
                gr.Dropdown(get_all_supported_models(),value=Settings.llm_settings.default_llm,label="模型，对话开始后不要改变，因为不同模型的传参格式可能不一样！"),
            ]
        )
    with gr.Tab("🔍 内容识别"):
        with gr.Row():
            with gr.Column(f"上传文件,最多上传{MAX_FILE_NUM}个文件",scale=1):
                file_input = gr.File(label="上传文件，支持文本、视频、音频等多种格式",file_count="multiple",file_types=list(SUPPORTED_FORMATS.keys()))
                
                html_list = [gr.HTML() for _ in range(MAX_FILE_NUM)]
                def show_files(files):
                    ret = []
                    file_num = len(files) if files else 0
                    for i in range(MAX_FILE_NUM):
                        if i < file_num:
                            ret.append(generate_html_for_file(files[i]))
                        else:
                            ret.append("")
                    
                    return ret
                
                file_input.change(show_files,file_input,html_list)
                

            with gr.Column("识别结果",scale=1):
                label_list = [gr.Label(label = f'文件{i+1}识别结果：',every=0.01) for i in range(MAX_FILE_NUM)]
                btn = gr.Button("开始识别")
                btn.click(analyze,file_input,label_list)

iface.launch()
