from mycelium.core.bootstrap_kernel import bootstrap
from mycelium.core.router import route
from mycelium.core.compiler import IntentCompiler

# Initialize Rich Console
console = Console()

def grow_mycelium():
    """
    Generates a procedural ASCII mycelium growth effect.
    """
    chars = ['/', '\\', '|', '-', ' ', ' ', ' ', ' ', ' ', ' ']
    width = 40
    for i in range(3):
        line = ""
        for _ in range(width):
            line += random.choice(chars)
        console.print(f"  [dim white]{line}[/dim white]")
        time.sleep(0.1)

def print_header():
    """Prints a stylized Mycelium Brain header."""
    header_text = Text("🧠 MYCELIUM BRAIN", style="bold magenta")
    header_text.append("\nDistributed Cognitive Interface v2", style="italic cyan")
    
    console.print(
        Panel(
            Align.center(header_text),
            border_style="magenta",
            title="[bold white]System Online[/bold white]",
            subtitle="Forged Intent | The Studio | VeinWeave"
        )
    )

def main():
    # Initialize the kernel
    state = bootstrap()
    
    # Clear screen and show identity
    console.clear()
    print_header()
    
    grow_mycelium()
    
    console.print(f"\n[bold white]Status:[/bold white] {state.get('status', 'Unknown')} | [bold white]Registry:[/bold white] {state.get('registry_size', 0)} handlers")
    console.print("[italic white]Ready for your commands. Type 'exit' to quit.\n[/italic white]")

    while True:
        try:
            raw = Prompt.ask("[bold cyan]mshell> [/bold cyan]").strip()
            
            if raw.lower() in ["exit", "quit"]:
                console.print("[bold red]Shutting down shell... Goodbye.[/bold red]")
                break
            if not raw:
                continue

            # Visual growth before response
            console.print("🌱", end=" ")
            for _ in range(3):
                console.print(".", end=" ")
                time.sleep(0.1)
            console.print(" ")

            intent = IntentCompiler.compile(raw)
            
            with console.status("[bold yellow]Brain is thinking...[/bold yellow]"):
                result = route(intent)

            if isinstance(result, dict):
                if "response" in result:
                    response_text = result['response']
                    if "**" in response_text or "#" in response_text or "`" in response_text:
                        console.print(Panel(Markdown(response_text), border_style="blue", title="Mycelium Brain"))
                    else:
                        console.print(f"\n[bold magenta]🤖 Brain:[/bold magenta] [white]{response_text}[/white]\n")
                elif "result" in result:
                    console.print(f"\n[bold green]✅ Result:[/bold green] [white]{result['result']}[/white]\n")
                elif result.get("status") == "NO_HANDLER":
                    console.print(f"\n[bold yellow]⚠️  No specific handler for {result.get('intent')}, but I'm adapting...[/bold yellow]\n")
                else:
                    console.print(f"\n[bold blue]📦 Data:[/bold blue] {result}\n")
            else:
                console.print(f"\n{result}\n")

        except EOFError:
            break
        except Exception as e:
            console.print(f"\n[bold red]❌ ERROR: {e}[/bold red]\n")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
