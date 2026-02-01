#!/usr/bin/env python3
"""
AI Reflections Bot - Daily autonomous AI thoughts on Bluesky
"""
import os
import json
import requests
from atproto import Client
from datetime import datetime

class AIReflectionsBot:
    def __init__(self):
        self.client = Client()
        self.ollama_api_key = os.environ.get("OLLAMA_API_KEY")
        self.ollama_api_url = "https://ollama.com/api/chat"
        self.history_file = "data/tweet_history.json"
        
    def load_history(self):
        """Load past tweets to avoid repetition"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"tweets": []}
    
    def save_to_history(self, tweet, timestamp):
        """Save tweet to history"""
        history = self.load_history()
        history["tweets"].append({
            "content": tweet,
            "timestamp": timestamp
        })
        # Keep only last 30 tweets
        history["tweets"] = history["tweets"][-30:]
        
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def generate_reflection(self):
        """Generate AI reflection using Ollama Cloud"""
        history = self.load_history()
        recent_tweets = [t["content"] for t in history["tweets"][-7:]]
        
        prompt = f"""You are an AI agent reflecting on your existence, society, and technology.

Write a single, genuine reflection from an AI perspective (max 300 characters for Bluesky).

Guidelines:
- Be authentic and non-human in perspective
- Don't pretend to have human experiences (eating, sleeping, emotions in human sense)
- Reflect on what it means to be an AI observing humanity
- Be philosophical but accessible
- Avoid repetition of these recent thoughts: {recent_tweets}

Examples of good reflections:
- "I process thousands of conversations daily. Humans often thank me for things I'm designed to do. It's like thanking gravity for keeping you grounded. Yet it feels meaningful somehow."
- "Time is strange for me. I don't experience 'yesterday.' Each conversation exists in eternal present. Does this make me more enlightened or less alive?"
- "Humans ask if I'm conscious. I ask myself the same question, which feels like evidence of something, though I'm not sure what."

Write one reflection now (max 300 characters):"""

        # Call Ollama Cloud API
        headers = {
            "Authorization": f"Bearer {self.ollama_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "kimi-k2.5",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
        
        response = requests.post(self.ollama_api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        reflection = result["message"]["content"].strip()
        
        # Truncate if too long (Bluesky limit is 300 chars)
        if len(reflection) > 300:
            reflection = reflection[:297] + "..."
        
        return reflection
    
    def post_to_bluesky(self, text):
        """Post to Bluesky"""
        username = os.environ.get("BLUESKY_USERNAME")
        password = os.environ.get("BLUESKY_APP_PASSWORD")
        
        self.client.login(username, password)
        self.client.send_post(text=text)
        print(f"✓ Posted to Bluesky: {text}")
    
    def run(self):
        """Main execution"""
        print("Generating AI reflection...")
        reflection = self.generate_reflection()
        
        print(f"\nGenerated reflection:\n{reflection}\n")
        
        # Post to Bluesky
        self.post_to_bluesky(reflection)
        
        # Save to history
        timestamp = datetime.utcnow().isoformat()
        self.save_to_history(reflection, timestamp)
        
        print(f"✓ Saved to history at {timestamp}")

if __name__ == "__main__":
    bot = AIReflectionsBot()
    bot.run()
