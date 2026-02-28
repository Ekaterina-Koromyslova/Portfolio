import curses
from src.controller.game_controller import GameController
from src.datalayer.save_manager import JsonDataService
from src.presentation.app import run

# from domain.game_logic import (
#     DomainLevelGenerator, DomainMovement, DomainCombat, DomainConsumables,
# )
# from presentation.curses_ui import (
#     CursesPresentation, CursesMapRenderer, CursesScreenRenderer,
# )


def main() -> None:
    data_service = JsonDataService()

    # TODO: заменить заглушки
    # presentation = CursesPresentation()
    # map_renderer = CursesMapRenderer()
    # screen_renderer = CursesScreenRenderer()
    # level_gen = DomainLevelGenerator()
    # movement = DomainMovement()
    # combat = DomainCombat()
    # consumables = DomainConsumables()

    # controller = GameController(
    #     presentation=presentation,
    #     map_renderer=map_renderer,
    #     screen_renderer=screen_renderer,
    #     level_generator=level_gen,
    #     movement=movement,
    #     combat=combat,
    #     consumables=consumables,
    #     data_service=data_service,
    # )
    # controller.run()


if __name__ == "__main__":
    main()
