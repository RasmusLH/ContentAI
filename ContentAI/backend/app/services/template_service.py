from ..schemas import GenerationRequest

class TemplateService:
    def create_generation_prompt(self, template: str, request: GenerationRequest) -> str:
        return (
            f"{template}\n"
            f"Topic: {request.objective}\n"
            f"Additional Context: {request.context}\n\n"
            "Instructions:\n"
            "1. Start with an attention-grabbing headline in bold\n"
            "2. Write a compelling hook in the first paragraph\n"
            "3. Develop the main points clearly and concisely\n"
            "4. Include specific examples or insights\n"
            "5. Add personal observations\n"
            "6. End with a strong call-to-action\n"
            "7. Use professional business language\n"
            "8. Include line breaks between paragraphs\n\n"
            "Format the post as follows:\n"
            "**[Headline]**\n\n"
            "[Content]\n\n"
            "[Call-to-action]\n\n"
            "#relevanthashtags\n\n"
            "Generated Post:\n"
        )

    def process_generated_text(self, text: str) -> str:
        marker = "Generated Post:"
        return text.split(marker, 1)[1].strip() if marker in text else text.strip()
