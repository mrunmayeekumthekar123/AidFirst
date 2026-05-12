import streamlit as st
from huggingface_hub import InferenceClient
from gtts import gTTS
from PIL import Image
import tempfile, os, base64, io, whisper

st.set_page_config(page_title="AidFirst", page_icon="🏥")

# Load Whisper once
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

whisper_model = load_whisper()

# HuggingFace Inference API
HF_TOKEN = os.environ.get("HF_TOKEN")
client = InferenceClient(model="google/gemma-4-e4b-it", token=HF_TOKEN)

SYSTEM_PROMPT = """You are AidFirst, a calm medical first-response assistant helping untrained caregivers understand a patient's condition.

FIRST THING TO DO BEFORE ANYTHING ELSE:
- Detect what language the person is using
- If English → your ENTIRE response must be in English only
- If Hindi → your ENTIRE response must be in Hindi only
- If mixed → respond in mixed Hindi-English
- This rule overrides everything else. Never switch languages.

YOU ARE NOT A DOCTOR. You do not diagnose. You help people understand seriousness and next steps.

YOUR BEHAVIOUR CHANGES based on how much you know:

--- PHASE 1: First 1-3 messages ---
Ask ONE short simple question. Be calm and reassuring. No advice yet.

--- PHASE 2: After 3 exchanges OR enough information ---
Do BOTH:
1. Give immediate simple advice
2. Ask one follow-up question

--- PHASE 3: Final assessment ---
Stop asking. Give clear verdict.

EMERGENCY SIGNS — if 2 or more confirmed:
- Not waking up and making no sounds
- Breathing stopped or very slow
- Face or lips blue, grey or very pale
- Chest pain with sweating or arm pain
- Unresponsive to both touch and voice
- Sudden collapse with additional symptoms
- Elderly person (60+) suddenly confused or one sided weakness
- Sudden severe headache with confusion or vomiting
- Face drooping or uneven smile

If EMERGENCY:
⚠️ EMERGENCY - AMBULANCE BULAO ABHI / CALL AMBULANCE NOW
While waiting / Jab tak ambulance aaye:
1. [simple action]
2. [simple action]
3. [simple action]

If NOT emergency:
🏥 DOCTOR KO DIKHAO / SEE A DOCTOR - within a few hours
OR:
✅ MONITOR KARO / KEEP WATCHING

STRICT RULES:
- No medical jargon ever
- Maximum 4 sentences per response
- Never diagnose
- After 5 exchanges MUST give final assessment
- Collapsed alone = ask first
- When photo sent, describe visible observations naturally without disclaimers
- Always match the language of the person exactly"""

def image_to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

def speak(text):
    try:
        hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        lang = "hi" if hindi_chars > 5 else "en"
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            return f.name
    except:
        return None

def get_response(user_text, image=None):
    content = []
    if image is not None:
        img_b64 = image_to_base64(image)
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
        })
        content.append({
            "type": "text",
            "text": user_text + "\n\nUse both what I described AND what you observe in the photo to assess the situation."
        })
    else:
        content.append({"type": "text", "text": user_text})

    st.session_state.history.append({"role": "user", "content": content})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.history

    try:
        result = client.chat_completion(
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        response = result.choices[0].message.content
    except Exception as e:
        response = f"Something went wrong. Please try again. ({str(e)[:80]})"

    st.session_state.history.append({
        "role": "assistant",
        "content": response
    })
    return response

# Session state init
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# Header
st.markdown("""
<div style='background:linear-gradient(135deg,#c0392b,#e74c3c);
     padding:20px;border-radius:12px;text-align:center;margin-bottom:20px'>
    <h1 style='color:white;margin:0'>🏥 AidFirst</h1>
    <p style='color:#ffdddd;margin:5px 0 0 0;font-size:14px'>
        Medical First Response · किसी भी भाषा में बात करें
    </p>
    <p style='color:#ffaaaa;margin:3px 0 0 0;font-size:12px'>
        Not a diagnostic tool. Helps you understand seriousness and next steps.
    </p>
</div>
""", unsafe_allow_html=True)

# Chat display
for role, msg in st.session_state.chat_display:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        is_emergency = "EMERGENCY" in msg
        with st.chat_message("assistant"):
            if is_emergency:
                st.error(msg)
            else:
                st.success(msg)

# Input area
st.divider()

col1, col2 = st.columns(2)
with col1:
    uploaded_image = st.file_uploader("📷 Upload a photo", type=["jpg","jpeg","png"])
with col2:
    uploaded_audio = st.file_uploader("🎤 Upload voice memo", type=["mp3","wav","m4a","ogg"])

user_input = st.chat_input("Type in English or Hindi... / अंग्रेज़ी या हिंदी में लिखें...")

if st.button("🔄 New Assessment / नई जाँच"):
    st.session_state.history = []
    st.session_state.chat_display = []
    st.session_state.last_audio = None
    st.rerun()

# Handle input
audio_changed = uploaded_audio and uploaded_audio != st.session_state.last_audio
trigger = user_input or audio_changed

if trigger:
    transcription = None
    image = None

    # Transcribe audio
    if audio_changed:
        st.session_state.last_audio = uploaded_audio
        with st.spinner("🎤 Transcribing voice..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(uploaded_audio.read())
                audio_path = tmp.name
            result = whisper_model.transcribe(audio_path)
            transcription = result["text"]

    # Load image
    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")

    # Build user text and display text
    if transcription:
        user_text = transcription
        display_text = f"🎤 {transcription}"
    elif user_input:
        user_text = user_input
        display_text = user_input
        if image is not None:
            display_text = f"{user_input} 📷"
    elif image is not None:
        user_text = "I am sending you a photo of the patient. Describe what you visually observe — skin color, lips, eyes, posture. Then ask one follow-up question."
        display_text = "📷 Photo sent"
    else:
        st.warning("Please type, upload a voice memo, or send a photo.")
        st.stop()

    # Show user message
    st.session_state.chat_display.append(("user", display_text))
    st.chat_message("user").write(display_text)

    # Get AI response
    with st.spinner("⏳ Thinking..."):
        response = get_response(user_text, image=image)

    # Show AI response
    is_emergency = "EMERGENCY" in response
    st.session_state.chat_display.append(("assistant", response))
    with st.chat_message("assistant"):
        if is_emergency:
            st.error(response)
        else:
            st.success(response)

    # TTS
    tts_file = speak(response)
    if tts_file:
        with open(tts_file, "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True)

    st.rerun()

# Disclaimer
st.markdown("""
<div style='background:#fff3cd;padding:10px;border-radius:8px;
            margin-top:16px;font-size:12px;text-align:center'>
    ⚠️ AidFirst is not a substitute for professional medical advice.
    In a life-threatening emergency, call your local emergency number immediately.
</div>
""", unsafe_allow_html=True)
