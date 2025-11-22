import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from system import HotelSystem
from agent import HospitalityAI

def main():
    console = Console()
    system = HotelSystem()
    ai = HospitalityAI(system)

    console.print(Panel.fit("Welcome to HOSPITALITY-AI System", style="bold blue"))

    # Role Selection
    role = Prompt.ask("Select Role", choices=["guest", "staff", "manager"], default="guest")
    name = "Guest"
    if role == "guest":
        name = Prompt.ask("What is your name?")
        # Auto-create guest profile for demo
        system.create_guest(name)

    console.print(f"[green]System initialized for {role.upper()} mode.[/green]")
    console.print("Type 'exit' to quit.\n")

    while True:
        user_input = Prompt.ask(f"[{role}] >")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response = ai.process_input(user_input, user_role=role, user_name=name)
        console.print(f"[bold blue]AI:[/bold blue] {response}\n")

if __name__ == "__main__":
    main()
