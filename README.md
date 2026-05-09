# AidFirst 
### Multilingual Medical First-Response Assistant

AidFirst helps untrained caregivers understand medical emergencies — in any language, on any phone.

Built for the [Gemma 4 Good Hackathon](https://www.kaggle.com/competitions/gemma-4-good-hackathon) by a second-year engineering student from Pune, India.

---

## The Problem

In India and across the developing world, medical emergencies happen far from hospitals, far from doctors, and far from anyone who speaks the right language. A caregiver — a family member, a neighbor, an ASHA worker — finds themselves next to someone who is sick or unconscious. They don't know what's wrong. They can't explain it in medical terms. And the person who is sick can't explain it either.

Nothing exists to help that person in that moment. Until now.

---

## What AidFirst Does

AidFirst is a voice-first, multilingual medical assessment tool that:

- **Understands any input** — voice memo, photo, or typed text
- **Speaks any language** — Hindi, English, Hinglish, or mixed
- **Asks intelligent follow-up questions** to understand the situation
- **Assesses seriousness** — Monitor, See a Doctor, or Emergency
- **Gives clear instructions** in the caregiver's own language
- **Works offline** — runs entirely on-device using Gemma 4 E4B

It does not diagnose. It helps untrained people understand what is happening and what to do next.

---

## Why I Built This

My grandfather passed away two months ago. He was 85, had Parkinson's, and had suffered multiple brain strokes. After six weeks in hospital he was brought home, completely dependent on a caregiver.

One night he started coughing. His breathing became gritty and labored. The caregiver didn't recognize the signs. We trusted her when she said everything was okay. He passed away that night.

I keep thinking — if someone had known what to look for, maybe something could have been done. AidFirst is my small effort to make sure that moment of helplessness has somewhere to turn.

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
- Audio reasoning
- Agentic follow-up question generation

---

## How to Run

1. Open the notebook on Kaggle
2. Enable GPU: Settings → Accelerator → T4 GPU
3. Run Cell 1: Install dependencies
4. Run Cell 2: Load Gemma 4 E4B model
5. Run Cell 3: Launch AidFirst UI
6. Type, upload a voice memo, or send a photo

**Requirements:**
- Kaggle account (free)
- Internet connection for first model download
- GPU accelerator enabled

---

## Demo

[Watch the demo video](#) ← add YouTube link on demo day

---

## Hackathon Track

Submitted under the **Health** track of the Gemma 4 Good Hackathon.

---

*Built with Gemma 4 by Google DeepMind*
