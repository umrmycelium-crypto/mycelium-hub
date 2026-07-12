from threading import Thread
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.text import Text
from rich.align import Align

from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.events import RAW_INPUT
from mycelium.core.workers.shell_workers import bootstrap_shell_workers
from mycelium.core.workers.sensor_workers import bootstrap_sensor_workers
from mycelium.agents.executive_agent import executive_agent_personal

# Initialize Rich Console
console = Console()

def print_header():
    """Prints a stylized Mycelium Brain header."""
    header_text = Text("🧠 MYCELIUM BRAIN", style="bold magenta")
    header_text.append("
Distributed Cognitive Interface v2", style="italic cyan")
    
    console.print(
        Panel(
            Align.center(header_text),
            border_style="magenta",
            title="[bold white]System Online[/bold white]",
            subtitle="Forged Intent | The Studio | VeinWeave"
        )
    )

def input_collector():
    """
    Modernized input loop using Rich.
    Directly invokes the Executive Agent for a 'Chat' experience.
    """
    while True:
        try:
            raw = Prompt.ask("[bold cyan]mshell> [/bold cyan]")
            
            if raw.strip().lower() == "exit":
                console.print("[bold red]Exiting Mycelium Shell...[/bold red]")
                break

            if not raw.strip():
                continue

            # Display user input immediately
            console.print(f"
[bold magenta]➜ You:[/bold magenta] [white]{raw}[/white]")

            # Use the Executive Agent to process the request
            # We run this in a separate thread or just call it if the agent's run is efficient
            # For the best 'chat' feel, we call it and print the result
            
            with console.status("[bold yellow]Brain is thinking...[/bold yellow]"):
                response = executive_agent_personal.run(raw)
            
            # Render response
            if "**" in response or "#" in response or "`" in response:
                console.print(Panel(Markdown(response), border_style="blue", title="Mycelium Brain"))
            else:
                console.print(f"
[bold magenta]➜ Brain:[/bold magenta] [white]{response}[/white]")
            
            console.print("
")
            
        except EOFError:
            break
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")

def main():
    # Clear screen for a clean start
    console.clear()
    print_header()
    console.print("[italic white]Type 'exit' to quit. Your personal brain is now listening...[/italic white]
")

    # Sit the workers at the table
    bootstrap_shell_workers()
    bootstrap_sensor_workers()

    # Start the input listener
    # We no longer need a separate thread for collector if we want a synchronous chat feel,
    # but we keep it for compatibility with the event bus if other workers need to print.
    input_collector()

if __name__ == "__main__":
    main()
