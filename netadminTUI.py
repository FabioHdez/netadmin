# netadmin_ui.py
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Label, ListItem, ListView, Static

import re, netty, netadminComponents


MENU_OPTIONS = {
	'opt_1': 'View Hosts',
	'opt_2': 'SSH to Host ',
	'opt_3': 'Ping Host',
	'opt_4': 'Add Host',
	'opt_r': 'Refresh Hosts & Configuration',
	'opt_d': 'Restore to Default',
	'opt_q': 'Exit'
}

class NetAdminUI(App):
	CSS_PATH = "netadmin_ui.tcss"
	BINDINGS = [("backspace", "focus_back", "Return to options menu.")]

	def on_mount(self) -> None:
		pass

	def compose(self) -> ComposeResult:
		# Top banner
		yield netadminComponents.TitleBar("NetAdmin", version = '2.0', online_count=len(netty.online_hosts.all_hosts()))

		# Two-column body
		with Horizontal(id="body"):
			with Vertical():
				yield Label("Menu", classes="section-title")
				self.menu = netadminComponents.Menu(id="options")
				yield self.menu

			with Vertical():
				yield Label("Currently Online Hosts:", classes="section-title")
				self.hosts = netadminComponents.HostList(id="hosts")
				yield self.hosts
		yield Footer()
	
	def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
		"""Called when user siwtches on a ListView item."""
		highlighted_item_id = event.item.id

		# ignore items without id
		if not highlighted_item_id:
			return

		options_menu_pattern = r'^opt_(\w)$'
		highlighted_item_match = re.match(options_menu_pattern, highlighted_item_id)

		if highlighted_item_match:
			highlighted_option = highlighted_item_match.group(1)
			if highlighted_option.isalpha():
				self.query_one("#hosts", ListView).disabled = True
			else:
				self.query_one("#hosts", ListView).disabled = False

	def on_list_view_selected(self, event: ListView.Selected) -> None:
		"""Called when user presses Enter on a ListView item."""
		selected_item_id = event.item.id

		# ignore items without id
		if not selected_item_id:
			return

		############ OPTIONS ############
		# matches for this pattern are only for the option menu
		options_menu_pattern = r'^opt_(\w)$'
		selected_item_match = re.match(options_menu_pattern, selected_item_id)

		if selected_item_match:
			selected_option = selected_item_match.group(1)
			if selected_option.isalpha():
				# options that do not require host
				self.query_one("#hosts", ListView).can_focus = False
				print(f"Executing {selected_item_id}")
			else:
				# options that require host
				self.query_one("#hosts", ListView).can_focus = True
				self.action_focus_next()
			return
		
		############ HOSTS ############
		# matches for this pattern are only for the hosts menu
		hosts_menu_pattern = r'^hst_(\w+)$'
		selected_item_match = re.match(hosts_menu_pattern, selected_item_id)

		if selected_item_match:
			options_menu = self.query_one("#options", ListView)	
			print(f"Executing {options_menu.highlighted_child.id} on {selected_item_id}")
			return
	
	def action_focus_back(self):
		self.query_one("#options", ListView).focus()


if __name__ == "__main__":
	# pre load stuff
	print("Loading NetAdmin v2.0...")
	try:
		netty.refresh_json()
		if (netty.ip_range == ''):raise Exception
	except Exception as e:
		print("Issue found with config file. Reconfiguring...")
		netty.init_config()
	netty.scan_network(netty.ip_range)

	# run app
	NetAdminUI().run()
