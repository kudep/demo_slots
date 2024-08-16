import uuid
import itertools
import requests
import streamlit as st
import streamlit.components.v1 as components
from streamlit_chat import message

API_URL = "http://app:8000/chat"
model_options = ('Open Assistant', 'NER')


def query(payload, user_id) -> requests.Response:
    response = requests.post(
        API_URL + f"/?user_id={user_id}",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload,
    )
    return response


def send_and_receive(model_choice: str):
    """
    Send text inside the input field. Receive response from API endpoint.
    Add both the request and response to `user_requests` and `bot_responses`.
    """
    user_request = st.session_state["input"]

    if user_request == "":
        return

    st.session_state["user_requests"].append(user_request)

    bot_response = query(
        {
            "text": user_request,
            "misc": {"flag": model_choice}
        },
        user_id=st.session_state["user_id"]
        )
    bot_response.raise_for_status()

    bot_message = bot_response.json()["response"]["text"]

    st.session_state["bot_responses"].append(bot_message)

    st.session_state["input"] = ""


def reset():
    """
    Clear state when changing model type
    """
    st.session_state["user_id"] = str(uuid.uuid4())
    st.session_state["bot_responses"] = []
    st.session_state["user_requests"] = []


def main():
    st.set_page_config(page_title="Streamlit DFF Chat", page_icon=":robot:")
    st.header("Streamlit DFF Chat")

    if "user_id" not in st.session_state:
        st.session_state["user_id"] = str(uuid.uuid4())
    if "bot_responses" not in st.session_state:
        st.session_state["bot_responses"] = []
    if "user_requests" not in st.session_state:
        st.session_state["user_requests"] = []

    model_choice = st.selectbox('Model', model_options, on_change=reset)
    st.text_input("You: ", key="input")
    st.button("Send", on_click=send_and_receive, args=[model_choice])

    for i, bot_response, user_request in zip(
        itertools.count(0),
        st.session_state.get("bot_responses", []),
        st.session_state.get("user_requests", []),
    ):
        message(user_request, key=f"{i}_user", is_user=True)
        message(bot_response, key=f"{i}_bot")

    # add a component that presses the Send button whenever user presses the Enter key.
    components.html(
        """
    <script>
    const doc = window.parent.document;
    buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));
    const send_button = buttons.find(el => el.innerText === 'Send');
    doc.addEventListener('keypress', function(e) {
        switch (e.keyCode) {
            case 13: // (13 = Enter key)
                send_button.click();
                break;
        }
    });
    </script>
    """,
        height=0,
        width=0,
    )


if __name__ == "__main__":
    main()
