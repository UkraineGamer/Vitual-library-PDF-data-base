import unittest
from unittest.mock import Mock

from virtual_library.ui.views import AppViewsMixin


class CategoryLayoutTests(unittest.TestCase):
    def test_scrolling_and_hit_areas_use_the_visible_viewport(self):
        view = AppViewsMixin()
        view.canvas = Mock()
        view._round_rect = Mock()
        view._category_chips_metrics = lambda: ([(str(i), 70) for i in range(8)], 624)
        view.active_category = '0'
        view.buttons = []
        view._button = lambda x1, y1, x2, y2, *args, **kwargs: view.buttons.append(dict(x1=x1, x2=x2))
        for width in (400, 650, 1000):
            for scroll in (0, 10000):
                view.category_scroll = scroll
                view.buttons.clear()
                view._draw_category_container(225, 76, width)
                geom = view._category_container_geom
                left = geom['viewport_x']
                right = left + geom['viewport_w']
                self.assertLessEqual(right, 225 + width - 150)
                self.assertEqual(view.category_scroll_bounds[-1], max(0, 624 - geom['viewport_w']))
                for button in view.buttons:
                    self.assertGreaterEqual(button['x1'], left)
                    self.assertLessEqual(button['x2'], right)
                if view.category_scroll_bounds[-1]:
                    x1, _, x2, _, _, thumb, size, _ = view.category_scrollbar_bounds
                    self.assertGreaterEqual(thumb, x1)
                    self.assertLessEqual(thumb + size, x2)


if __name__ == '__main__':
    unittest.main()
