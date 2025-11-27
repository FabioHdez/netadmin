from textual.widgets import Label, ListItem, ListView

class HostList(ListView):
	"""Right list—purely visual."""
	def __init__(self,hosts: list[str], *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.hosts = hosts

	def on_mount(self) -> None:
		self._build_ui()
	
	def _build_ui(self):
		self.clear()
		for host in self.hosts:
			li = ListItem(Label(host))
			self.append(li)

	def update_hosts (self, new_hosts: list[str]):
		self.hosts = new_hosts
		self._build_ui()
