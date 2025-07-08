# main.py
import base64
import magic
import io
import pandas as pd
import docx
from pdf2image import convert_from_bytes
import pdfplumber
import uvicorn
from PIL import Image

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Union, Literal, Optional

# --- Pydantic Models for the Unified Structure ---
# Modelos que definem a estrutura de saída unificada para a API.

class ImageData(BaseModel):
    """Define a estrutura para retornar dados de imagem."""
    original_mime_type: str
    image_base64_png: str

class TextBlock(BaseModel):
    """Define um bloco de conteúdo de texto."""
    type: Literal["bloco_texto"] = "bloco_texto"
    source_page: Optional[int] = None
    content: str

class ImageBlock(BaseModel):
    """Define um bloco de conteúdo de imagem."""
    type: Literal["bloco_imagem"] = "bloco_imagem"
    source_page: Optional[int] = None
    content: ImageData

class FileInput(BaseModel):
    """Modelo de entrada para a requisição da API."""
    file_base64: str

class UnifiedProcessResponse(BaseModel):
    """Modelo de resposta unificada para a API."""
    status: Literal["success", "error"]
    content_type: Literal["documento_unificado", "unsupported", "error"]
    data: Union[List[Union[TextBlock, ImageBlock]], None]
    message: str

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Serviço de Extração Unificada de Dados",
    description="Uma API que recebe um arquivo em base64 e retorna uma estrutura de conteúdo unificada para agentes de IA.",
    version="4.0.0",
)

# --- Core Processing Function ---

def process_base64_file(base64_string: str) -> dict:
    """
    Decodifica uma string base64, identifica o tipo de arquivo e retorna
    uma lista unificada de blocos de conteúdo (texto e/ou imagem).
    """
    try:
        decoded_bytes = base64.b64decode(base64_string)
        mime_type = magic.from_buffer(decoded_bytes, mime=True)
        file_stream = io.BytesIO(decoded_bytes)
        
        content_blocks = []

        # --- PDF Processing (Unified Logic) ---
        if mime_type == 'application/pdf':
            try:
                with pdfplumber.open(file_stream) as pdf:
                    for page in pdf.pages:
                        # Tenta extrair texto da página
                        page_text = page.extract_text(x_tolerance=2)
                        
                        if page_text and page_text.strip():
                            content_blocks.append(TextBlock(source_page=page.page_number, content=page_text.strip()))
                        else:
                            # Se não houver texto, converte a página em imagem PNG de alta qualidade
                            page_image = convert_from_bytes(decoded_bytes, fmt='png', first_page=page.page_number, last_page=page.page_number)[0]
                            buffered = io.BytesIO()
                            page_image.save(buffered, format="PNG", optimize=False, compress_level=0)
                            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                            image_content = ImageData(original_mime_type=mime_type, image_base64_png=img_str)
                            content_blocks.append(ImageBlock(source_page=page.page_number, content=image_content))
                
                return {"status": "success", "content_type": "documento_unificado", "data": content_blocks, "message": f"PDF processado. Total de {len(content_blocks)} páginas."}

            except Exception as pdf_error:
                 raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {pdf_error}")

        # --- Image Processing ---
        elif mime_type.startswith('image/'):
            img = Image.open(file_stream)
            # Mantém o modo original da imagem para preservar a qualidade
            buffered = io.BytesIO()
            # Salva como PNG com qualidade máxima
            img.save(buffered, format="PNG", optimize=False, compress_level=0)
            png_base64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_data = ImageData(original_mime_type=mime_type, image_base64_png=png_base64_string)
            content_blocks.append(ImageBlock(content=image_data))
            return {"status": "success", "content_type": "documento_unificado", "data": content_blocks, "message": f"Arquivo de imagem ({mime_type}) processado."}

        # --- DOCX Processing ---
        elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            doc = docx.Document(file_stream)
            full_text = [para.text for para in doc.paragraphs]
            content_blocks.append(TextBlock(content='\n'.join(full_text)))
            return {"status": "success", "content_type": "documento_unificado", "data": content_blocks, "message": "Arquivo DOCX processado."}

        # --- XLSX Processing ---
        elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file_stream)
            content_blocks.append(TextBlock(content=df.to_string()))
            return {"status": "success", "content_type": "documento_unificado", "data": content_blocks, "message": "Arquivo XLSX processado."}
        
        # --- Unsupported File Type ---
        else:
            return {"status": "error", "content_type": "unsupported", "data": None, "message": f"Tipo de arquivo não suportado: {mime_type}"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ocorreu um erro inesperado: {str(e)}")

# --- API Endpoint Definition ---
@app.post("/process-file/", response_model=UnifiedProcessResponse, tags=["File Processing"])
async def create_processing_job(file_input: FileInput):
    """
    Recebe um arquivo codificado em base64 e o transforma em uma estrutura
    de conteúdo unificada, pronta para ser consumida por agentes de IA.
    """
    result = process_base64_file(file_input.file_base64)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/", tags=["Health Check"])
async def read_root():
    """Endpoint raiz para verificar se a API está online."""
    return {"status": "ok", "message": "Serviço de Extração Unificada de Dados está no ar!"}

# --- To run the server directly for testing ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
