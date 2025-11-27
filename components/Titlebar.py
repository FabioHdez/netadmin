from textual.widgets import Static

class TitleBar(Static):
	"""Top banner only renders fixed text."""
	def __init__(self, title: str, version: str, online_count: int) -> None:
		super().__init__(id="titlebar")
		self.title = title
		self.version = version
		self.online_count = online_count

	def render(self) -> str:
		return f"{self.title} [b cyan]v{self.version}[/b cyan]  |  Online Hosts: [b cyan]{self.online_count}[/b cyan]"
	
	def update_online_count(self,new_count):
		self.online_count = new_count
		self.update(self.render())

