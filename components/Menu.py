from textual.widgets import Label, ListItem, ListView

MENU_OPTIONS = {
	'opt_1': 'View Hosts',
	'opt_2': 'SSH to Host ',
	'opt_3': 'Ping Host',
	'opt_4': 'Add Host',
	'opt_r': 'Refresh Hosts & Configuration',
	'opt_d': 'Restore to Default',
	'opt_q': 'Exit'
}
class Menu(ListView):
	"""Left list—purely visual."""
	def on_mount(self) -> None:
		for option in MENU_OPTIONS:
			self.append(ListItem(Label(f"{option[-1]}. {MENU_OPTIONS[option]}"), id=option))