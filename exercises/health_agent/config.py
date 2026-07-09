"""
Leitura centralizada de configuração via variáveis de ambiente.

Mantido separado de agent.py e app.py para que nenhum outro módulo
precise saber *como* a configuração chega (env var, .env local, ou
variáveis de ambiente do Render em produção) — só importa o que ela
contém.
"""

import os

from dotenv import load_dotenv

# Em produção (Render) as variáveis de ambiente já vêm do painel do
# serviço. Em desenvolvimento local, carregamos de um arquivo .env se
# ele existir. load_dotenv() não sobrescreve variáveis já definidas no
# ambiente, então isso é seguro em ambos os casos.
load_dotenv()


class ConfigError(RuntimeError):
    """Erro de configuração ausente ou inválida."""


OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")

# Modelo gratuito padrão no OpenRouter. Modelos "free tier" mudam com
# certa frequência — confira a lista atualizada em
# https://openrouter.ai/models?max_price=0 e ajuste via variável de
# ambiente OPENROUTER_MODEL se este deixar de estar disponível.
OPENROUTER_MODEL: str = os.getenv(
    "OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free"
)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Limite de tamanho de input do usuário, em caracteres. Existe para
# evitar que uma mensagem excessivamente longa estoure custo/limite da
# API sem necessidade — não é uma medida de segurança contra ataque,
# é controle de custo e uso responsável da chave.
MAX_INPUT_CHARS: int = int(os.getenv("MAX_INPUT_CHARS", "2000"))

# Nome da aplicação, usado no título da página e em headers da API
# (o OpenRouter recomenda identificar a aplicação que faz a chamada).
APP_NAME: str = os.getenv("APP_NAME", "Agente de Saude")


def validate() -> None:
    """Levanta ConfigError se alguma configuração obrigatória faltar.

    Chamado explicitamente no início do app.py, em vez de falhar
    silenciosamente na primeira chamada à API — assim o usuário vê um
    erro claro de configuração, não um erro de rede confuso.
    """
    if not OPENROUTER_API_KEY:
        raise ConfigError(
            "OPENROUTER_API_KEY não encontrada. Defina essa variável de "
            "ambiente (localmente via arquivo .env, ou no painel do "
            "Render em produção) antes de rodar a aplicação."
        )
