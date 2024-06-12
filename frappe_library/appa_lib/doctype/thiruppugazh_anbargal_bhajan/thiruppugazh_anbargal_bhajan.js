// Copyright (c) 2024, App Publishing and contributors
// For license information, please see license.txt

frappe.ui.form.on("Thiruppugazh Anbargal Bhajan", {
	refresh(frm) {
		frm.add_custom_button(__('Update playlist'), () => {
			if (frm.is_dirty()) {
				console.log('Saving Bhajan...')
				frm.save();
			}
			console.log("Calling backend...");
			frm.call('update_playlist')
		})
	},
});

reload_page = () => {
	console.log("Reloading the bhajan...")
	location.reload()
}
