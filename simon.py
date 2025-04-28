import random
from asyncio import sleep

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Center, Grid, VerticalGroup
from textual.reactive import reactive
from textual.widgets import Button, Digits, Static

SIMON_LOGO = """\
▄▄▄ ▄ ▄▄▄▄▄ ▄▄▄ ▄▄▄
█▄▄ █ █ █ █ █ █ █ █
▄▄█ █ █ █ █ █▄█ █ █\
"""

COLORS = ["green", "red", "yellow", "blue"]


class ColorButton(Button, can_focus=False, inherit_css=False):
    DEFAULT_CSS = """
    ColorButton {
        min-width: 24;
        min-height: 12;
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
        width: 48;
        height: 24;
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

    #center-panel {
        layer: center-panel;
        align: center middle;
        width: 24;
        height: 12;
        padding: 1;
    }

    #logo {
        text-align: center;
    }

    #score {
        text-style: bold;
        background: $surface-lighten-2;
        width: 8;
        padding: 0 1;
        margin-top: 1;
    }
    """

    flashed_buttons: list[str] = []
    pressed_buttons: list[str] = []
    score: reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        with Grid(id="button-grid"):
            for color in COLORS:
                yield ColorButton(color)

        with VerticalGroup(id="center-panel"):
            yield Static(SIMON_LOGO, id="logo")
            with Center():
                yield Digits(id="score")

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
                self.score += 1
                self.notify("You win!")
            else:
                self.score = 0
                self.notify("You lose!", severity="error")

    def watch_score(self) -> None:
        self.query_one("#score", Digits).update(f"{self.score:02}")

    def action_press_button(self, color: str) -> None:
        button = self.query_one(f"#{color}-btn", Button)
        button.press()


if __name__ == "__main__":
    game = SimonGame()
    game.run()
