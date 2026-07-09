# Agente de Saúde

Assistente conversacional em Streamlit, restrito ao domínio de saúde,
usando um modelo gratuito via [OpenRouter](https://openrouter.ai).

> ⚠️ Este agente fornece informação geral sobre saúde. Não substitui
> diagnóstico, prescrição ou acompanhamento médico profissional.

## Estrutura do projeto

```
.
├── app.py              # Interface Streamlit (UI e orquestração)
├── agent.py            # Prompt de sistema, chamada à API, tratamento de erro
├── config.py           # Leitura de variáveis de ambiente
├── requirements.txt
├── render.yaml          # Blueprint opcional para deploy no Render
├── .env.example
└── .gitignore
```

## Rodando localmente

1. Clone o repositório e entre na pasta:
   ```bash
   git clone <url-do-seu-repositorio>
   cd <pasta-do-projeto>
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e preencha sua chave:
   ```bash
   cp .env.example .env
   ```
   Gere sua chave gratuita em https://openrouter.ai/keys e cole em
   `OPENROUTER_API_KEY` dentro do `.env`.

4. Rode a aplicação:
   ```bash
   streamlit run app.py
   ```
   O navegador abrirá automaticamente em `http://localhost:8501`.

## Publicando no GitHub

```bash
git init
git add .
git commit -m "Agente de saude - versao inicial"
git branch -M main
git remote add origin <url-do-seu-repositorio-no-github>
git push -u origin main
```

O `.env` não será enviado ao GitHub (está no `.gitignore`) — a chave da
API fica só no seu ambiente local e depois no painel do Render.

## Deploy no Render

**Opção A — via Blueprint (mais rápido, usa o `render.yaml` incluído):**

1. No painel do Render, clique em **New +** → **Blueprint**.
2. Conecte sua conta GitHub e selecione este repositório.
3. O Render vai ler o `render.yaml` e propor o serviço automaticamente.
4. Quando solicitado, cole sua chave em `OPENROUTER_API_KEY`.
5. Clique em **Apply** — o deploy começa automaticamente.

**Opção B — configurando manualmente:**

1. No painel do Render, clique em **New +** → **Web Service**.
2. Conecte o repositório GitHub.
3. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Em **Environment Variables**, adicione `OPENROUTER_API_KEY` com sua
   chave (e, opcionalmente, `OPENROUTER_MODEL` se quiser trocar o
   modelo padrão).
5. Escolha o plano **Free** e clique em **Create Web Service**.

A cada `git push` na branch conectada, o Render refaz o deploy
automaticamente.

## Sobre o modelo gratuito

O `OPENROUTER_MODEL` padrão é `meta-llama/llama-3.2-3b-instruct:free`.
Modelos gratuitos no OpenRouter mudam de disponibilidade com certa
frequência — se parar de funcionar, confira a lista atual em
https://openrouter.ai/models?max_price=0 e ajuste a variável de
ambiente `OPENROUTER_MODEL` sem precisar alterar código.

## Decisões e suposições assumidas nesta versão

- **Sem autenticação**: o app é single-user/uso aberto. Se for expor
  publicamente para múltiplos usuários, considere adicionar
  autenticação (o Streamlit tem suporte nativo simples via
  `st.secrets` + senha, ou algo mais robusto como OAuth).
- **Sem persistência**: o histórico de conversa vive só na sessão do
  navegador (`st.session_state`) e some ao recarregar a página. Se
  precisar de histórico entre sessões, isso exigiria um banco de dados
  e, por ser dado de saúde, atenção redobrada a criptografia e LGPD.
- **Restrição de domínio via prompt de sistema**: o agente é instruído
  a só falar sobre saúde diretamente no prompt enviado ao modelo, não
  por um filtro de palavras-chave no código — isso é mais resistente a
  tentativas de contornar a restrição.
- **Sem log de conteúdo de conversa**: como o domínio é saúde, o
  código não grava o conteúdo das mensagens em log algum, para evitar
  reter dado sensível desnecessariamente.
