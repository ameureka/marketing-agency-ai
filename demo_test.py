#!/usr/bin/env python3
"""
Demo script to test the Marketing Agency functionality
"""

import asyncio
import textwrap
from google.adk.runners import InMemoryRunner
from marketing_agency.agent import root_agent
from google.genai.types import Part, UserContent
import dotenv

# Load environment variables
dotenv.load_dotenv()

async def test_marketing_agency():
    """Test the marketing agency with a bakery business example."""
    
    user_input = textwrap.dedent(
        """
        I want to start a bakery business called "Sweet Dreams Bakery". 
        We specialize in custom wedding cakes, artisanal breads, and gourmet pastries.
        Our target market is upscale customers who value quality and craftsmanship.
        Can you help me create a complete marketing package including:
        1. Domain name suggestions
        2. Website design
        3. Marketing strategy
        4. Logo design
        """
    ).strip()

    print("🍰 Testing Marketing Agency with Sweet Dreams Bakery...")
    print("=" * 60)
    print(f"Input: {user_input}")
    print("=" * 60)
    
    try:
        runner = InMemoryRunner(agent=root_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="demo_user"
        )
        
        content = UserContent(parts=[Part(text=user_input)])
        response_text = ""
        
        print("🤖 Marketing Agency is processing your request...")
        print("⏳ This may take a few moments...\n")
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response_text = event.content.parts[0].text
                print(f"📝 Response chunk received: {len(response_text)} characters")
        
        print("\n" + "=" * 60)
        print("🎉 MARKETING AGENCY RESPONSE:")
        print("=" * 60)
        print(response_text)
        print("=" * 60)
        print("✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting Marketing Agency Demo...")
    asyncio.run(test_marketing_agency())