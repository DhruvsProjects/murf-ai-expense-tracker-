import speech_recognition as sr
import google.generativeai as genai
from murf import Murf
import pyaudio
import json
import os
import time

# ==========================================
# CONFIGURATION
# ==========================================


GEMINI_API_KEY = "YOUR_API_KEY"
MURF_API_KEY = "YOUR_API_KEY"

# Murf Settings
MURF_VOICE_ID = "en-IN-nikhil" # You can change this voice ID
SAMPLE_RATE = 24000             # Standard for Murf Falcon
HISTORY_FILE = "expense_history.json" # Where your data lives

# ==========================================
# MEMORY (FILE OPERATIONS)
# ==========================================

def load_history():
    """Loads past expenses from the JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_expense(expense_item):
    """Saves a new expense to the JSON file."""
    history = load_history()
    history.append(expense_item)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

# ==========================================
# CORE FUNCTIONS
# ==========================================

def listen_to_user():
    """Records audio from microphone and converts to text."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nListening... (Speak now!)")
        # Adjust for background noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # Listen (waits up to 5 seconds for silence)
            audio = recognizer.listen(source, timeout=5)
            print("Transcribing...")
            
            # Use Google's free speech recognition
            text = recognizer.recognize_google(audio)
            print(f"You said: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected.. please try again")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Connection error: {e}")
            return None

def smart_analyze(text):
    """Sends user text + history to Gemini to decide on an action."""
    print("Expense Tracker is analyzing...")
    
    # 1. Load context (memory)
    history = load_history()
    
    # 2. Setup Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # 3. The Prompt
    prompt = f"""
    You are an intelligent expense assistant.
    
    CURRENT DATA: {json.dumps(history)}
    USER INPUT: "{text}"
    
    INSTRUCTIONS:
    1. If the user is ADDING a new expense:
       Return JSON: {{"action": "add", "data": {{"item": "string", "amount": number, "currency": "INR", "category": "string", "date": "DD-MM-YYYY"}}}}
    
    2. If the user is ASKING a question (summary, total, specific item search):
       Analyze the CURRENT DATA and calculate the answer yourself.
       Return JSON: {{"action": "reply", "message": "Your natural language answer here."}}

    3. If unrelated/error:
       Return JSON: {{"action": "error"}}

    4. If the user is asking to clear data:
        Delete all the content from expense_history.json   
       
    RETURN ONLY RAW JSON. NO MARKDOWN.
    """
    
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"Logic Error: {e}")
        return None

def speak_live(text):
    
    print(f"🗣️ Murf Speaking: '{text}'")
    
    try:
        # 1. Initialize Clients
        client = Murf(api_key=MURF_API_KEY)
        p = pyaudio.PyAudio()
        
        # 2. Open Speaker Stream
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            output=True
        )

        # 3. Request Stream from Murf (Falcon Model)
        audio_stream = client.text_to_speech.stream(
            text=text,
            voice_id=MURF_VOICE_ID,
            model="FALCON",
            format="PCM",
            sample_rate=SAMPLE_RATE
        )

        # 4. Stream Playback Loop
        for chunk in audio_stream:
            if chunk:
                stream.write(chunk)

        # 5. Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    except Exception as e:
        print(f"Streaming Error: {e}")

# ==========================================
# MAIN APP LOOP
# ==========================================

def main():
    print("Expense Tracker Started.")
    
    while True:
        # 1. Get Input
        text = listen_to_user()
        
        if text:
            # Check for exit command
            if text.lower() in ["stop", "exit", "quit", "bye", "goodbye"]:
                print("Exiting...")
                speak_live("Goodbye!")
                break

            # 2. Analyze (with memory)
            result = smart_analyze(text)
            
            if not result:
                speak_live("I'm sorry, I had trouble processing that request.")
                continue

            action = result.get("action")

            # 3. Take Action
            if action == "add":
                # Add to history
                data = result.get("data")
                save_expense(data)
                print(f"Saved: {data['item']} (₹{data['amount']})")
                
                # Confirm to user
                speak_live(f"I've logged {data['item']} for {data['amount']} rupees.")

            elif action == "reply":
                # Just answer the question
                message = result.get("message")
                print(f"Answer: {message}")
                speak_live(message)

            else:
                speak_live("I didn't quite get that.")
        
        # Small pause between loops to prevent instant re-triggering
        time.sleep(1)

if __name__ == "__main__":
    main()