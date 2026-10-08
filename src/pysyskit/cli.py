"""Command-line interface for PySysKit."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from pysyskit.modules.filesystem import get_disk_usage
from pysyskit.modules.logs import analyze_logs
from pysyskit.modules.network import get_network_info
from pysyskit.modules.process import get_process_list
from pysyskit.modules.security import get_open_ports, inspect_accounts, run_security_audit
from pysyskit.modules.system import get_resource_usage, get_system_info

app = typer.Typer(name="pysyskit", help="Python System & Automation Toolkit.", no_args_is_help=True)

system_app = typer.Typer(help="System information and resource monitoring.")
process_app = typer.Typer(help="Process inspection.")
network_app = typer.Typer(help="Network interface inspection.")
disk_app = typer.Typer(help="Filesystem and disk inspection.")
logs_app = typer.Typer(help="Local log analysis.")
security_app = typer.Typer(help="Local security diagnostics.")

app.add_typer(system_app, name="system")
app.add_typer(process_app, name="process")
app.add_typer(network_app, name="network")
app.add_typer(disk_app, name="disk")
app.add_typer(logs_app, name="logs")
app.add_typer(security_app, name="security")

console = Console()


def format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


@system_app.command("info")
def system_info() -> None:
    data = get_system_info()
    table = Table(title="PySysKit — System Information")
    table.add_column("Property")
    table.add_column("Value")
    for key, value in data.items():
        table.add_row(key.replace("_", " ").title(), str(value))
    console.print(table)


@system_app.command("resources")
def system_resources() -> None:
    data = get_resource_usage()
    table = Table(title="PySysKit — Resource Usage")
    table.add_column("Resource")
    table.add_column("Value")
    table.add_row("CPU Usage", f"{data['cpu_percent']:.1f}%")
    memory = data["memory"]
    table.add_row("Memory", f"{format_bytes(memory['used'])} / {format_bytes(memory['total'])} ({memory['percent']:.1f}%)")
    swap = data["swap"]
    table.add_row("Swap", f"{format_bytes(swap['used'])} / {format_bytes(swap['total'])} ({swap['percent']:.1f}%)")
    disk = data["disk"]
    table.add_row("Root Disk", f"{format_bytes(disk['used'])} / {format_bytes(disk['total'])} ({disk['percent']:.1f}%)")
    console.print(table)


@process_app.command("list")
def process_list() -> None:
    processes = get_process_list()
    table = Table(title="PySysKit — Running Processes")
    for column in ("PID", "Name", "Status", "User", "Memory %"):
        table.add_column(column)
    for process in processes:
        table.add_row(str(process["pid"]), str(process["name"]), str(process["status"]),
                      str(process["username"]), f"{process['memory_percent']:.2f}")
    console.print(table)


@network_app.command("info")
def network_info() -> None:
    interfaces = get_network_info()
    table = Table(title="PySysKit — Network Interfaces")
    table.add_column("Interface")
    table.add_column("State")
    table.add_column("Speed")
    table.add_column("Addresses")
    for interface in interfaces:
        addresses = "\n".join(
            str(item["address"]) for item in interface["addresses"] if item["address"]
        )
        table.add_row(
            interface["name"],
            "UP" if interface["is_up"] else "DOWN",
            f"{interface['speed_mbps']} Mbps" if interface["speed_mbps"] else "N/A",
            addresses or "N/A",
        )
    console.print(table)


@disk_app.command("usage")
def disk_usage(path: str = typer.Option("/", "--path", "-p")) -> None:
    data = get_disk_usage(path)
    table = Table(title="PySysKit — Disk Usage")
    table.add_column("Property")
    table.add_column("Value")
    for key in ("path", "total", "used", "free", "percent"):
        value = data[key]
        if key in {"total", "used", "free"}:
            value = format_bytes(value)
        elif key == "percent":
            value = f"{value:.1f}%"
        table.add_row(key.title(), str(value))
    console.print(table)


@logs_app.command("analyze")
def logs_analyze() -> None:
    """Analyze common Linux authentication/system logs."""
    result = analyze_logs()

    table = Table(title="PySysKit — Log Analysis")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Scanned files", str(len(result["scanned_files"])))
    table.add_row("Failed authentication", str(result["failed_authentication_attempts"]))
    table.add_row("Successful authentication", str(result["successful_authentication_events"]))
    table.add_row("Invalid user events", str(result["invalid_user_events"]))
    console.print(table)

    if result["top_failure_sources"]:
        source_table = Table(title="Top Authentication Failure Sources")
        source_table.add_column("Source")
        source_table.add_column("Attempts")
        for source, count in result["top_failure_sources"]:
            source_table.add_row(source, str(count))
        console.print(source_table)

    if result["inaccessible_files"]:
        console.print("[yellow]Some log files could not be read due to permissions.[/yellow]")


@security_app.command("ports")
def security_ports() -> None:
    """List listening TCP/UDP sockets on the local host."""
    ports = get_open_ports()
    table = Table(title="PySysKit — Listening Ports")
    table.add_column("Protocol")
    table.add_column("Address")
    table.add_column("Port")
    table.add_column("PID")
    table.add_column("Severity")

    for item in ports:
        if "status" in item:
            console.print(f"[yellow]{item['message']}[/yellow]")
            continue
        table.add_row(
            item["protocol"].upper(),
            item["address"],
            str(item["port"]),
            str(item["pid"] or "N/A"),
            item["severity"],
        )
    console.print(table)


@security_app.command("accounts")
def security_accounts() -> None:
    """Review local accounts for security-relevant indicators."""
    accounts = inspect_accounts()
    table = Table(title="PySysKit — Account Security Review")
    table.add_column("Username")
    table.add_column("UID")
    table.add_column("Shell")
    table.add_column("Severity")
    table.add_column("Indicators")

    for account in accounts:
        table.add_row(
            account["username"],
            str(account["uid"]),
            account["shell"],
            account["severity"],
            ", ".join(account["indicators"]) or "None detected",
        )
    console.print(table)


@security_app.command("audit")
def security_audit() -> None:
    """Run a combined local security audit."""
    result = run_security_audit()

    console.rule("[bold]PySysKit Security Audit[/bold]")

    ports = [item for item in result["open_ports"] if "port" in item]
    console.print(f"Listening sockets: {len(ports)}")

    high_accounts = [
        account for account in result["accounts"] if account["severity"] == "HIGH"
    ]
    review_accounts = [
        account for account in result["accounts"] if account["severity"] == "REVIEW"
    ]

    console.print(f"High-severity account findings: {len(high_accounts)}")
    console.print(f"Accounts requiring review: {len(review_accounts)}")

