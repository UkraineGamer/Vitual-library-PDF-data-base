from virtual_library.config import COLORS, TextAnchor, TextJustify


class UiComponentsMixin:

    def _round_rect(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        radius: float = 8,
        fill: str = "",
        outline: str = "",
        width: int = 1,
    ) -> int:
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.canvas.create_polygon(
            points,
            smooth=True,
            splinesteps=12,
            fill=fill,
            outline=outline,
            width=width,
        )

    def _text(
        self,
        x: float,
        y: float,
        text: str,
        fill: str = COLORS["text"],
        font: str = "body",
        anchor: TextAnchor = "nw",
        width: float | None = None,
        justify: TextJustify = "left",
    ) -> int:
        kwargs = {
            "text": text,
            "fill": fill,
            "font": self.fonts[font],
            "anchor": anchor,
            "justify": justify,
        }
        if width is not None:
            kwargs["width"] = width
        return self.canvas.create_text(x, y, **kwargs)

    def _button(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        label: str,
        action: str,
        payload: str | None = None,
        *,
        fill: str = COLORS["panel_soft"],
        active_fill: str | None = None,
        text_fill: str = COLORS["text"],
        radius: int = 8,
        font: str = "button",
        icon: str | None = None,
    ) -> None:
        key = (action, payload)
        hovered = self.hover_action == key
        bg = active_fill if hovered and active_fill else fill
        self._round_rect(x1, y1, x2, y2, radius, fill=bg, outline=COLORS["line_soft"])
        center_y = (y1 + y2) / 2
        if icon:
            label_max = max(20, x2 - x1 - 42)
            label = self._trim(label, label_max, font)
            self._text(x1 + 14, center_y, icon, text_fill, "body", "w")
            self._text(x1 + 36, center_y, label, text_fill, font, "w")
        else:
            label_max = max(20, x2 - x1 - 12)
            label = self._trim(label, label_max, font)
            self._text((x1 + x2) / 2, center_y, label, text_fill, font, "center")
        self.buttons.append(
            {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "action": action,
                "payload": payload,
            }
        )

