import asyncio

from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Log, Button


class PingScreen(Screen):
	"""Screen that runs `ping` and shows the output."""

	BINDINGS = [
		("escape", "app.pop_screen", "Close"),
		("enter", "app.pop_screen", "Close"),
		("space", "app.pop_screen", "Close")
	]

	def __init__(self, host: str, **kwargs):
		super().__init__(**kwargs)
		self.host = host

	def compose(self) -> ComposeResult:
		yield Log(id="ping_log")

	def on_mount(self) -> None:
		# Start the ping as soon as the screen is shown
		self.run_ping(self.host)

	@work  # runs as an async worker (non-blocking)
	async def run_ping(self, host: str) -> None:
		log = self.query_one("#ping_log", Log)
		log.write_line(f"Pinging {host}...\n")

		process = await asyncio.create_subprocess_shell(
			f"ping {host}",
			stdout=asyncio.subprocess.PIPE,
			stderr=asyncio.subprocess.PIPE,
		)

		# Stream stdout lines into the Log
		assert process.stdout is not None
		async for raw_line in process.stdout:
			line = raw_line.decode(errors="ignore").rstrip()
			log.write_line(line)

		await process.wait()
		log.write_line(f"\nPing finished with code {process.returncode}")

