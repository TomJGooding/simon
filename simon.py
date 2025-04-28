import random
from asyncio import sleep

from textual import work
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

    def flash(self) -> None:
        self._start_active_affect()


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

    def __init__(self) -> None:
        super().__init__()
        self.flashed_buttons: list[str] = []
        self.pressed_buttons: list[str] = []

    def compose(self) -> ComposeResult:
        with Grid(id="button-grid"):
            for color in COLORS:
                yield ColorButton(color)

    def on_mount(self) -> None:
        self.play_round()

    def play_round(self) -> None:
        # TODO: Add a new color to the sequence each round
        self.random_sequence()

        self.flash_buttons()

    def random_sequence(self) -> None:
        color_buttons = self.query(ColorButton)
        for _ in range(4):
            random_button = random.choice(color_buttons)
            assert random_button.id is not None
            self.flashed_buttons.append(random_button.id)

    @work(exclusive=True)
    async def flash_buttons(self) -> None:
        for button in self.flashed_buttons:
            await sleep(1)
            self.query_one(f"#{button}", ColorButton).flash()

    def on_button_pressed(self, event: ColorButton.Pressed) -> None:
        button = event.button
        assert button.id is not None
        self.pressed_buttons.append(button.id)

        if len(self.pressed_buttons) == len(self.flashed_buttons):
            if self.pressed_buttons == self.flashed_buttons:
                self.notify("You win!")
            else:
                self.notify("You lose!", severity="error")

    def action_press_button(self, color: str) -> None:
        button = self.query_one(f"#{color}-btn", Button)
        button.press()


if __name__ == "__main__":
    game = SimonGame()
    game.run()
