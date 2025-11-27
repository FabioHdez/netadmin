from textual.widgets import Button, Static, Label, ListItem, ListView
from textual.containers import Center, Vertical
from textual.screen import ModalScreen

class ConfirmationModal(ModalScreen[bool]):
	"""A simple Yes/No confirmation modal."""

	def __init__(self, message: str = "Are you sure?"):
		super().__init__()
		self.message = message

	def compose(self):
		yield Center(
			Vertical(
				Static(self.message, id="confirm-message"),
				ListView(
					ListItem(Label("Yes")),
					ListItem(Label("No"))
				),
				
				# Button("Yes", id="yes", variant="success"),
				# Button("No", id="no", variant="error"),
				id="confirm-box",
			)
		)

	async def on_list_view_selected(self, event: ListView.Selected) -> None:
		selected_option:Label = event.item.children[0]
		
		if selected_option.content == "Yes":
			self.dismiss(True)
		else:
			self.dismiss(False)
