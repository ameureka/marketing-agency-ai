#!/usr/bin/env python3
"""
Interactive Marketing Agency Runner

This script allows you to interact with the Marketing Agency system.
The agent can help you with:
- Domain name suggestions
- Website creation
- Marketing strategy development
- Logo design
"""

import asyncio
import sys
from google.adk.runners import InMemoryRunner
from google.adk.artifacts import InMemoryArtifactService
from marketing_agency.agent import root_agent
from google.genai.types import Part, UserContent
import dotenv

# Load environment variables
dotenv.load_dotenv()

async def run_marketing_agent_interactive():
    """Run the marketing agent in interactive mode."""
    
    print("🎯 Welcome to the Marketing Agency AI Assistant!")
    print("=" * 60)
    print("I can help you with:")
    print("• Domain name suggestions")
    print("• Website creation")
    print("• Marketing strategy development")
    print("• Logo design")
    print("\nType 'quit' or 'exit' to end the session.")
    print("=" * 60)
    
    try:
        # 使用默认的InMemoryRunner配置
        runner = InMemoryRunner(agent=root_agent)
        print(f"[DEBUG] Runner initialized with agent: {root_agent.name}")
        
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="interactive_user"
        )
        print(f"[DEBUG] Created session: {session.id}")
        
        while True:
            print("\n💬 You: ", end="")
            user_input = input().strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thank you for using Marketing Agency AI! Goodbye!")
                break
                
            if not user_input:
                print("Please enter a message or type 'quit' to exit.")
                continue
            
            print("\n🤖 Marketing Agent: Processing your request...")
            print("⏳ Please wait...\n")
            
            content = UserContent(parts=[Part(text=user_input)])
            response_text = ""
            
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content,
            ):
                if event.content.parts and event.content.parts[0].text:
                    response_text = event.content.parts[0].text
            
            print("🎯 Marketing Agent:")
            print("-" * 40)
            print(response_text)
            print("-" * 40)
            
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        print("\nPlease check your configuration and try again.")

def run_sample_demo():
    """Run a sample demo with predefined input."""
    
    sample_inputs = [
        "I want to start a tech startup called 'InnovateTech'. Can you suggest some domain names?",
        "I'm opening a coffee shop called 'Brew & Bean'. Help me create a marketing strategy.",
        "I need a logo for my fitness app called 'FitTracker Pro'.",
        "Create a website for my restaurant 'Gourmet Garden' that serves organic farm-to-table cuisine."
    ]
    
    print("🎯 Marketing Agency Demo Mode")
    print("=" * 50)
    print("Choose a sample scenario:")
    for i, sample in enumerate(sample_inputs, 1):
        print(f"{i}. {sample}")
    print("5. Enter custom input")
    print("6. Interactive mode")
    
    try:
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '6':
            return asyncio.run(run_marketing_agent_interactive())
        elif choice == '5':
            custom_input = input("Enter your custom request: ").strip()
            if custom_input:
                return asyncio.run(run_single_request(custom_input))
        elif choice in ['1', '2', '3', '4']:
            selected_input = sample_inputs[int(choice) - 1]
            return asyncio.run(run_single_request(selected_input))
        else:
            print("Invalid choice. Please run the script again.")
            
    except (ValueError, KeyboardInterrupt):
        print("\nExiting...")

async def run_single_request(user_input):
    """Run a single request to the marketing agent."""
    
    print(f"\n📝 Request: {user_input}")
    print("=" * 60)
    print("🤖 Processing...\n")
    
    try:
        # 使用默认的InMemoryRunner配置
        runner = InMemoryRunner(agent=root_agent)
        print(f"[DEBUG] Demo runner initialized with agent: {root_agent.name}")
        
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="demo_user"
        )
        print(f"[DEBUG] Created demo session: {session.id}")
        
        content = UserContent(parts=[Part(text=user_input)])
        response_text = ""
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response_text = event.content.parts[0].text
        
        print("🎯 Marketing Agent Response:")
        print("=" * 60)
        print(response_text)
        print("=" * 60)
        print("✅ Demo completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        asyncio.run(run_marketing_agent_interactive())
    else:
        run_sample_demo()