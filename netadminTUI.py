# netadmin_ui.py
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Label, ListItem, ListView, Static


MENU_OPTIONS = {
    'opt_1': 'View Hosts',
    'opt_2': 'SSH to Host ',
    'opt_3': 'Ping Host',
    'opt_4': 'Add Host',
    'opt_d': 'Restore to Default',
    'opt_r': 'Refresh Hosts & Configuration',
    'opt_q': 'Exit'
}

RIGHT_HOSTS = [
	" 1: 10.0.0.10  - local.main",
	" 2: 10.0.0.11  - local.dev",
]


class TitleBar(Static):
	"""Top banner only renders fixed text."""
	def __init__(self, title: str, version: str, online_count: int) -> None:
		super().__init__(id="titlebar")
		self.title = title
		self.version = version
		self.online_count = online_count

	def render(self) -> str:
		return f"{self.title} [b cyan]v{self.version}[/b cyan]  |  Online Hosts: [b cyan]{self.online_count}[/b cyan]"


class Menu(ListView):
	"""Left list—purely visual."""
	def on_mount(self) -> None:
		for option in MENU_OPTIONS:
			self.append(ListItem(Label(f"{option[-1]}. {MENU_OPTIONS[option]}"), id=option))

	# print the currently selected menu option
	def on_list_view_highlighted(self, event: ListView.Selected) -> None:
		# Get the selected ListItem
		selected_item = event.item
		id = selected_item.id
		print(f"Selected option: {id}")

class HostList(ListView):
	"""Right list—purely visual."""
	def on_mount(self) -> None:
		for line in RIGHT_HOSTS:
			self.append(ListItem(Label(line)))


class NetAdminUI(App):
	CSS_PATH = "netadmin_ui.tcss"

	def compose(self) -> ComposeResult:
		# Top banner
		yield TitleBar("NetAdmin", version = '2.0', online_count=2)

		# Two-column body
		with Horizontal(id="body"):
			with Vertical(id="left"):
				yield Label("Menu", classes="section-title")
				self.menu = Menu()
				yield self.menu

			with Vertical(id="right"):
				yield Label("Currently Online Hosts:", classes="section-title")
				self.hosts = HostList()
				yield self.hosts
		yield Footer()
	



	# Optional: make Tab just flip focus for nicer demo (no logic invoked)
	# def on_mount(self) -> None:
	# 	self.set_focus(self.menu)
				

	# def action_focus_next(self) -> None:  # bound by Footer help
	#     if self.focused is self.menu:
	#         self.set_focus(self.hosts)
	#     else:
	#         self.set_focus(self.menu)


if __name__ == "__main__":
	NetAdminUI().run()
