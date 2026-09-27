import importlib
import tkinter as tk
import unittest
from types import SimpleNamespace
from threading import Event
from tempfile import TemporaryDirectory
from pathlib import Path
from PIL import Image
from unittest.mock import patch

from virtual_library.data import SIDEBAR_ITEMS
from virtual_library.ui.app import BookDownloaderApp


class UiTests(unittest.TestCase):
    def setUp(self):
        root = tk.Tk()
        root.withdraw()
        original_scale = root.tk.call('tk', 'scaling')
        with patch('virtual_library.ui.app.tk.Tk', return_value=root):
            self.app = BookDownloaderApp()
        self.addCleanup(self.app._close)
        self.addCleanup(lambda: root.tk.call('tk', 'scaling', original_scale))

    def test_every_screen_renders_at_supported_sizes(self):
        for width, height in ((1060, 700), (1280, 850), (1920, 1080)):
            with patch.object(self.app.canvas, 'winfo_width', return_value=width), patch.object(self.app.canvas, 'winfo_height', return_value=height):
                for _, label in SIDEBAR_ITEMS:
                    self.app._handle_action('nav', label)
                    if label == 'Головна':
                        for item in self.app.canvas.find_all():
                            if self.app.canvas.type(item) == 'text':
                                x, y = self.app.canvas.coords(item)
                                if x >= width - 412:
                                    self.assertGreaterEqual(y, 22)
                self.app._handle_action('nav', 'Пошук книг')
                search = next(button for button in self.app.buttons if button['action'] == 'search')
                self.assertLessEqual(search['x2'], width - 14)
                bottom = float(self.app.canvas.cget('scrollregion').split()[3])
                self.assertGreaterEqual(bottom, self.app.results_scroll_bounds[3] * self.app.ui_scale)
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

    def test_cover_images_are_reused_and_search_widget_survives_redraw(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / 'cover.png'
            Image.new('RGB', (30, 40)).save(path)
            book = dict(self.app._book_by_id('1984'), cover_image=str(path))
            with patch('PIL.Image.open', wraps=Image.open) as opened:
                for _ in range(3):
                    self.app._draw_cover(10, 10, 60, 80, book, small=True)
                opened.assert_called_once()
        window = self.app._search_window
        self.app.draw()
        self.app.draw()
        self.assertEqual(self.app.canvas.itemcget(window, 'window'), str(self.app.search_entry))

    def test_search_words_can_match_separate_fields(self):
        self.app.placeholder_active = False
        self.app.search_entry.delete(0, tk.END)
        self.app.search_entry.insert(0, '1984 Орвелл')
        self.assertEqual([book['id'] for book in self.app._visible_books()], ['1984'])

    def test_wrapped_description_marks_omitted_lines(self):
        width = self.app._measure('word word', 'body')
        lines = self.app._wrap_text('word word word word', width, 'body', max_lines=1)
        self.assertTrue(lines[0].endswith('...'))
        self.assertLessEqual(self.app._measure(lines[0], 'body'), width)

    def test_file_picker_import_has_no_gui_side_effect(self):
        with patch('tkinter.Tk') as root, patch('tkinter.filedialog.askopenfilename') as dialog:
            importlib.import_module('virtual_library.path')
        root.assert_not_called()
        dialog.assert_not_called()

    def test_layout_at_small_sizes_and_display_scales(self):
        for scale in (1, 1.25, 1.5, 2):
            self.app.root.tk.call('tk', 'scaling', scale * 96 / 72)
            self.app._apply_font_size()
            for width, height in ((360, 640), (640, 480), (800, 600), (1024, 768), (1920, 1080), (3840, 2160)):
                with self.subTest(scale=scale, size=(width, height)), patch.object(self.app.canvas, 'winfo_width', return_value=width), patch.object(self.app.canvas, 'winfo_height', return_value=height):
                    for _, label in SIDEBAR_ITEMS:
                        self.app._handle_action('nav', label)
                        right, bottom = map(float, self.app.canvas.cget('scrollregion').split()[2:])
                        for button in self.app.buttons:
                            self.assertGreaterEqual(button['x1'], 0, label)
                            self.assertLessEqual(button['x2'] * self.app.ui_scale, right + 1, label)
                            self.assertGreater(button['x2'], button['x1'], label)
                            self.assertLessEqual(button['y2'] * self.app.ui_scale, bottom + 1, label)
                        for item in self.app.canvas.find_all():
                            bounds = self.app.canvas.bbox(item)
                            if bounds and self.app.canvas.type(item) in ('text', 'window'):
                                self.assertGreaterEqual(bounds[0], -2, (label, self.app.canvas.itemcget(item, 'text') if self.app.canvas.type(item) == 'text' else 'window'))
                                self.assertLessEqual(bounds[2], right + 2, label)
                    self.app._handle_action('set_font_size', 'large')
                    self.app._handle_action('nav', 'Пошук книг')
                    self.app._handle_action('filter', None)
                    self.app._handle_action('toggle_description', None)

    def test_hover_does_not_rebuild_canvas_and_redraw_requests_coalesce(self):
        self.app.draw()
        button = next(button for button in self.app.buttons if button['action'] == 'search')
        event = SimpleNamespace(x=(button['x1'] + button['x2']) / 2 * self.app.ui_scale, y=(button['y1'] + button['y2']) / 2 * self.app.ui_scale)
        with patch.object(self.app, 'draw') as draw:
            self.app._on_motion(event)
            self.app._on_leave(None)
            draw.assert_not_called()
        self.app._request_draw()
        job = self.app._draw_job
        self.app._request_draw()
        self.assertEqual(job, self.app._draw_job)

    def test_clicks_follow_page_scroll_and_column_resize_does_not_crash(self):
        with patch.object(self.app.canvas, 'winfo_width', return_value=640):
            self.app.draw()
        button = next(button for button in self.app.buttons if button['action'] == 'favorite')
        self.app.canvas.yview_moveto(0.5)
        origin = self.app.canvas.canvasy(0)
        event = SimpleNamespace(x=(button['x1'] + button['x2']) / 2 * self.app.ui_scale,
                                y=(button['y1'] + button['y2']) / 2 * self.app.ui_scale - origin)
        with patch.object(self.app, '_handle_action') as action:
            self.app._on_click(event)
            action.assert_called_once_with('favorite', button['payload'])
        self.app.scroll_drag = dict(kind='col_resize', start_mouse=0, col_a='status', col_b='date', start_a=110, start_b=132, min_a=72, min_b=80)
        self.app._on_drag(SimpleNamespace(x=10 * self.app.ui_scale, y=0))
        self.assertEqual(self.app.download_col_status_w, 120)

    def test_search_runs_in_background_and_ignores_stale_results(self):
        started, finish = Event(), Event()
        def slow_search(_query):
            started.set()
            finish.wait(2)
            return []
        self.app.placeholder_active = False
        self.app.search_entry.delete(0, tk.END)
        self.app.search_entry.insert(0, 'old query')
        with patch.object(self.app.book_search, 'search_books', side_effect=slow_search):
            self.app._run_search()
            self.assertTrue(started.wait(1))
            self.assertTrue(self.app._search_pending)
            self.app.search_entry.delete(0, tk.END)
            self.app._run_search()
            finish.set()
            result = self.app._search_queue.get(timeout=2)
            self.app._search_queue.put(result)
            if self.app._search_job:
                self.app.root.after_cancel(self.app._search_job)
            self.app._poll_search()
            self.assertIsNone(self.app.api_results)


if __name__ == '__main__':
    unittest.main()
