# Extrator Mestre

API para extração de conteúdo de diferentes tipos de arquivos (PDF, DOCX, XLSX e imagens).

## Requisitos

- Docker

## Como construir e executar com Docker

1. Construa a imagem Docker:

```bash
docker build -t extrator-mestre .
```

2. Execute o contêiner:

```bash
docker run -p 8000:8000 extrator-mestre
```

A API estará disponível em `http://localhost:8000`.

## Documentação da API

A documentação interativa da API estará disponível em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Exemplo de uso

Para enviar um arquivo para processamento:

```python
import requests
import base64

# Caminho para o arquivo que você deseja enviar
caminho_arquivo = "caminho/para/seu/arquivo.pdf"  # ou .docx, .xlsx, imagem, etc.

# Ler o arquivo e codificar em base64
with open(caminho_arquivo, "rb") as arquivo:
    conteudo_bytes = arquivo.read()
    conteudo_base64 = base64.b64encode(conteudo_bytes).decode('utf-8')

# Preparar o payload JSON
payload = {
    "file_base64": conteudo_base64
}

# Enviar a requisição POST para a API
url = "http://localhost:8000/process-file/"
resposta = requests.post(url, json=payload)

# Exibir o resultado
print(resposta.status_code)
print(resposta.json())
```

## Implantação no EasyPanel

1. No EasyPanel, vá para "Applications" e clique em "New App"
2. Selecione "Dockerfile" como método de implantação
3. Configure o repositório Git onde este código está hospedado
4. Configure a porta 8000
5. Clique em "Deploy" 