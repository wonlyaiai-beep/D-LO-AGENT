import asyncio
import uuid
from dlo_agent import get_response

def main():
    """D'LO AI Sales Agent — Main Loop"""
    
    print("=" * 50)
    print("  D'LO AI Sales Agent")
    print("  Humanoid AI Agents For Business")
    print("=" * 50)
    print("Type 'quit' to exit\n")
    
    # Unique session ID
    session_id = str(uuid.uuid4())
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("D'LO Agent: Allah Hafiz! 🙏")
                break
            
            # Response lo
            response = asyncio.run(get_response(session_id, user_input))
            print(f"\nD'LO Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nD'LO Agent: Allah Hafiz! 🙏")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()