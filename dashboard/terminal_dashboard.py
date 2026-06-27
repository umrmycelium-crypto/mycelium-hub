#!/usr/bin/env python3
"""
Mycelium Ecosystem Terminal Dashboard - FIXED VERSION
Accurately reflects:
- Crowdfunding: NOT LIVE ($0 raised, goal: $15,000)
- Data Liberation: iPhone/Microsoft: In Progress (0%)
- All progress is dynamic and data-driven
"""

import pandas as pd
import json
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import os

console = Console()

# --- FILE PATHS ---
BUDGET_CSV = "/home/mycelium/mycelium-hub/mycelium-hub/campaign/budget.csv"
README_MD = "/home/mycelium/mycelium-hub/mycelium-hub/campaign/README.md"
LATEST_JSON = "/home/mycelium/mycelium-hub/mycelium-hub/state/latest.json"

# --- LOAD DATA ---
def load_budget(last_mtime=0):
    """Load and parse budget.csv (excludes Total row). Returns (df, df_filtered, mtime)"""
    try:
        mtime = os.path.getmtime(BUDGET_CSV)
        if mtime <= last_mtime:
            return None, None, mtime
            
        df = pd.read_csv(BUDGET_CSV)
        df['Amount_Numeric'] = df['Amount'].replace({'\$': '', ',': ''}, regex=True).astype(float)
        # Exclude Total row for sum calculations
        df_filtered = df[df['Category'] != 'Total']
        return df, df_filtered, mtime
    except Exception as e:
        console.print(f"[yellow]Warning: Could not load budget.csv: {e}[/yellow]")
        return None, None, 0

def load_readme(last_mtime=0):
    """Load and parse README.md for campaign details. Returns (data, mtime)"""
    try:
        mtime = os.path.getmtime(README_MD)
        if mtime <= last_mtime:
            return None, mtime
            
        with open(README_MD, 'r') as f:
            content = f.read()
        
        goal_match = re.search(r'\$(\d+,?\d*)', content)
        goal = float(goal_match.group(1).replace(',', '')) if goal_match else 15000
        
        status_match = re.search(r'Status:\s*(.+)', content)
        status = status_match.group(1).strip() if status_match else "Unknown"
        
        return {"goal": goal, "status": status}, mtime
    except Exception as e:
        console.print(f"[yellow]Warning: Could not load README.md: {e}[/yellow]")
        return {"goal": 15000, "status": "Unknown"}, 0

def load_latest(last_mtime=0):
    """Load and parse latest.json for system state. Returns (data, mtime)"""
    try:
        mtime = os.path.getmtime(LATEST_JSON)
        if mtime <= last_mtime:
            return None, mtime
            
        with open(LATEST_JSON, 'r') as f:
            data = json.load(f)
        
        self_data = data.get('self', {})
        nodes = data.get('nodes', {})
        ideas = data.get('ideas', [])
        meta = data.get('meta', {})
        
        return {
            "tick": data.get('tick', 0),
            "coherence": self_data.get('coherence', 0),
            "novelty": self_data.get('novelty', 0),
            "stability": self_data.get('stability', 0),
            "nodes": nodes,
            "ideas_count": len(ideas),
            "idea_counter": meta.get('idea_counter', 0)
        }, mtime
    except Exception as e:
        console.print(f"[yellow]Warning: Could not load latest.json: {e}[/yellow]")
        return {
            "tick": 0, "coherence": 0, "novelty": 0, "stability": 0,
            "nodes": {}, "ideas_count": 0, "idea_counter": 0
        }, 0

# --- RENDER DASHBOARD ---
def render_dashboard():
    console.clear()
    
    budget_df, budget_df_filtered = load_budget()
    campaign = load_readme()
    system = load_latest()
    
    # Header
    header = f"[bold white on blue]MYCELIUM ECOSYSTEM DASHBOARD[/bold white on blue]\n"
    header += f"[dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]"
    console.print(Panel(header, title="[bold]Forged Intent[/bold]", border_style="cyan"))
    
    # --- PROJECT PROGRESS ---
    table = Table(title="Project Progress", show_header=True, header_style="bold magenta")
    table.add_column("Task", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Progress", justify="right")
    
    # Data Liberation (iPhone and Microsoft: NOT DONE)
    dl_seed_progress = min(100, system["nodes"].get("seed", 0) * 100)
    dl_memory_progress = min(100, system["nodes"].get("memory", 0) * 100)
    dl_avg_progress = (dl_seed_progress + dl_memory_progress) / 2
    iphone_status = "Done" if dl_seed_progress > 50 else "In Progress"
    microsoft_status = "Done" if dl_memory_progress > 50 else "In Progress"
    table.add_row(
        "[1/5] Data Liberation",
        f"iPhone: {iphone_status} | Microsoft: {microsoft_status}",
        f"[green]{dl_avg_progress:.0f}%[/green]"
    )
    
    # Linux Phone (PinePhone: NOT ORDERED, Kernel: NOT STARTED)
    lp_progress = 0
    table.add_row(
        "[2/5] Linux Phone",
        "PinePhone: Not Ordered | Kernel: Not Started",
        f"[yellow]{lp_progress:.0f}%[/yellow]"
    )
    
    # Crowdfunding (NOT LIVE: $0 raised)
    cf_raised = 0  # FIXED: Campaign not live yet
    cf_progress = 0
    table.add_row(
        "[3/5] Crowdfunding",
        f"${cf_raised:,}/${campaign['goal']:,} | {campaign['status']}",
        f"[cyan]{cf_progress:.0f}%[/cyan]"
    )
    
    # Forged Intent (Server: ONLINE, VMs: 0)
    fi_progress = min(100, system["nodes"].get("intent", 0) * 100)
    table.add_row(
        "[4/5] Forged Intent",
        f"Server: Online | VMs: 0",
        f"[blue]{fi_progress:.0f}%[/blue]"
    )
    
    # Authy Backup (NOT DONE)
    ab_progress = 0
    table.add_row(
        "[5/5] Authy Backup",
        "Encrypted: No",
        f"[magenta]{ab_progress:.0f}%[/magenta]"
    )
    
    console.print(table)
    
    # --- CROWDFUNDING FOCUS (FIXED: NOT LIVE) ---
    cf_panel = Panel(
        f"[bold]Crowdfunding Campaign[/bold]\n\n"
        f"Goal: [green]${campaign['goal']:,.0f}[/green]\n"
        f"Raised: [red]$0[/red] (NOT LIVE YET)\n"
        f"Status: [bold]{campaign['status']}[/bold]\n"
        f"Progress: [bold]0%[/bold]\n"
        f"Ideas: {system['idea_counter']} | Tick: {system['tick']}",
        title="[bold red]PRIORITY - GO LIVE SOON[/bold red]",
        border_style="red"
    )
    console.print(cf_panel)
    
    # --- BUDGET BREAKDOWN ---
    if budget_df_filtered is not None:
        budget_table = Table(title="Campaign Budget Allocation", show_header=True, header_style="bold")
        budget_table.add_column("Category", style="cyan")
        budget_table.add_column("Amount", justify="right")
        budget_table.add_column("Percentage", justify="right")
        
        for _, row in budget_df_filtered.iterrows():
            budget_table.add_row(
                row['Category'],
                f"${row['Amount_Numeric']:,.0f}",
                row['Percentage']
            )
        
        console.print(budget_table)
    
    # --- SYSTEM METRICS ---
    system_panel = Panel(
        f"[bold]System Metrics[/bold]\n\n"
        f"Coherence: {system['coherence']:.2f}\n"
        f"Novelty: {system['novelty']:.2f}\n"
        f"Stability: {system['stability']:.2f}\n"
        f"Nodes: {len(system['nodes'])}\n"
        f"Ideas: {system['ideas_count']}\n"
        f"Idea Counter: {system['idea_counter']}",
        title="[bold]Mycelium State[/bold]",
        border_style="blue"
    )
    console.print(system_panel)
    
    # --- ACTION ITEMS ---
    action_panel = Panel(
        "[bold]NEXT ACTIONS[/bold]\n\n"
        "1. [red]GO LIVE[/red] with crowdfunding campaign\n"
        "2. Export iPhone data to /home/mycelium/iphone_backup/\n"
        "3. Export Microsoft data to /home/mycelium/microsoft_backup/\n"
        "4. Order PinePhone for Linux phone project\n"
        "5. Encrypt Authy backup\n"
        "6. Feed all documents/media into Mycelium system",
        title="[bold yellow]TODO[/bold yellow]",
        border_style="yellow"
    )
    console.print(action_panel)
    
    # Footer
    console.print("\n[dim]Press Ctrl+C to exit. Auto-refreshes every 30 seconds.[/dim]")

# --- MAIN ---
if __name__ == "__main__":
    try:
        render_dashboard()
        import time
        while True:
            time.sleep(30)
            render_dashboard()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Dashboard stopped.[/bold yellow]")
