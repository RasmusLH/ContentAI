import logging
from fastapi import HTTPException, UploadFile
from typing import List

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self):
        self.ALLOWED_EXTENSIONS = {'.txt', '.doc', '.docx'}
        self.MAX_FILE_SIZE = 50 * 1024  # 50KB per file
        self.MAX_TOTAL_SIZE = 200 * 1024  # 200KB total

    async def process_files(self, files: List[UploadFile]) -> List[str]:
        """Process and validate uploaded files"""
        if not files:
            return []

        total_size = 0
        document_texts = []
        
        for file in files:
            try:
                # Check file extension
                file_ext = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
                if file_ext not in self.ALLOWED_EXTENSIONS:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File type {file_ext} not allowed. Supported types: {', '.join(self.ALLOWED_EXTENSIONS)}"
                    )

                content = await file.read()
                size = len(content)
                
                if size > self.MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File {file.filename} exceeds maximum size of 50KB"
                    )
                
                total_size += size
                if total_size > self.MAX_TOTAL_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail="Total size of all files exceeds 200KB"
                    )
                
                await file.seek(0)
                try:
                    text = content.decode('utf-8')
                    document_texts.append(text)
                except UnicodeDecodeError:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File {file.filename} appears to be binary or not a valid text document"
                    )
                    
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error processing file {file.filename}: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Error processing file {file.filename}"
                )
        
        return document_texts
