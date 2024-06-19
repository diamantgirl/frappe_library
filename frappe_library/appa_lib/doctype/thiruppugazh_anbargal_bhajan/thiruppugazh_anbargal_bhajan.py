# Copyright (c) 2024, App Publishing and contributors
# For license information, please see license.txt

import os
import time
from urllib.parse import urlparse, parse_qs

import frappe
from frappe.model.document import Document
import frappe_library.appa_lib.playlists as playlists


class ThiruppugazhAnbargalBhajan(Document):
    @frappe.whitelist()
    def update_playlist(self):
        print("Playing lists!")
        youtube = playlists.get_api_client()
        num_steps = 1 + len(self.song_list)
        step = 100 / (num_steps)
        state = 0
        frappe.publish_progress(
            1 + int(state * step),
            title="Updating Playlist",
            description="Creating empty playlist...",
            # doctype=self.doctype,
            # docname=self.name,
        )
        time.sleep(1)
        if self.link_to_playlist:
            print(f"Found existing playlist: {self.link_to_playlist}")
            query = urlparse(self.link_to_playlist).query
            playlist_ids = parse_qs(query).get("list")
            if playlist_ids and len(playlist_ids) > 0:
                try:
                    print(f"Attempt to delete: {playlist_ids[0]}")
                    playlists.delete(youtube, playlist_ids[0])
                    print("Successfully deleted!")
                except Exception as e:
                    print(
                        f"Failed to delete existing playlist: {self.link_to_playlist}\n {e}"
                    )
                finally:
                    self.link_to_playlist = ""

        ctime = time.asctime(time.localtime())
        playlist_description = f"முருகா ஶரணம். Playlist for practice. Created: {ctime}"
        response = playlists.create(
            youtube, title=self.name, description=playlist_description
        )
        playlist_ids = response.get("id") if response else ""
        state += 1
        frappe.publish_progress(
            int(state * step),
            title="Updating Playlist",
            description="Empty Playlist created. Adding songs...",
            # doctype=self.doctype,
            # docname=self.name,
        )
        time.sleep(1)
        for entry in self.song_list:
            print(f"{entry.number}\t{entry.song}")
            song = frappe.get_doc("Song", entry.song)
            video_ids = playlists.extract_id(song.video_link_youtube)
            frappe.publish_progress(
                int(state * step),
                title="Updating Playlist",
                description=f"Add to playlist: {entry.song}",
                # doctype=self.doctype,
                # docname=self.name,
            )
            time.sleep(1)
            if video_ids and len(video_ids) > 0:
                playlists.insert_video(youtube, playlist_ids, video_ids[0])
            state += 1
            frappe.publish_progress(
                int(state * step),
                title="Updating Playlist",
                description=f"Successfully added {entry.song}!",
                # doctype=self.doctype,
                # docname=self.name,
            )
            time.sleep(1)
        frappe.publish_progress(
            100,
            title="Updating Playlist",
            description="Updating Bhajan with link to playlist",
            # doctype=self.doctype,
            # docname=self.name,
        )
        time.sleep(1)
        self.link_to_playlist = f"https://www.youtube.com/playlist?list={playlist_ids}"
        self.save()
        frappe.msgprint(
            title="Success",
            msg=f'Created playlist on <a href="{self.link_to_playlist}" target="blank">Youtube </a>',
            realtime=True,
            primary_action={
                "label": frappe._("Ok"),
                "client_action": "reload_page",
                "hide_on_success": True,
            },
        )
