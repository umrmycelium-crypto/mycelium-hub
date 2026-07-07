import requests
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GalaxyWolfSim")

SERVER_URL = "http://localhost:7000"

def simulate_interaction(text):
    logger.info(f"--- SIMULATING DEVICE INPUT: '{text}' ---")
    
    # 1. Simulate the device detecting the wake-word and sending the audio/text to the server
    # In a real scenario, the device would send a POST request to /ai/<prompt>
    try:
        response = requests.get(f"{SERVER_URL}/ai/{text}", timeout=10)
        result = response.json()
        
        if result.get("type") == "intent":
            logger.info(f"System recognized intent: {result.get('intent')}")
            logger.info(f"Response: {result.get('response')}")
        elif result.get("type") == "conversation":
            logger.info(f"Response: {result.get('response')}")
        else:
            logger.info(f"Unexpected response: {result}")
            
    except Exception as e:
        logger.error(f"Connection failed: {e}")

if __name__ == "__main__":
    # Scenario 1: Wake-word + Device Action
    simulate_interaction("Galaxy Wolf! Organize my apps by color!")
    
    time.sleep(1)
    
    # Scenario 2: Wake-word + Creative Direction
    simulate_interaction("Galaxy Wolf! I have an idea for a Minecraft kaiju short. Check the trends for me!")
