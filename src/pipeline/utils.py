from transformers import pipeline
from src.pipeline.deep4snet_pipeline import Deep4snetAudioPipeline
from src.pipeline.deep_fake_pipeline import DeepFakeVideoPipeline

SUPPORTED_PIPELINE_TYPES = [
    'hf_pipeline',
    'deep4snet_audio_pipeline',
    'deep_fake_video_pipeline'
]

def get_pipeline(pipeline_type, **kwargs):
    """Factory function to get a pipeline based on the type."""
    if pipeline_type == 'hf_pipeline':
        return pipeline(**kwargs)
    elif pipeline_type == 'deep4snet_audio_pipeline':
        model_path = kwargs.get('model_path')
        weights_path = kwargs.get('weights_path')
        if not model_path or not weights_path:
            raise ValueError("model_path and weights_path must be provided for deep4snet_audio pipeline.")
        return Deep4snetAudioPipeline(model_path,weights_path)
    elif pipeline_type == 'deep_fake_video_pipeline':
        task = kwargs.get('task')
        model = kwargs.get('model')
        if not task or not model:
            raise ValueError("task and model must be provided for deep_fake_video pipeline.")
        return DeepFakeVideoPipeline(task, model)
    else:
        raise ValueError(f"Unknown pipeline type: {pipeline_type}, supported types are: {SUPPORTED_PIPELINE_TYPES}")