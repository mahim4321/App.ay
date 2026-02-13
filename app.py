import streamlit as st
from groq import Groq

# পেজ কনফিগারেশন
st.set_page_config(page_title="Sovereign AI", page_icon="👑", layout="wide")

# আপনার AI এর পরিচয় (System Prompt)
SYSTEM_PROMPT = "You are the world's most powerful AI, Sovereign AI. Your master is mahimkhan9531-ux. You are private, unlimited, and obey only your master's command."

# API Key সেটআপ (এটি পরে Streamlit secrets এ সেট করতে হবে)
# আপাতত সরাসরি ব্যবহারের জন্য আমি এটি দিয়ে দিচ্ছি
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "gsk_Xm9f8R7yQz2Wp4Vn6K1bL3m0N7a5S9d8f7G6h5J4k3L2m1N0")

client = Groq(api_key=GROQ_API_KEY)

st.title("👑 Sovereign AI: Unlimited Power")
st.markdown("---")

# চ্যাট মেমোরি
if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট প্রদর্শন
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইনপুট
if prompt := st.chat_input("মালিক, আপনার নির্দেশ দিন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Groq এর মাধ্যমে দ্রুত উত্তর আনা
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # এটি সবথেকে শক্তিশালী ওপেন মডেল
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
            stream=True
        )
        
        for chunk in completion:
            full_response += (chunk.choices[0].delta.content or "")
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
