from textual.screen import ModalScreen
from textual.containers import Center
from textual.widgets import Static

class LoadingModal(ModalScreen):
	def compose(self):
		yield Center(
			Static("Loading...\nPlease wait",id="loading-box")
		)
