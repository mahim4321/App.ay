import streamlit as st
from groq import Groq

st.set_page_config(page_title="Sovereign AI", page_icon="👑")
st.title("👑 Sovereign AI")

# API Key - এটি Groq থেকে নিতে হয়, আপাতত টেস্ট করার জন্য:
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "gsk_Xm9f8R7yQz2Wp4Vn6K1bL3m0N7a5S9d8f7G6h5J4k3L2m1N0"))

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("আপনার হুকুম দিন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        response = completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
