import importlib
import tkinter as tk
import unittest
from unittest.mock import patch

from virtual_library.data import SIDEBAR_ITEMS
from virtual_library.ui.app import BookDownloaderApp


class UiTests(unittest.TestCase):
    def setUp(self):
        root = tk.Tk()
        root.withdraw()
        with patch('virtual_library.ui.app.tk.Tk', return_value=root):
            self.app = BookDownloaderApp()
        self.addCleanup(root.destroy)

    def test_every_screen_renders_at_supported_sizes(self):
        for width, height in ((1060, 700), (1280, 850), (1920, 1080)):
            with patch.object(self.app.canvas, 'winfo_width', return_value=width), patch.object(self.app.canvas, 'winfo_height', return_value=height):
                for _, label in SIDEBAR_ITEMS:
                    self.app._handle_action('nav', label)
                self.app._handle_action('nav', 'Пошук книг')
                search = next(button for button in self.app.buttons if button['action'] == 'search')
                self.assertLessEqual(search['x2'], width - 14)
                self.assertLessEqual(self.app.results_scroll_bounds[3] + 10 + 226, height - 14)
                self.app._handle_action('set_theme', 'light')
                self.app._handle_action('set_theme', 'dark')

    def test_font_sizes_include_details_and_restore_original_sizes(self):
        original = {name: font.cget('size') for name, font in self.app.fonts.items()}
        self.app._handle_action('set_font_size', 'large')
        self.assertEqual(self.app.fonts['body_detail'].cget('size'), original['body_detail'] + 2)
        self.app._handle_action('set_font_size', 'small')
        self.app._handle_action('set_font_size', 'medium')
        self.assertEqual({name: font.cget('size') for name, font in self.app.fonts.items()}, original)

    def test_redraw_releases_cover_references(self):
        self.app._cover_refs = [object()]
        self.app.draw()
        self.assertEqual(self.app._cover_refs, [])

    def test_file_picker_import_has_no_gui_side_effect(self):
        with patch('tkinter.Tk') as root, patch('tkinter.filedialog.askopenfilename') as dialog:
            importlib.import_module('virtual_library.path')
        root.assert_not_called()
        dialog.assert_not_called()


if __name__ == '__main__':
    unittest.main()
