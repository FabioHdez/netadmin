from textual.widgets import Static, Input
from textual.containers import Center, Vertical
from textual.screen import ModalScreen

class InputModal(ModalScreen[str | None]):
	"""A simple centered text input modal."""

	BINDINGS = [
		("escape", "app.pop_screen", "Close"),
		("enter", "app.pop_screen", "Close"),
		("space", "app.pop_screen", "Close")
	]

	def __init__(self, message: str = "Enter a value:"):
		super().__init__()
		self.message = message

	def compose(self):
		yield Center(
			Vertical(
				Static(self.message, id="input-message"),
				Center(
					Input(
						#placeholder="e.g. 10.0.0.0/27",
						id="input-field",
					)
				),
				id="input-box",
			)
		)
	async def on_input_submitted(self, event: Input.Submitted) -> None:
		"""Called when user presses Enter in the input."""
		self.dismiss(event.value)
