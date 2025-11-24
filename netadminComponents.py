from textual.widgets import Footer, Label, ListItem, ListView, Static
import netadminTUI, netty

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
		for option in netadminTUI.MENU_OPTIONS:
			self.append(ListItem(Label(f"{option[-1]}. {netadminTUI.MENU_OPTIONS[option]}"), id=option))

class HostList(ListView):
	"""Right list—purely visual."""
	def on_mount(self) -> None:
		# build hosts dictionary
		hosts = {}
		for i,host in enumerate(netty.online_hosts.all_hosts(),1):
			hosts[f"hst_{i}"] = host	
		# append to ui
		for host in hosts:
			self.append(ListItem(Label(hosts[host]), id=host))

