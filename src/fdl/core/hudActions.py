from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QApplication
from .action import Action
from .action import ActionType


class HudActions(QObject):

    # Envia o novo texto para o KeyTile
    label_changed = Signal(str)

    def __init__(
        self,
        action: Action,
    ):
        super().__init__()

        self.action = action

        # Estado do Exit
        self._stExit = False

        # Contador
        self._exit_count = 2

        # Timer do Qt
        self._exit_timer = QTimer(self)

        self._exit_timer.setInterval(
            1000
        )

        self._exit_timer.timeout.connect(
            self._update_exit_timer
        )

    # ---------------------------------------------------------
    # Getter
    # ---------------------------------------------------------

    @property
    def stExit(self) -> bool:
        return self._stExit

    # ---------------------------------------------------------
    # Setter
    # ---------------------------------------------------------

    @stExit.setter
    def stExit(
        self,
        value: bool,
    ) -> None:

        self._stExit = value

        if value:
            self.exit_app()
        else:
            self.cancel_exit()

    # ---------------------------------------------------------
    # Inicia contador
    # ---------------------------------------------------------

    def exit_app(self) -> None:

        print(
            ">>> [HUD] Exit iniciado."
        )

        self._exit_count = 2

        self._set_label(
            f"Exit ({self._exit_count})"
        )

        self._exit_timer.start()

    # ---------------------------------------------------------
    # Cancela contador
    # ---------------------------------------------------------

    def cancel_exit(self) -> None:

        print(
            ">>> [HUD] Exit cancelado."
        )

        self._exit_timer.stop()

        self._set_label(
            "Exit"
        )

    # ---------------------------------------------------------
    # Atualiza contador
    # ---------------------------------------------------------

    def _update_exit_timer(self) -> None:

        self._exit_count -= 1

        print(
            f">>> [HUD] Contador: "
            f"{self._exit_count}"
        )

        # Chegou ao final
        if self._exit_count <= 0:

            self._exit_timer.stop()

            self._set_label(
                "Exit (0)"
            )

            print(
                ">>> [EXIT] Saindo..."
            )

            # Fecha a aplicação Qt
            QApplication.quit()

            return

        # Atualiza texto
        self._set_label(
            f"Exit ({self._exit_count})"
        )

    # ---------------------------------------------------------
    # Atualiza Action + interface
    # ---------------------------------------------------------

    def _set_label(
        self,
        text: str,
    ) -> None:

        # Atualiza o Action
        self.action.label = text

        # Avisa o KeyTile
        self.label_changed.emit(
            text
        )