import subprocess
import sys
import os
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional


from  ..interface.style_manager import load_stylesheet

import keyboard

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


# =============================================================
# 1. ACTION DEFINITIONS
# =============================================================

class ActionType(Enum):
    HUD_ACTION = auto()
    LAUNCH_APP = auto()
    DEBUG_PRINT = auto()
    MEDIA_CONTROL = auto()


@dataclass
class Action:
    action_type: ActionType
    payload: Any
    label: str
    key: str


# =============================================================
# 2. HUD ACTIONS
# =============================================================

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


# =============================================================
# 3. ACTION RUNNER
# =============================================================

class ActionRunner:

    # Referência global para HudActions
    hud_actions: Optional[HudActions] = None

    # ---------------------------------------------------------
    # Configura HudActions
    # ---------------------------------------------------------

    @classmethod
    def set_hud_actions(
        cls,
        hud_actions: HudActions,
    ) -> None:

        cls.hud_actions = hud_actions

    # ---------------------------------------------------------
    # Executa Action
    # ---------------------------------------------------------

    @classmethod
    def execute(
        cls,
        action: Action,
    ) -> None:

        # -----------------------------------------------------
        # LAUNCH APP
        # -----------------------------------------------------

        if action.action_type == ActionType.LAUNCH_APP:

            try:

                subprocess.Popen(
                    action.payload,
                    shell=False,
                )

                print(
                    f">>> [APP] "
                    f"{action.label} iniciado."
                )

            except FileNotFoundError:

                print(
                    f">>> [ERRO] "
                    f"Aplicativo não encontrado: "
                    f"{action.payload}"
                )

            except Exception as exc:

                print(
                    f">>> [ERRO] "
                    f"Não foi possível iniciar "
                    f"{action.payload}: {exc}"
                )

        # -----------------------------------------------------
        # DEBUG PRINT
        # -----------------------------------------------------

        elif action.action_type == ActionType.DEBUG_PRINT:

            print(
                f">>> [ACTION] "
                f"{action.payload}"
            )

        # -----------------------------------------------------
        # MEDIA CONTROL
        # -----------------------------------------------------

        elif action.action_type == ActionType.MEDIA_CONTROL:

            try:

                keyboard.send(
                    action.payload
                )

                print(
                    f">>> [MEDIA] "
                    f"{action.label} "
                    f"({action.payload})"
                )

            except Exception as exc:

                print(
                    f">>> [ERRO MEDIA] "
                    f"{action.payload}: {exc}"
                )

        # -----------------------------------------------------
        # HUD ACTION
        # -----------------------------------------------------

        elif action.action_type == ActionType.HUD_ACTION:

            try:

                if cls.hud_actions is None:

                    print(
                        ">>> [ERRO] "
                        "HudActions não configurado."
                    )

                    return

                # Toggle True / False
                cls.hud_actions.stExit = (
                    not cls.hud_actions.stExit
                )

            except Exception as exc:

                print(
                    f">>> [ERRO HUD] "
                    f"{exc}"
                )


# =============================================================
# 4. KEY TILE
# =============================================================

class KeyTile(QFrame):

    def __init__(
        self,
        key_char: str,
        action: Optional[Action] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(
            parent
        )

        self.key_char = key_char
        self.action = action
        
        

        self.setFixedSize(
            84,
            84,
        )

        self.setObjectName(
            "KeyTile"
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        layout.setSpacing(
            4
        )

        # -----------------------------------------------------
        # Tecla
        # -----------------------------------------------------

        self.key_label = QLabel(
            key_char
        )

        self.key_label.setFont(
            QFont(
                "Consolas",
                11,
                QFont.Weight.Bold,
            )
        )

        self.key_label.setAlignment(
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignLeft
        )

        # -----------------------------------------------------
        # Action label
        # -----------------------------------------------------

        action_text = (
            action.label
            if action
            else "—"
        )

        self.action_label = QLabel(
            action_text
        )

        self.action_label.setFont(
            QFont(
                "Segoe UI",
                9,
            )
        )

        self.action_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.action_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.key_label
        )

        layout.addWidget(
            self.action_label
        )

        self.setStyleSheet(load_stylesheet())

    # ---------------------------------------------------------
    # Atualiza label
    # ---------------------------------------------------------

    def update_action_label(
        self,
        text: str,
    ) -> None:

        self.action_label.setText(
            text
        )

    # ---------------------------------------------------------
    # Estilo padrão
    # ---------------------------------------------------------

    def set_default_style(
        self,
    ) -> None:

        if self.action:

            active_border = "#3e4451"
            bg_color = "#282c34"
            text_color = "#abb2bf"

        else:

            active_border = "#21252b"
            bg_color = "#1a1d23"
            text_color = "#4b5263"

        self.setStyleSheet(load_stylesheet())

        

    # ---------------------------------------------------------
    # Feedback visual
    # ---------------------------------------------------------

    def trigger_visual_feedback(
        self,
    ) -> None:

        self.setStyleSheet(load_stylesheet())

        self.repaint()

        QTimer.singleShot(
            120,
            self.set_default_style,
        )


# =============================================================
# 5. CONFIGURATION DIALOG
# =============================================================

class MacroConfigDialog(QDialog):

    def __init__(
        self,
        actions: Dict[str, Action],
        parent: Optional[QWidget] = None,
    ):
        super().__init__(
            parent
        )

        self.actions = actions

        self.hud = (
            parent
            if isinstance(
                parent,
                ActionDeckHUD,
            )
            else None
        )

        self.setWindowTitle(
            "Configurar Macros"
        )

        self.setMinimumSize(
            650,
            480,
        )

        self.setStyleSheet(load_stylesheet())

        layout = QVBoxLayout(
            self
        )

        # -----------------------------------------------------
        # Título
        # -----------------------------------------------------

        title = QLabel(
            "Macros Ativas"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Weight.Bold,
            )
        )

        layout.addWidget(
            title
        )

        # -----------------------------------------------------
        # Tabela
        # -----------------------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Tecla",
                "Nome",
                "Tipo",
                "Payload",
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        layout.addWidget(
            self.table
        )

        self.populate_table()

        # -----------------------------------------------------
        # Opções
        # -----------------------------------------------------

        self.auto_close_checkbox = QCheckBox(
            "Fechar HUD automaticamente após executar uma macro"
        )

        if self.hud:

            self.auto_close_checkbox.setChecked(
                self.hud.auto_close_on_execute
            )

        self.auto_close_checkbox.toggled.connect(
            self.toggle_auto_close
        )

        layout.addWidget(
            self.auto_close_checkbox
        )

        # -----------------------------------------------------
        # Botões
        # -----------------------------------------------------

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        close_button = QPushButton(
            "Fechar"
        )

        close_button.clicked.connect(
            self.accept
        )

        button_layout.addWidget(
            close_button
        )

        layout.addLayout(
            button_layout
        )

    # ---------------------------------------------------------
    # Toggle auto close
    # ---------------------------------------------------------

    def toggle_auto_close(
        self,
        checked: bool,
    ) -> None:

        if self.hud:

            self.hud.auto_close_on_execute = (
                checked
            )

    # ---------------------------------------------------------
    # Preenche tabela
    # ---------------------------------------------------------

    def populate_table(
        self,
    ) -> None:

        self.table.clearContents()

        self.table.setRowCount(
            len(self.actions)
        )

        for row, (
            key,
            action,
        ) in enumerate(
            self.actions.items()
        ):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    key
                ),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    action.label
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    action.action_type.name
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(action.payload)
                ),
            )


# =============================================================
# 6. MAIN HUD
# =============================================================

class ActionDeckHUD(QWidget):

    GRID_LAYOUT = [
        ["1", "2", "3", "4", "5"],
        ["Q", "W", "E", "R", "T"],
        ["A", "S", "D", "F", "G"],
        ["Z", "X", "C", "V", "B"],
    ]

    def __init__(
        self,
        actions: Dict[str, Action],
        parent: Optional[QWidget] = None,
    ):
        super().__init__(
            parent
        )

        self.actions = actions

        self.auto_close_on_execute = True

        self.tiles: Dict[
            str,
            KeyTile,
        ] = {}

        self.init_window()

        self.init_grid()

    # ---------------------------------------------------------
    # Janela
    # ---------------------------------------------------------

    def init_window(
        self,
    ) -> None:

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        shadow = QGraphicsDropShadowEffect(
            self
        )

        shadow.setBlurRadius(
            30
        )

        shadow.setColor(
            QColor(
                0,
                0,
                0,
                180,
            )
        )

        shadow.setOffset(
            0,
            8,
        )

        self.setGraphicsEffect(
            shadow
        )

    # ---------------------------------------------------------
    # Grid
    # ---------------------------------------------------------

    def init_grid(
        self,
    ) -> None:

        old_layout = self.layout()

        if old_layout is not None:

            while old_layout.count():

                item = old_layout.takeAt(
                    0
                )

                widget = item.widget()

                if widget is not None:

                    widget.deleteLater()

            QWidget().setLayout(
                old_layout
            )

        outer_layout = QVBoxLayout(
            self
        )

        outer_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        container = QFrame()

        container.setObjectName(
            "HUDContainer"
        )

        container.setStyleSheet(
            """
            QFrame#HUDContainer {
                background-color: #16181c;
                border-radius: 12px;
            }
            """
        )

        grid_layout = QGridLayout(
            container
        )

        grid_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        grid_layout.setSpacing(
            10
        )

        self.tiles.clear()

        for row_index, row in enumerate(
            self.GRID_LAYOUT
        ):

            for column_index, key in enumerate(
                row
            ):

                action = self.actions.get(
                    key
                )

                tile = KeyTile(
                    key,
                    action,
                    container,
                )

                self.tiles[
                    key
                ] = tile

                grid_layout.addWidget(
                    tile,
                    row_index,
                    column_index,
                )

        outer_layout.addWidget(
            container
        )

        self.adjustSize()

    # ---------------------------------------------------------
    # Atualiza grid
    # ---------------------------------------------------------

    def refresh_grid(
        self,
    ) -> None:

        self.init_grid()

        self.center_on_screen()

    # ---------------------------------------------------------
    # Centraliza
    # ---------------------------------------------------------

    def center_on_screen(
        self,
    ) -> None:

        screen = QApplication.primaryScreen()

        if screen is None:
            return

        geometry = (
            screen.availableGeometry()
        )

        self.adjustSize()

        x = (
            geometry.x()
            + (
                geometry.width()
                - self.width()
            )
            // 2
        )

        y = (
            geometry.y()
            + (
                geometry.height()
                - self.height()
            )
            // 2
        )

        self.move(
            x,
            y,
        )

    # ---------------------------------------------------------
    # Mostrar / esconder
    # ---------------------------------------------------------

    def toggle_visibility(
        self,
    ) -> None:

        if self.isVisible():

            self.hide()

            return

        self.center_on_screen()

        self.show()

        self.raise_()

        self.activateWindow()

        self.setFocus(
            Qt.FocusReason.OtherFocusReason
        )

    # ---------------------------------------------------------
    # Teclado
    # ---------------------------------------------------------

    def keyPressEvent(
        self,
        event: QKeyEvent,
    ) -> None:

        if event.isAutoRepeat():

            event.accept()

            return

        # -----------------------------------------------------
        # ESC
        # -----------------------------------------------------

        if event.key() == Qt.Key.Key_Escape:

            self.hide()

            event.accept()

            return

        # -----------------------------------------------------
        # Tecla
        # -----------------------------------------------------

        key_text = (
            event.text()
            .upper()
            .strip()
        )

        if not key_text:

            key_map = {

                Qt.Key.Key_1: "1",
                Qt.Key.Key_2: "2",
                Qt.Key.Key_3: "3",
                Qt.Key.Key_4: "4",
                Qt.Key.Key_5: "5",

                Qt.Key.Key_Q: "Q",
                Qt.Key.Key_W: "W",
                Qt.Key.Key_E: "E",
                Qt.Key.Key_R: "R",
                Qt.Key.Key_T: "T",

                Qt.Key.Key_A: "A",
                Qt.Key.Key_S: "S",
                Qt.Key.Key_D: "D",
                Qt.Key.Key_F: "F",
                Qt.Key.Key_G: "G",

                Qt.Key.Key_Z: "Z",
                Qt.Key.Key_X: "X",
                Qt.Key.Key_C: "C",
                Qt.Key.Key_V: "V",
                Qt.Key.Key_B: "B",
            }

            key_text = key_map.get(
                event.key(),
                "",
            )

        if key_text not in self.tiles:

            event.ignore()

            return

        tile = self.tiles[
            key_text
        ]

        tile.trigger_visual_feedback()

        action = self.actions.get(
            key_text
        )

        if action is not None:

            # Executa a ação
            QTimer.singleShot(
                50,
                lambda action=action:
                    ActionRunner.execute(
                        action
                    ),
            )

            # -------------------------------------------------
            # Não fecha o HUD para HUD_ACTION
            # -------------------------------------------------

            if (
                self.auto_close_on_execute
                and action.action_type
                != ActionType.HUD_ACTION
            ):

                QTimer.singleShot(
                    70,
                    self.hide,
                )

        event.accept()


# =============================================================
# 7. GLOBAL HOTKEY WORKER
# =============================================================

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


# =============================================================
# 8. SYSTEM TRAY
# =============================================================

def create_tray_icon(
    app: QApplication,
) -> QSystemTrayIcon:

    tray_icon = QSystemTrayIcon(
        app
    )

    pixmap = QPixmap(
        32,
        32,
    )

    pixmap.fill(
        QColor(
            40,
            44,
            52,
        )
    )

    painter = QPainter(
        pixmap
    )

    painter.setPen(
        QColor(
            97,
            175,
            239,
        )
    )

    painter.setFont(
        QFont(
            "Segoe UI",
            12,
            QFont.Weight.Bold,
        )
    )

    painter.drawText(
        pixmap.rect(),
        Qt.AlignmentFlag.AlignCenter,
        "M",
    )

    painter.end()

    tray_icon.setIcon(
        QIcon(
            pixmap
        )
    )

    return tray_icon


# =============================================================
# 9. MAIN
# =============================================================

def main() -> int:

    app = QApplication(
        sys.argv
    )

    app.setQuitOnLastWindowClosed(
        False
    )

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

##########################

