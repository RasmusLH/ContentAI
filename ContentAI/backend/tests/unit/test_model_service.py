import pytest
from unittest.mock import patch, MagicMock
from app.services.model_service import ModelService
from app.utils.error_handlers import APIError

def test_model_service_initialization():
    with patch('openai.OpenAI') as mock_openai:
        service = ModelService()
        assert service.client is not None
        mock_openai.assert_called_once()

def test_model_service_initialization_failure():
    with patch('openai.OpenAI', side_effect=Exception("API Key invalid")):
        with pytest.raises(APIError) as exc_info:
            ModelService()
        assert exc_info.value.status_code == 500
        assert "Failed to initialize AI model" in str(exc_info.value)

def test_get_model_without_client():
    service = ModelService()
    service.client = None
    with pytest.raises(APIError) as exc_info:
        service.get_model()
    assert exc_info.value.status_code == 500
    assert "OpenAI client not initialized" in str(exc_info.value)
