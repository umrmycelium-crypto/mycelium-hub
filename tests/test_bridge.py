import asyncio
import unittest
from unittest.mock import MagicMock, patch
from mycelium.core.bridge import IntentSynthesizer
from mycelium.core.registry import REGISTRY

class TestIntentBridge(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup a mock state
        self.state = {
            "tick": 100,
            "intent_field": 0.85,
            "ideas": [
                {"name": "vitality", "strength": 0.9, "value": 0.9},
                {"name": "coherence", "strength": 0.8, "value": 0.8},
                {"name": "action", "strength": 0.7, "value": 0.7}
            ]
        }
        # Mock the AI response to simulate a successful synthesis
        self.mock_ai_response = {
            "intent": "system.ping",
            "confidence": 0.95,
            "reason": "High coherence detected, triggering vitality pulse."
        }
        self.synthesizer = IntentSynthesizer()

    @patch("mycelium.core.registry.REGISTRY")
    async def test_successful_synthesis(self, mock_registry):
        # Setup mock registry to have system.ping
        mock_registry.__contains__.return_value = True
        mock_registry.__getitem__.return_value = MagicMock(return_value={"status": "OK"})

        # Mock the ai.ask intent in the registry
        def mock_ai_ask(payload, context):
            import json
            return {"response": json.dumps(self.mock_ai_response)}
        
        mock_registry["ai.ask"] = mock_ai_ask

        # Test synthesis
        result = await self.synthesizer.synthesize(self.state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["intent"], "system.ping")
        self.assertEqual(result["payload"]["confidence"], 0.95)

    async def test_low_confidence_rejection(self):
        # Mock the ai.ask intent to return low confidence
        def mock_ai_ask_low(payload, context):
            import json
            low_conf = {"intent": "system.ping", "confidence": 0.2, "reason": "Unsure"}
            return {"response": json.dumps(low_conf)}
        
        REGISTRY["ai.ask"] = mock_ai_ask_low

        result = await self.synthesizer.synthesize(self.state)
        self.assertIsNone(result, "Should reject low confidence synthesis")

    async def test_interval_blocking(self):
        # First call should work
        await self.synthesizer.synthesize(self.state)
        
        # Second call immediately after should return None due to interval
        self.state["tick"] = 101
        result = await self.synthesizer.synthesize(self.state)
        self.assertIsNone(result, "Should block synthesis before interval is reached")

if __name__ == "__main__":
    unittest.main()
