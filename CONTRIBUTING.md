# Guia de Contribuição

Obrigado por seu interesse em contribuir com o **Extrator Mestre**! Este documento define as diretrizes para garantir que o projeto continue organizado e fácil de manter.

## 1. Configuração do Ambiente de Desenvolvimento

Para rodar o projeto localmente sem Docker, siga os passos abaixo:

### Pré-requisitos
- **Python 3.9+**
- **Poppler** (necessário para o `pdf2image`):
  - **Ubuntu/Debian:** `sudo apt-get install poppler-utils`
  - **macOS:** `brew install poppler`
  - **Windows:** Baixe os binários e adicione a pasta `bin` ao seu PATH.
- **libmagic** (necessário para `python-magic`):
  - **Ubuntu/Debian:** `sudo apt-get install libmagic1`
  - **macOS:** `brew install libmagic`

### Passo a Passo
1. Clone o repositório:
   ```bash
   git clone https://github.com/HiImYeda/extrator_mestre.git
   cd extrator_mestre
   ```

2. Crie um ambiente virtual (venv):
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - **Linux/macOS:** `source venv/bin/activate`
   - **Windows:** `venv\Scripts\activate`

4. Instale as dependências:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 2. Como Rodar o Projeto

### Executando a API
Para iniciar o servidor FastAPI com recarregamento automático (hot-reload):
```bash
python main.py
```
A API estará disponível em `http://localhost:8000`. Acesse `/docs` para a documentação interativa.

### Testes
Atualmente, o projeto utiliza testes manuais via Swagger ou scripts de exemplo (como o presente no README). 
**Dica para Contribuidores:** Ao adicionar novas funcionalidades, considere adicionar testes unitários usando `pytest`.

## 3. Padrões de Código

Para manter a consistência, por favor siga estas diretrizes:

- **Estilo:** Siga a [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Tipagem:** Use type hints sempre que possível para facilitar a legibilidade e validação com Pydantic.
- **Documentação:** Docstrings em funções complexas ajudam outros desenvolvedores a entender a lógica de extração.
- **Commits:** Tente usar mensagens claras e em português ou inglês (ex: `feat: adiciona suporte a arquivos RTF` ou `fix: corrige erro na extração de tabelas DOCX`).

## 4. Fluxo de Pull Request

1. **Crie uma Branch:** Nunca envie mudanças diretamente para a `main`.
   ```bash
   git checkout -b feature/minha-nova-funcionalidade
   ```
2. **Desenvolva e Teste:** Certifique-se de que sua alteração não quebrou os formatos de arquivos já suportados (PDF, DOCX, XLSX, Imagens).
3. **Faça o Push:**
   ```bash
   git push origin feature/minha-nova-funcionalidade
   ```
4. **Abra um PR:** No GitHub, abra um Pull Request descrevendo:
   - O que foi alterado.
   - Por que a alteração é necessária.
   - Como testar a mudança.

---
Se tiver dúvidas, sinta-se à vontade para abrir uma Issue!