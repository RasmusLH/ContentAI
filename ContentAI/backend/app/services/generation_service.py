import logging
from typing import Dict, Any, List, Optional
from openai.types.chat import ChatCompletion
from .model_service import ModelService
from ..config import settings

logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self, model_service: ModelService):
        self.model_service = model_service

    def _create_system_prompt(self) -> str:
        return (
            "You are a professional LinkedIn Marketing Specialist with expertise in creating "
            "engaging and impactful posts. Follow these guidelines:\n"
            "1. Start with a bold, attention-grabbing headline\n"
            "2. Write in a professional yet conversational tone\n"
            "3. Include specific, actionable insights\n"
            "4. Use clear paragraph breaks for readability\n"
            "5. End with a compelling call-to-action\n"
            "6. Keep paragraphs concise (2-4 sentences)\n"
            "7. Format using LinkedIn-optimized structure\n"
        )

    def _create_user_prompt(self, template: str, objective: str, context: str, document_texts: Optional[List[str]] = None) -> str:
        prompt = (
            f"Topic: {objective}\n\n"
            f"Context: {context}\n\n"
        )
        
        if document_texts and len(document_texts) > 0:
            prompt += "\nAdditional Context from Documents:\n"
            for i, text in enumerate(document_texts, 1):
                # Take first 1000 chars of each document to avoid token limits
                summary = text[:1000] + "..." if len(text) > 1000 else text
                prompt += f"Document {i}:\n{summary}\n\n"
        
        prompt += (
            f"Template Guidelines: {template}\n\n"
            "Create a LinkedIn post that includes:\n"
            "- A compelling headline\n"
            "- Main content with key points\n"
            "- A clear call-to-action\n"
            "- 2-3 relevant hashtags"
        )
        
        return prompt

    def _validate_response(self, response: ChatCompletion) -> None:
        if not response.choices:
            raise ValueError("No choices in response")
        if not response.choices[0].message:
            raise ValueError("No message in first choice")
        if not response.choices[0].message.content:
            raise ValueError("Empty message content")

    def generate_text(
        self, 
        template: str, 
        request_objective: str, 
        request_context: str,
        document_texts: Optional[List[str]] = None
    ) -> str:
        try:
            client = self.model_service.get_model()
            response = client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": self._create_user_prompt(
                        template, request_objective, request_context, document_texts
                    )}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
                presence_penalty=0.6,  # Encourage creativity
                frequency_penalty=0.3  # Reduce repetition
            )
            
            self._validate_response(response)
            return response.choices[0].message.content.strip()

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}", exc_info=True)
            raise
