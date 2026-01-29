import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent import TravelAgent

console = Console()

def main():
    load_dotenv()
    console.print(Panel("[bold green]Travel Itinerary AI Agent[/bold green]\nType 'exit' to quit.", title="Welcome"))

    # Check config
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("OPENAI_API_KEY") and not os.getenv("OLLAMA_BASE_URL"):
        console.print("[bold red]WARNING:[/bold red] Please configure your .env file with API keys or Ollama URL.")

    try:
        agent = TravelAgent()
    except Exception as e:
        console.print(f"[bold red]Error initializing Agent:[/bold red] {e}")
        return

    while True:
        user_input = Prompt.ask("\n[bold cyan]Where would you like to go?[/bold cyan]")
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            console.print("[green]Goodbye![/green]")
            break
            
        if not user_input.strip():
            continue

        try:
            # 1. Understand
            with console.status("[bold yellow]Understanding your request...[/bold yellow]"):
                request_data = agent.understand_request(user_input)
            
            if request_data:
                console.print(Panel(
                    f"[bold]Destination:[/bold] {request_data.destination}\n"
                    f"[bold]Duration:[/bold] {request_data.duration_days or 'Flexible'} days\n"
                    f"[bold]Budget:[/bold] {request_data.budget}\n"
                    f"[bold]Interests:[/bold] {', '.join(request_data.interests)}",
                    title="[bold green]Plan Details[/bold green]"
                ))
                
                # 2. Plan
                confirm = Prompt.ask("Proceed with this plan?", choices=["y", "n"], default="y")
                if confirm == "y":
                    with console.status("[bold magenta]Researching & Planning... (This may take a moment)[/bold magenta]"):
                        itinerary = agent.create_itinerary(request_data)
                    
                    console.print("\n")
                    console.print(Markdown(itinerary))
                    console.print("\n[bold green]Enjoy your trip![/bold green]")
                else:
                    console.print("Okay, please refine your request.")
            else:
                console.print("[bold red]Could not understand the request.[/bold red] Please try again.")
                
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
