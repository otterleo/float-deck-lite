from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional
import keyboard


from ..interface.style_manager import load_stylesheet
from ..core.action import Action
from ..core.action import ActionType
from ..core.actionRunner import ActionRunner
from ..core.hudActions import HudActions
from ..interface.macroDialog import MacroConfigDialog
from ..interface.mainHud import ActionDeckHUD
from ..interface.trayIcon import create_tray_icon



from PySide6.QtCore import (
    QObject,
    Qt,
    QTimer,
    Signal,
)


class HotkeyWorker(QObject):

    hotkey_triggered = Signal(
        str
    )

    def __init__(self):
        super().__init__()

        self.hotkeys = []

    def _hud_callback(
        self,
    ) -> None:

        self.hotkey_triggered.emit(
            "hud"
        )

    def _config_callback(
        self,
    ) -> None:

        self.hotkey_triggered.emit(
            "config"
        )

    def start(
        self,
    ) -> bool:

        try:

            hud_hotkey = keyboard.add_hotkey(
                "ctrl+space",
                self._hud_callback,
            )

            config_hotkey = keyboard.add_hotkey(
                "ctrl+m",
                self._config_callback,
            )

            self.hotkeys = [
                hud_hotkey,
                config_hotkey,
            ]

            print(
                ">>> [HOTKEY] "
                "Ctrl + Espaço registrado."
            )

            print(
                ">>> [HOTKEY] "
                "Ctrl + M registrado."
            )

            return True

        except Exception as exc:

            print(
                f">>> [ERRO HOTKEY] "
                f"{exc}"
            )

            return False

    def stop(
        self,
    ) -> None:

        for hotkey_handle in self.hotkeys:

            try:

                keyboard.remove_hotkey(
                    hotkey_handle
                )

            except Exception as exc:

                print(
                    f">>> [WARNING] "
                    f"Erro removendo hotkey: "
                    f"{exc}"
                )

        self.hotkeys.clear()
