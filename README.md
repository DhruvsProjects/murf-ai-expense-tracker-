# murf-ai-expense-tracker-
This is a voice-activated tool designed to make tracking your finances as easy as having a conversation. Instead of forcing you to use specific keywords or rigid commands, it uses Google Gemini to understand natural speech. It also uses murf.ai to speak back to you in a natural tone.

AI Voice Expense Tracker

This is a voice-activated tool designed to make tracking your finances as easy as having a conversation. Instead of forcing you to use specific keywords or rigid commands, it uses Google Gemini to understand natural speech. You can just say what you bought and how much it cost, and the system handles the parsing, math, and categorization for you. It then uses Murf.ai to confirm the action back to you with a realistic voice, making the interaction feel seamless and interactive.

Features

Voice-to-JSON: Uses Google Speech Recognition to convert spoken audio to text.

Intelligent Parsing: Uses Gemini 2.0 Flash to extract structured data (Item, Amount, Category) from casual speech.

Smart Queries: Ask questions like "How much did I spend on food?" and Gemini will analyze your transaction history to give a calculated answer.

Streaming Voice Output: Uses Murf.ai Falcon model for ultra-low latency, realistic voice responses (no MP3 files generated).

Persistent Memory: Automatically saves all transactions to expense_history.json.

Prerequisites

You will need Python 3.9+ and the following free API keys:

Google Gemini API Key: Get it here (Free Tier available)

Murf.ai API Key: Get it here (Free Trial available)

Installation




Install system dependencies (for PyAudio):

Mac: ```brew install portaudio```

Linux (Ubuntu): ```sudo apt-get install python3-pyaudio portaudio19-dev```

Windows: Usually pre-installed, but if errors occur, install the specific .whl file for PyAudio.

Install Python libraries:

```pip install speechrecognition google-generativeai murf pyaudio```


Configuration

Open expense_tracker_complete.py and paste your API keys at the top:

# ==========================================
# CONFIGURATION
# ==========================================

GEMINI_API_KEY = "PASTE_YOUR_GEMINI_KEY_HERE"
MURF_API_KEY = "PASTE_YOUR_MURF_KEY_HERE"

# Optional: Change Voice ID or Currency
MURF_VOICE_ID = "en-US-natalie" 
HISTORY_FILE = "expense_history.json"


How to Use

Run the script:

```python expense_tracker_complete.py```


The app will start listening immediately. Speak naturally!

Example Commands

Adding Expenses:

"I bought a coffee for 250 rupees."

"Add a taxi ride for 500 rupees to transport."

"Spent 1200 rupees on groceries."

Asking Questions:

"How much have I spent in total?"

"What is my total spending on food?"

"List my recent transactions."

Exiting:

"Stop" or "Goodbye"

Data Storage

Your data is stored locally in expense_history.json. It looks like this:
```
[
  {
    "item": "coffee",
    "amount": 250,
    "currency": "INR",
    "category": "food",
    "date": "2023-10-27"
  }
]
```

Troubleshooting

PyAudio Error: If you can't install PyAudio, ensure you have installed portaudio via Homebrew (Mac) or apt (Linux).

Murf Error: If the voice stops working, check your Murf.ai dashboard. The free trial has a limit on voice generation time.

Microphone Issues: Ensure your default microphone is set correctly in your system settings.

License

This project is open-source and available under the MIT License.
