import subprocess
import sys
import os
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional
import keyboard


from ..interface.style_manager import load_stylesheet
from .action import Action
from .action import ActionType
from .actionRunner import ActionRunner
from .hudActions import HudActions
from ..interface.macroDialog import MacroConfigDialog
from ..interface.mainHud import ActionDeckHUD
from ..interface.trayIcon import create_tray_icon
from ..interface.hotkeyWorker import HotkeyWorker




from PySide6.QtCore import (
    QObject,
    Qt,
    QTimer,
    Signal,
)

from PySide6.QtGui import (
    QAction,
    QColor,
    QFont,
    QIcon,
    QKeyEvent,
    QPainter,
    QPixmap,
)

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QMessageBox
)



def main() -> int:

    app = QApplication(sys.argv)


    
    app.setQuitOnLastWindowClosed(False)

    
    # =========================================================
    # ACTIONS
    # =========================================================

    sample_deck: Dict[
        str,
        Action,
    ] = {

        "Q": Action(
            ActionType.LAUNCH_APP,
            "notepad.exe",
            "Notepad",
            "Q",
        ),

        "W": Action(
            ActionType.LAUNCH_APP,
            "mspaint.exe",
            "Paint",
            "W",
        ),

        "E": Action(
            ActionType.LAUNCH_APP,
            "calc.exe",
            "Calculator",
            "E",
        ),

        "R": Action(
            ActionType.DEBUG_PRINT,
            "Terminal Reloaded",
            "Terminal",
            "R",
        ),

        "1": Action(
            ActionType.MEDIA_CONTROL,
            "previous track",
            "Previous",
            "1",
        ),

        "2": Action(
            ActionType.MEDIA_CONTROL,
            "play/pause",
            "Play / Pause",
            "2",
        ),

        "3": Action(
            ActionType.MEDIA_CONTROL,
            "next track",
            "Next",
            "3",
        ),

        "4": Action(
            ActionType.MEDIA_CONTROL,
            "volume up",
            "Vol +",
            "4",
        ),

        "5": Action(
            ActionType.MEDIA_CONTROL,
            "volume down",
            "Vol -",
            "5",
        ),

        "B": Action(
            ActionType.HUD_ACTION,
            "",
            "Exit",
            "B",
        ),
    }

    # =========================================================
    # HUD
    # =========================================================

    hud = ActionDeckHUD(
        sample_deck
    )

    hud.center_on_screen()
    hud.show()
    hud.activateWindow()#ativar tela

    # =========================================================
    # HUD ACTIONS
    # =========================================================

    hud_actions = HudActions(
        sample_deck["B"]
    )

    # Entrega HudActions ao Runner
    ActionRunner.set_hud_actions(
        hud_actions
    )

    # Conecta o contador ao tile B
    b_tile = hud.tiles["B"]

    hud_actions.label_changed.connect(
        b_tile.update_action_label
    )

    # =========================================================
    # CONFIG MENU
    # =========================================================

    def open_config_menu() -> None:

        if hud.isVisible():

            hud.hide()

        dialog = MacroConfigDialog(
            sample_deck,
            hud,
        )

        dialog.exec()

        hud.refresh_grid()

    # =========================================================
    # SYSTEM TRAY
    # =========================================================

    tray_icon = create_tray_icon(
        app
    )

    tray_menu = QMenu()

    # ---------------------------------------------------------
    # Config
    # ---------------------------------------------------------

    action_config = QAction(
        "Configurar Macros (Ctrl+M)",
        app,
    )

    action_config.triggered.connect(
        open_config_menu
    )

    tray_menu.addAction(
        action_config
    )

    tray_menu.addSeparator()

    # ---------------------------------------------------------
    # Abrir HUD
    # ---------------------------------------------------------

    action_show = QAction(
        "Abrir HUD (Ctrl+Espaço)",
        app,
    )

    action_show.triggered.connect(
        hud.toggle_visibility
    )

    tray_menu.addAction(
        action_show
    )

    tray_menu.addSeparator()

    # ---------------------------------------------------------
    # Sair
    # ---------------------------------------------------------

    action_quit = QAction(
        "Sair",
        app,
    )

    action_quit.triggered.connect(
        app.quit
    )

    tray_menu.addAction(
        action_quit
    )

    tray_icon.setContextMenu(
        tray_menu
    )

    tray_icon.setToolTip(
        "ActionDeck"
    )

    tray_icon.show()

    # =========================================================
    # HOTKEYS
    # =========================================================

    hotkey_worker = HotkeyWorker()

    def handle_hotkey(
        action_type: str,
    ) -> None:

        if action_type == "hud":

            hud.toggle_visibility()

        elif action_type == "config":

            open_config_menu()

    hotkey_worker.hotkey_triggered.connect(
        handle_hotkey
    )

    if not hotkey_worker.start():

        print(
            ">>> [WARNING] "
            "Não foi possível registrar os "
            "atalhos globais."
        )

    # =========================================================
    # CLEANUP
    # =========================================================

    def cleanup() -> None:

        print(
            ">>> [ActionDeck] Encerrando..."
        )

        hotkey_worker.stop()

        tray_icon.hide()

    app.aboutToQuit.connect(
        cleanup
    )

    # =========================================================
    # INFO
    # =========================================================

    print()

    print(
        "========================================"
    )

    print(
        "           ACTIONDECK - WINDOWS"
    )

    print(
        "========================================"
    )

    print(
        "Ctrl + Espaço  -> Abrir/fechar HUD"
    )

    print(
        "Ctrl + M       -> Configurar macros"
    )

    print(
        "ESC            -> Fechar HUD"
    )

    print(
        "B              -> Iniciar/cancelar Exit"
    )

    print(
        "========================================"
    )

    print()

    return app.exec()



