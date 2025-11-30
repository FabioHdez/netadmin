from textual.widgets import Label, ListItem, ListView

import netty

class HostList(ListView):
	"""Right list—purely visual."""
	def __init__(self,hosts: list[str], json_data, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.hosts = hosts
		self.json_data = json_data

	def on_mount(self) -> None:
		self._build_ui()
	
	def _build_ui(self):
		self.clear()
		for host in self.hosts:
			print(host)
			hostname = netty.get_json_host(json_data=self.json_data, ip=host)
			print(hostname)
			if hostname and hostname["hostname"] != "":
				hostname = f"{hostname["hostname"]} - {host}"
			else:
				hostname = host
			li = ListItem(Label(hostname),name=host)
			self.append(li)

	def update_hosts (self, new_hosts: list[str],json_data):
		self.hosts = new_hosts
		self.json_data = json_data
		self._build_ui()
