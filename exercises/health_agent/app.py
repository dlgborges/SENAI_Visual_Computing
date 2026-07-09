"""
Interface Streamlit do agente de saúde.

Este módulo só cuida de UI e orquestração — toda a lógica de negócio
(prompt de sistema, chamada à API, tratamento de erro) vive em agent.py,
e toda leitura de configuração vive em config.py. Manter essa separação
é o que permite testar/trocar a lógica do agente sem mexer na interface.
"""

import streamlit as st

import agent
import config

st.set_page_config(page_title=config.APP_NAME, page_icon="🩺")


def _validate_config_or_stop() -> None:
    """Mostra um erro claro na tela se a configuração estiver incompleta,
    em vez de deixar o app quebrar na primeira mensagem enviada."""
    try:
        config.validate()
    except config.ConfigError as exc:
        st.error(str(exc))
        st.stop()


def _init_session_state() -> None:
    # Histórico mantido apenas durante a sessão do navegador (não é
    # persistido em disco/banco). Ao fechar ou recarregar a aba, o
    # histórico se perde — comportamento assumido para esta primeira
    # versão do projeto.
    if "messages" not in st.session_state:
        st.session_state.messages = []


def _render_history() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def _handle_user_input(user_text: str) -> None:
    if len(user_text) > config.MAX_INPUT_CHARS:
        st.warning(
            f"Sua mensagem tem mais de {config.MAX_INPUT_CHARS} "
            "caracteres. Por favor, resuma e envie novamente."
        )
        return

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            try:
                result = agent.get_response(st.session_state.messages)
                reply_text = result.text
            except agent.AgentError as exc:
                reply_text = f"⚠️ {exc}"
        st.markdown(reply_text)

    st.session_state.messages.append({"role": "assistant", "content": reply_text})


def main() -> None:
    _validate_config_or_stop()
    _init_session_state()

    st.title("🩺 " + config.APP_NAME)
    st.caption(
        "Assistente de informações gerais sobre saúde. Não substitui "
        "consulta, diagnóstico ou tratamento médico."
    )

    _render_history()

    user_text = st.chat_input("Digite sua pergunta sobre saúde...")
    if user_text:
        _handle_user_input(user_text)


if __name__ == "__main__":
    main()
