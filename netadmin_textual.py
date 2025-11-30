from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, Footer, ListView
from textual import work


from components.Titlebar import TitleBar
from components.Menu import Menu, MENU_OPTIONS
from components.HostList import HostList
from components.LoadingModal import LoadingModal
from components.ConfirmationModal import ConfirmationModal
from components.InputModal import InputModal
from components.PingScreen import PingScreen

import re, os
import netty


all_hosts:list[str] = []
ip_range:str = ""
json_data = ""

class NetAdmin(App):
	"""
	Docstring for NetAdmin
	"""
	CSS_PATH = "netadmin_ui.tcss"
	BINDINGS = [("backspace", "focus_back", "Return to options menu.")]

	def compose(self) -> ComposeResult:
		# Top banner
		self.title_bar = TitleBar("NetAdmin", version = '2.0', online_count=len(all_hosts))
		yield self.title_bar
		
		# Two-column body
		with Horizontal(id="body"):
			with Vertical():
				yield Label("Menu", classes="section-title")
				self.menu = Menu(id="options")
				yield self.menu
			with Vertical():
				yield Label("Currently Online Hosts:", classes="section-title")
				self.hosts = HostList(id="hosts",hosts=all_hosts, json_data=json_data)
				yield self.hosts
		yield Footer()
	
	def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
		"""Called when user siwtches on a ListView item."""
		
		highlighted_item_id = getattr(event.item, "id", None)
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

	async def on_list_view_selected(self, event: ListView.Selected) -> None:
		"""Called when user presses Enter on a ListView item."""

		selected_item_id = getattr(event.item, "id", None)
		if not selected_item_id:
			selected_item_id = ""

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
				option_handle = {
					'opt_r': self.option_refresh,
					'opt_d': self.option_restore,
					'opt_q': self.option_exit_program
				}
				await option_handle[selected_item_id]()
			else:
				# options that require host
				self.query_one("#hosts", ListView).can_focus = True
				self.action_focus_next()
			return
		############ HOSTS ############
		# matches for this pattern are only for the hosts menu
		hosts_menu_pattern = r'^\d+\.\d+\.\d+\.\d+$'
		selected_host = event.item.name
		if not selected_host or selected_host.strip() == "": return
		

		selected_item_match = re.match(hosts_menu_pattern, selected_host)

		if selected_item_match:
			options_menu = self.query_one("#options", ListView)
			selected_option = options_menu.highlighted_child.id
			print(f"Executing {selected_option} on {selected_host}")
			option_handle = {
				'opt_1': self.option_view,
				'opt_2': self.option_ssh,
				'opt_3': self.option_ping,
				'opt_4': self.option_add
			}
			await option_handle[selected_option](selected_host)
			return
		
	def action_focus_back(self):
		self.query_one("#options", ListView).focus()


	# TODO: DELETE LATER
	async def key_space(self):
		#self.title_bar.update_online_count(self.title_bar.online_count+1)
		#self.hosts.update_hosts(new_hosts=['127.0.0.1','127.0.0.2','127.0.0.3'])
		# await self.push_screen(LoadingModal())
		# time.sleep(3)
		# await self.pop_screen()
		# await self.push_screen(InputModal(), callback = lambda result: print(result))
		# await self.push_screen(PingScreen(host="10.0.0.11"))
		host = "10.0.0.11"
		username:str = ""
		if username == r"N\A" or username.strip() == "":
			command = fr'''start powershell -NoExit -Command "$u = Read-Host 'Username'; ssh $u@{host}"'''
		else:
			command = fr'start powershell -NoExit -Command "ssh {username}@{host}"'
		os.system(command)
		#os.system("ssh fabio@10.0.0.11")
		pass
		

	def refresh_ui(self):
		"""Scan network and refresh ui"""
		global json_data
		global ip_range
		json_data = netty.refresh_json()
		ip_range = json_data["ip_range"]
		new_hosts = netty.scan_network(ip_range)
		self.title_bar.update_online_count(len(new_hosts))
		self.hosts.update_hosts(new_hosts, json_data)

	# Refresh
	async def option_refresh(self):
		"""Full refresh of the configuration and online hosts cache"""
		await self.push_screen(LoadingModal())
		self.refresh_ui() # custom func to refresh the hosts list and the ui
		await self.pop_screen()
	
	# Restore
	RESTORE_CONFIRM_MSG = "Are you sure you want to restore the configuration to the default?"
	async def option_restore(self,msg=RESTORE_CONFIRM_MSG):
		"""Restore configuration to default"""
		await self.push_screen(ConfirmationModal(message=msg),self.option_restore_confirmation_callback)
	# callback function for the confirmation modal
	async def option_restore_confirmation_callback(self, result:bool, message:str = "Enter IP range: (e.g. 10.0.0.0/27)"):
		if result:
			# callback for the new modal can be a simple variable assignment with the ip
			print(result)
			await self.push_screen(InputModal(message=message),callback=self.option_restore_ip_range_input_callback)

	async def option_restore_ip_range_input_callback(self, result:str):
		result = result.strip()
		if result != "" and netty.valid_ip(result):
			netty.init_config(result)
			await self.push_screen(LoadingModal())
			self.refresh_ui() # custom func to refresh the hosts list and the ui
			await self.pop_screen()
		else:
			await self.option_restore(msg=f"Invalid IP Range!\n{self.RESTORE_CONFIRM_MSG}")
	
	# Exit
	async def option_exit_program(self):
		self.exit()
	
	# Ping
	async def option_ping(self, host:str):
		await self.push_screen(PingScreen(host=host))
		pass
	# Add
	async def option_add(self, host:str):
		print(f"adding host {host}")
		setattr(self,"host", host)
		message = "Enter a hostname:"
		# modal to set the hostname
		await self.push_screen(InputModal(message=message),callback=self.option_add_get_hostname_callback)

	async def option_add_get_hostname_callback(self, result:str):
		hostname = result.strip()
		print(f"adding hostname: {hostname}")
		if hostname == '': hostname = 'N/A'
		setattr(self,"hostname", hostname)
		message = "Enter your username for this host (Leave empty if none): "
		await self.push_screen(InputModal(message=message),callback=self.option_add_get_username_callback)

	async def option_add_get_username_callback(self, result:str):
		username = result
		setattr(self,"username", username)

		host = getattr(self,"host",None)
		hostname = getattr(self,"hostname",None)
		username = getattr(self,"username",None)
		
		netty.add_host(host=host, hostname=hostname, username=username)
		await self.push_screen(LoadingModal())
		self.refresh_ui() # custom func to refresh the hosts list and the ui
		await self.pop_screen()
	
	# ssh
	async def option_ssh(self, host:str):
		username:str = ""
		cached_host = netty.get_json_host(json_data, host)
		if cached_host:
			username = cached_host["username"]
		if username.strip() == "":
			# powershell prompts user for username
			command = fr'''start powershell -NoExit -Command "$u = Read-Host 'Username'; ssh $u@{host}"'''
		else:
			# no username prompting
			command = fr'start powershell -NoExit -Command "ssh {username}@{host}"'
		os.system(command)
		pass
		
	# view
	async def option_view(self, host:str):
		cached_host = netty.get_json_host(json_data,host)
		# show modal 
		if cached_host:
			print('Saved')
			print(f'IP: {cached_host["ip"]}')
			print(f'Hostname: {cached_host["hostname"]}')
			print(f'Username: {cached_host["username"]}')
		else:
			print('Not Saved')
			print(f'IP: {host}')
		
	

if __name__ == "__main__":
	print("Loading NetAdmin v2.0...")
	try:
		json_data = netty.refresh_json()
		ip_range = json_data["ip_range"]
		if (ip_range == ''):raise Exception
	except Exception as e:
		print("Issue found with config file. Reconfiguring...")
		netty.init_config()

	all_hosts = netty.scan_network(ip_range)
	# run app
	NetAdmin().run()
