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
from utils.formatting import format_itinerary_to_markdown, export_to_pdf
from validation import validate_itinerary_activities, format_validation_report

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
            
            if not request_data:
                console.print("[bold red]Could not understand the request.[/bold red]")
                console.print("💡 [yellow]Tip:[/yellow] Try providing more details like destination, duration, and interests.")
                console.print("   Example: 'Plan a 3-day trip to Paris for a couple interested in art and food. Medium budget.'")
                continue
            
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
                    
                    if not itinerary:
                        console.print("[bold red]Failed to generate itinerary.[/bold red]")
                        console.print("💡 [yellow]Possible reasons:[/yellow]")
                        console.print("   • Network connectivity issues")
                        console.print("   • API rate limits reached")
                        console.print("   • Invalid API configuration")
                        console.print("\n[cyan]Please try again in a moment or check your API settings.[/cyan]")
                        continue
                    
                    formatted_itinerary = format_itinerary_to_markdown(itinerary)
                    console.print("\n")
                    console.print(Markdown(formatted_itinerary))
                    
                    # 2.5. Optional Activity Validation
                    validate_prompt = Prompt.ask("\n[cyan]Validate activities (verify places exist)?[/cyan]", choices=["y", "n"], default="n")
                    if validate_prompt == "y":
                        with console.status("[bold yellow]Validating activities...[/bold yellow]"):
                            validation_results = validate_itinerary_activities(itinerary, sample_validation=True)
                        
                        if validation_results['warnings']:
                            validation_report = format_validation_report(validation_results)
                            console.print("\n")
                            console.print(Markdown(validation_report))
                        else:
                            console.print("\n[bold green]✓ All sampled activities verified successfully![/bold green]")
                    
                    console.print("\n[bold green]Enjoy your trip![/bold green]")
                    
                    # 3. Export
                    save_confirm = Prompt.ask("\nSave itinerary to file?", choices=["y", "n"], default="y")
                    if save_confirm == "y":
                        export_format = Prompt.ask("Choose format", choices=["markdown", "pdf"], default="markdown")
                        
                        base_filename = f"trip_to_{request_data.destination.replace(' ', '_').lower()}"
                        output_dir = "output"
                        os.makedirs(output_dir, exist_ok=True)
                        
                        if export_format == "markdown":
                            filepath = os.path.join(output_dir, f"{base_filename}.md")
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write(formatted_itinerary)
                        else:
                            filepath = os.path.join(output_dir, f"{base_filename}.pdf")
                            success = export_to_pdf(formatted_itinerary, filepath)
                            if not success:
                                console.print("[bold red]Failed to generate PDF.[/bold red]")
                                continue
                                
                        console.print(f"[bold green]Itinerary saved to {filepath}[/bold green]")

                else:
                    console.print("Okay, please refine your request.")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user.[/yellow]")
            continue
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
            console.print("\n💡 [yellow]Troubleshooting tips:[/yellow]")
            console.print("   • Check your internet connection")
            console.print("   • Verify your .env file has correct API keys")
            console.print("   • Ensure the selected model is available")
            console.print("   • Check if you've exceeded API rate limits")

if __name__ == "__main__":
    main()
