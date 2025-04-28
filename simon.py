from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button

COLORS = ["green", "red", "yellow", "blue"]


class ColorButton(Button, can_focus=False, inherit_css=False):
    DEFAULT_CSS = """
    ColorButton {
        min-height: 8;
        min-width: 16;
        background-tint: black 30%;
        text-style: bold;
        padding: 1 2;
        
        &.-active {
            background-tint: 0%;
        }
    }
    """

    def __init__(self, color: str):
        super().__init__(color[0], id=f"{color}-btn")
        self.styles.background = color


class SimonGame(App):
    ENABLE_COMMAND_PALETTE = False

    BINDINGS = [(color[0], f"press_button('{color}')") for color in COLORS]

    CSS = """
    Screen {
        align: center middle;
    }

    #button-grid {
        height: 16;
        width: 32;
        grid-size: 2;
    }

    ColorButton {
        &:odd {
            content-align: left bottom;
        }

        &:first-of-type {
            content-align: left top;
        }

        &:even {
            content-align: right top;
        }

        &:last-of-type {
            content-align: right bottom;
        }
    }
    """

    def compose(self) -> ComposeResult:
        with Grid(id="button-grid"):
            for color in COLORS:
                yield ColorButton(color)

    def action_press_button(self, color: str) -> None:
        button = self.query_one(f"#{color}-btn", Button)
        button.press()


if __name__ == "__main__":
    game = SimonGame()
    game.run()
