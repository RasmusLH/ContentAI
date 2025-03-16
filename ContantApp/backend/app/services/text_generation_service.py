import logging
from typing import List, Optional
from openai.types.chat import ChatCompletion
from .model_service import ModelService
from ..config import settings

logger = logging.getLogger(__name__)

class TextGenerationService:
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

    def _create_prompt(self, template: str, objective: str, context: str, document_texts: Optional[List[str]] = None) -> str:
        prompt = f"Topic: {objective}\n\nContext: {context}\n\n"
        
        if document_texts and len(document_texts) > 0:
            prompt += "\nAdditional Context from Documents:\n"
            for i, text in enumerate(document_texts, 1):
                summary = text[:1000] + "..." if len(text) > 1000 else text
                prompt += f"Document {i}:\n{summary}\n\n"
        
        prompt += f"Template Guidelines: {template}\n\n"
        return prompt

    def _validate_response(self, response: ChatCompletion) -> None:
        if not response.choices:
            raise ValueError("No choices in response")
        if not response.choices[0].message:
            raise ValueError("No message in first choice")
        if not response.choices[0].message.content:
            raise ValueError("Empty message content")

    async def generate(self, template: str, objective: str, context: str, document_texts: Optional[List[str]] = None) -> str:
        try:
            client = self.model_service.get_model()
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": self._create_prompt(
                        template, objective, context, document_texts
                    )}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
                presence_penalty=settings.presence_penalty,
                frequency_penalty=settings.frequency_penalty
            )
            
            self._validate_response(response)
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}", exc_info=True)
            raise
