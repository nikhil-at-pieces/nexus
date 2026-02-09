"""
Nexus — Twitter listening / social listening tool.
Main CLI entry point: run, worker, scheduler, twitter-search.
"""
import os
from typing import List, Literal, Optional

import typer
import uvicorn
from rich.console import Console

console = Console()
app = typer.Typer(name="nexus", help="Nexus — Twitter listening tool")


@app.command()
def run(
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
    workers: int = typer.Option(1, help="Number of worker processes"),
):
    """Start the Nexus API server."""
    console.print("[bold green]Starting Nexus API server...[/bold green]")
    port_env = os.getenv("PORT")
    if port_env:
        try:
            port = int(port_env)
        except ValueError:
            pass
    uvicorn.run(
        "nexus.api.app:create_app",
        factory=True,
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
    )


@app.command()
def worker(
    queue: str = typer.Option("default", help="Queue name to process"),
    concurrency: int = typer.Option(4, help="Number of concurrent workers"),
):
    """Start a background worker process."""
    console.print(f"[bold blue]Starting worker for queue: {queue}[/bold blue]")
    from nexus.workers.celery_app import create_celery_app
    celery_app = create_celery_app()
    celery_app.worker_main([
        "worker", f"--queue={queue}", f"--concurrency={concurrency}", "--loglevel=info",
    ])


@app.command()
def scheduler():
    """Start the task scheduler for scheduled listening runs."""
    console.print("[bold yellow]Starting scheduler...[/bold yellow]")
    from nexus.scheduler.scheduled_listening_scheduler import run_scheduler
    run_scheduler()


@app.command("twitter-search")
def twitter_search(
    keyword: List[str] = typer.Option(..., "--keyword", "-k", help="Keyword(s) to search"),
    last_hours: int = typer.Option(48, "--last-hours", help="Look back hours"),
    limit: int = typer.Option(50, "--limit", help="Max tweets"),
    match_mode: Literal["ALL", "ANY"] = typer.Option("ANY", "--match-mode"),
    org_id: str = typer.Option(..., "--org-id", help="Organization ID for twscrape accounts"),
    output: Literal["table", "jsonl", "json"] = typer.Option("table", "--output"),
):
    """Search X/Twitter using configured twscrape accounts (org-scoped)."""
    from nexus.main import _build_x_search_query, _tweet_to_dict
    from nexus.services.twscrape_account_service import TwscrapeAccountService
    from twscrape import gather
    import asyncio
    import json

    async def _run():
        account_service = TwscrapeAccountService()
        api = await account_service.get_api_for_org(org_id)
        query = _build_x_search_query(keyword, hours_back=last_hours, match_mode=match_mode)
        tweets = await gather(api.search(query, limit=limit))
        rows = [_tweet_to_dict(t) for t in (tweets or [])]
        if output == "jsonl":
            for r in rows:
                console.print(json.dumps(r, ensure_ascii=False))
        elif output == "json":
            console.print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            from rich.table import Table
            table = Table(title=f"X search results ({len(rows)})")
            table.add_column("date"); table.add_column("user"); table.add_column("text"); table.add_column("url")
            for r in rows:
                table.add_row(r.get("date") or "", (r.get("username") or ""), (r.get("text") or "")[:200], r.get("url") or "")
            console.print(table)
    asyncio.run(_run())


if __name__ == "__main__":
    app()
