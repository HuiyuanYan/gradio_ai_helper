from abc import ABC, abstractmethod
from typing import Dict

class ContentAnalyzer(ABC):
    """Abstract base class for content analysis."""

    @abstractmethod
    def _analyze(self, file_path: str) -> Dict:
        """The concrete implementation of this method must analyze the file."""
        pass

    def analyze(self, file_path: str) -> Dict:
        """Performs analysis and ensures the result contains 'real' and 'fake' keys."""
        res = self._analyze(file_path)
        assert 'real' in res and 'fake' in res, "Result must contain 'real' and 'fake' keys"
        return res
