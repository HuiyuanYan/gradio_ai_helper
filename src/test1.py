import gradio as gr

def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths

with gr.Blocks() as demo:
    # 播放视频的html
    gr.HTML(
        """
        <video width="320" height="240" controls>
            <source src="/gradio_api/file=D:/workspace/Multimodal-artificial-intelligence-System/tmp/05bd857af7f70bf51b6aac1144046973bf3325c9101a554bc27dc9607dbbd8f5/sample-5s.mp4" type="video/mp4">
        </video>
        """
    )

demo.launch()