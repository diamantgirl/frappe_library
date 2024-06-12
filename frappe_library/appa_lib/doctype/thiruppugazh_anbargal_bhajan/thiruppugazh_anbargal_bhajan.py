# Copyright (c) 2024, App Publishing and contributors
# For license information, please see license.txt

import os
import frappe
from frappe.model.document import Document
import time

class ThiruppugazhAnbargalBhajan(Document):
	@frappe.whitelist()
	def update_playlist(self):
		print("Playing lists!")
		token = {}
		token_str = os.getenv("API_TOKEN_JSON")
		if token_str:
			print("Loading credentials from env...")
			token = eval(token_str)
		else:
			print("Credentials not found. Using empty token...")
		num_steps = 1 + len(self.song_list)
		step = 100 / (num_steps)
		state = 0
		frappe.publish_progress(
			int(state*step),
			title='Updating Playlist',
			description='Creating empty playlist...',
			doctype=self.doctype,
			docname=self.name,
		)
		# TODO: delete any existing playlist for this bhajan
		time.sleep(2)
		state += 1
		frappe.publish_progress(
			int(state*step),
			title="Updating Playlist",
			description="Empty Playlist created. Adding songs...",
			doctype=self.doctype,
			docname=self.name,
		)
		time.sleep(1)
		for entry in self.song_list:
			print(f"{entry.number}\t{entry.song}")
			frappe.publish_progress(
				int(state*step),
				title="Updating Playlist",
				description=f"Add to playlist: {entry.song}",
				doctype=self.doctype,
				docname=self.name,
			)
			time.sleep(1)
			state += 1
			frappe.publish_progress(
				int(state*step),
				title="Updating Playlist",
				description=f"Successfully added {entry.song}!",
				doctype=self.doctype,
				docname=self.name,
			)
		frappe.publish_progress(
			100,
			title="Updating Playlist",
			description="Updating Bhajan with link to playlist",
			doctype=self.doctype,
			docname=self.name,
		)
		frappe.msgprint(
			title = "Success",
			msg = "Create playlist on youtube: <a href=\"https://youtu.be\" target=\"blank\">Youtube </a>",
			realtime = True,
			primary_action = {
				"label": frappe._("Ok"),
				"client_action": "reload_page",
				"hide_on_success": True,
			}
		)
