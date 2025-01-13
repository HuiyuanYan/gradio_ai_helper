# 基于Gradio构建的智能AI助手

基于Gradio构建的简易支持多模态对话和AI伪造内容识别助手。


![python badge](https://img.shields.io/badge/conda-23.7.4-green)
![python badge](https://img.shields.io/badge/python-3.12-blue)
![python badge](https://img.shields.io/badge/gradio-5.9.1-orange)

## ⚠️ 注意！！！

本项目仅供学习参考，伪造内容识别不具有任何现实指导意义！！！

+ 多模态对话模型：`qwen-long`、`qwen-vl-max-0809`、`qwen-audio-turbo`

+ 文本识别模型：`ayZhou/e5-small-lora-ai-generated-detector`

+ 图片识别模型：`umm-maybe/AI-image-detector`

+ 音频识别模型：`weights_Deep4SNet`

+ 视频识别模型：`dima806/deepfake_vs_real_image_detection`

> **important！！！**
> 由于使用的音频识别模型`Deep4SNet`基于的`tensorflow`版本过低，导致在现行`tensorflow`运行过程中可能会报错，请自行修改或更换模型！

## 🎁 更新

- [x] [2025/1/14] 小更新，为项目增加了日志功能。

- [x] [2025/1/13] 支持自定义pipeline识别伪造文件内容，现在每种识别模式均可以选择`huggingface`官方的`pipeline`和自己定义的`CustomPipeline`了，自定义pipeline请参见`src/pipeline`文件夹相关逻辑，并且在`cfg/analyzer.yaml`文件中进行配置。

- [x] [2025/1/11] 现在所有配置均可以在cfg文件夹下进行配置了！参数详情请参见`cfg`文件夹下的三个yaml文件。

- [x] [2025/1/9] 初步构建Dockerfile, 支持Docker部署

- [x] [2025/1/7] 完成了视频、音频、图片的伪造内容识别分析

- [x] [2025/1/4] 更新了Gradio逻辑和界面，支持多文件上传

- [x] [2025/1/1] 完成了多模态AI对话、文本内容分析

- [x] [2024/12/30] 初步构建Gradio界面




**!!!本项目计划用作xjtu 2024秋 数据库系统原理及应用大作业，使用时请注意甄别。**

+ 支持多模态大预言模型对话
+ 支持不同模态AIGC伪造内容识别

![](./assets/main.png)

# 📌 安装虚拟环境
```bash
conda create -n ai_helper python=3.12

conda activate ai_helper

pip install -r requirements.txt
```

# 📋 配置环境变量

在`cfg/basic.yaml`文件中配置相关环境变量：
```yaml
# basic.yaml
version: 0.0.1
log_dir: ./logs
shields_start_url: https://img.shields.io/github/stars/HuiyuanYan/gradio_ai_helper?style=plastic
env:
  HF_ENDPOINT: https://hf-mirror.com
  GRADIO_TEMP_DIR: ./tmp
  OPENAI_BASE_URL: https://dashscope.aliyuncs.com/compatible-mode/v1
  OPENAI_API_KEY: sk-xxx
```

在`cfg/llms.yaml`进行大语言模型相关配置：
```yaml
# llms.yaml
default_history_len: 3
default_temperature: 0.7
default_llm: qwen-long
deault_llm_type: text

supported_llms:
  text:
    - qwen-long
  image:
    - qwen-vl-max-0809
  audio:
    - qwen-audio-turbo
```

在`cfg/analyzer.yaml`进行伪造内容识别相关配置（在2025/1/13的更新中，已经可以支持自定义pipeline，相关逻辑参见`src/pipeline`文件夹）：
```yaml
# analyzer.yaml
max_file_num: 4
supported_file_formats:
  image:
    - .jpg
    - .jpeg
    - .png
    - .webp
  video:
    - .mp4
    - .avi
    - .webm
  audio:
    - .mp3
    - .wav
  text:
    - .md
    - .txt
    - .doc
    - .pdf

image_analyzer:
  pipeline: hf_pipeline
  args:
    task: image-classification
    model: umm-maybe/AI-image-detector

text_analyzer:
  pipeline: hf_pipeline
  args:
    task: text-classification
    model: MayZhou/e5-small-lora-ai-generated-detector

audio_analyzer:
  pipeline: deep4snet_audio_pipeline
  args:
    model_path: ./models/deep4snet/model_Deep4SNet.h5
    weights_path: ./models/deep4snet/weights_Deep4SNet.h5
  
video_analyzer:
  pipeline: deep_fake_video_pipeline
  args:
    task: image-classification
    model: dima806/deepfake_vs_real_image_detection
```



# ⏰ 运行
```bash
python src/main.py
```
然后按照输出访问对应地址即可。

两种模式的效果展示如下：
![](./assets/chat/demo1.png)

![](./assets/recognition/demo1.png)
