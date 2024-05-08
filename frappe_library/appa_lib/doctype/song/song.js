// Copyright (c) 2024, App Publishing and contributors
// For license information, please see license.txt

frappe.ui.form.on('Song', {
	rich_lyrics: function (frm) {
		const synopsis_maxsize = 30;
		console.log(frm.doc.rich_lyrics);
		lyrics = new DOMParser()
			.parseFromString(frm.doc.rich_lyrics, "text/html")
			.documentElement.textContent
			.replace(/\s\s+/g, ' ');
		if (lyrics) {
			limit = Math.min(synopsis_maxsize, lyrics.length);
			end = lyrics.lastIndexOf(' ', limit);
			end = (end === -1) ? synopsis_maxsize : end
			frm.doc.synopsis = lyrics.substring(0, end);
			console.log(frm.doc.synopsis);
		} else {
			console.log("lyrics empty");
		}
	}
});
