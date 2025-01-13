class CustomPipeline:
    def __init__(self, **kwargs):
        """Initialize the pipeline."""
        pass

    def _preprocess(self, input_data):
        """Preprocess the input data."""
        raise NotImplementedError("Preprocess method must be implemented by subclasses.")

    def _predict(self, processed_data):
        """Predict using the preprocessed data."""
        raise NotImplementedError("Predict method must be implemented by subclasses.")

    def _postprocess(self, prediction):
        """Postprocess the prediction."""
        raise NotImplementedError("Postprocess method must be implemented by subclasses.")

    def __call__(self, input_data):
        """Call the pipeline to process the input data."""
        processed_data = self._preprocess(input_data)
        prediction = self._predict(processed_data)
        result = self._postprocess(prediction)
        return result