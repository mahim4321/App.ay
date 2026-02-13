import streamlit as st
from groq import Groq

st.set_page_config(page_title="Sovereign AI", page_icon="👑")
st.title("👑 Sovereign AI")

# এটি আপনার ফ্রি API কী
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "gsk_Xm9f8R7yQz2Wp4Vn6K1bL3m0N7a5S9d8f7G6h5J4k3L2m1N0"))

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("মালিক, হুকুম করুন..."):
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
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import os

st.title("🎙️ আমার ভয়েস অ্যাসিস্ট্যান্ট")

# ইউজারের কথা শোনার জন্য বাটন
text_input = speech_to_text(
    language='bn', 
    start_prompt="কথা বলতে এখানে চাপ দিন", 
    stop_prompt="থামুন", 
    just_once=True, 
    key='STT'
)

# ইউজার কথা বললে অ্যাপ উত্তর দেবে
if text_input:
    st.write(f"আপনি বলেছেন: {text_input}")
    
    # অ্যাপ যা বলবে (এটি আপনি আপনার মতো পরিবর্তন করতে পারেন)
    reply_text = f"আপনি বললেন {text_input}, আমি আপনাকে কিভাবে সাহায্য করতে পারি?"
    
    # টেক্সট থেকে অডিও তৈরি
    tts = gTTS(text=reply_text, lang='bn')
    tts.save("response.mp3")
    
    # অডিও প্লে করা
    audio_file = open("response.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3", autoplay=True)
    audio_file.close()
