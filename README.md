# AidFirst 🏥
### Multilingual Medical First-Response Assistant

AidFirst helps untrained caregivers understand medical emergencies — in any language, on any phone, without internet.

Built for the [Gemma 4 Good Hackathon](https://www.kaggle.com/competitions/gemma-4-good-hackathon) by a second-year engineering student.

---

## The Problem

Across the world — in rural villages, remote communities, underserved neighborhoods — medical emergencies happen far from doctors and far from anyone who speaks the right language. The person closest to the crisis is almost always untrained. A family member. A neighbor. A community health worker. They don't know what to look for. They can't explain what they're seeing. And in a panic, they have nothing to guide them.

This is not a rare edge case. This is everyday life for the majority of the world.

---

## What AidFirst Does

AidFirst is a voice-first, multilingual medical assessment tool that:

- **Understands any input** — voice memo, photo, or typed text
- **Speaks any language** — understands 140+ languages, responds in Hindi or English
- **Asks intelligent follow-up questions** to understand the situation
- **Assesses seriousness** — Monitor, See a Doctor, or Emergency
- **Gives clear instructions** in the caregiver's own language
- **Works offline** — runs entirely on-device using Gemma 4 E4B

It does not diagnose. It does not replace a doctor. It fills the gap between "something is wrong" and "I know what to do next."

---

## Why I Built This

My grandfather passed away two months ago. He was 85, had Parkinson's, and had suffered multiple brain strokes. One night his breathing became gritty and labored. The caregiver didn't recognize the signs. She told us everything was okay. We believed her. He passed away that night.

We weren't negligent. We just didn't know. Not knowing made us reluctant to act. AidFirst exists because that reluctance cost us everything.

---

## Technology

| Component | Technology |
|---|---|
| Core AI | Google Gemma 4 E4B (on-device) |
| Speech to Text | OpenAI Whisper |
| Text to Speech | gTTS (bilingual) |
| UI | IPython Widgets |
| Platform | Kaggle Notebooks (free GPU) |

**Gemma 4 capabilities used:**
- Multilingual understanding (140+ languages)
- Vision input (photo analysis)
- Audio input via Whisper pipeline
- Agentic follow-up question generation
- On-device inference — no cloud dependency

---

## How to Run

1. Open the notebook on Kaggle
2. Enable GPU: Settings → Accelerator → T4 GPU
3. Run Cell 1: Install dependencies
4. Run Cell 2: Load Gemma 4 E4B model
5. Run Cell 3: Launch AidFirst UI
6. Type a description, upload a voice memo, or send a photo

---

## Demo

[Watch the demo video](#) ← updated after demo day

---

## Limitations

- Response time is 15-20 seconds on free GPU — production would need edge deployment
- System prompt currently tuned for Hindi and English
- Accuracy depends on the caregiver's description
- Prototype uses file upload for audio and photo — production would use live camera and microphone

---

## Future Scope

- Android app with fully offline on-device inference via Ollama
- Expansion to regional languages — Marathi, Tamil, Bengali, Swahili, Spanish, Arabic
- One-tap emergency services integration
- Visual symptom cards for non-verbal patients
- Fine-tuning on real medical triage conversations

---

## Hackathon

Submitted to the **Gemma 4 Good Hackathon** under the Health and Impact tracks.

---

*Built with Gemma 4 by Google DeepMind*
