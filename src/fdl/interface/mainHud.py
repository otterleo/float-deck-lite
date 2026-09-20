from dataclasses import dataclass
from typing import Any, Dict, Optional

from PySide6.QtCore import Qt, QTimer

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

from PySide6.QtGui import (
    QAction,
    QColor,
    QFont,
    QIcon,
    QKeyEvent,
    QPainter,
    QPixmap,
)

from ..core.action import Action
from .style_manager import load_stylesheet
from ..interface.keyTile import KeyTile

from ..core.hudActions import HudActions
from ..core.action import ActionType
from ..core.actionRunner import ActionRunner



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

        container.setStyleSheet(load_stylesheet())

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

                tile.triggered.connect(
                    lambda tile=tile:
                        self.execute_tile(tile)
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

    #
    # Ativa
    #

    def execute_tile(self, tile: KeyTile) -> None:

        tile.trigger_visual_feedback()

        action = tile.action

        if action is None:
            return

        QTimer.singleShot(
            50,
            lambda action=action:
                ActionRunner.execute(action)
        )

        if (
            self.auto_close_on_execute
            and action.action_type != ActionType.HUD_ACTION
        ):
            QTimer.singleShot(
                70,
                self.hide
            )
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

###
        tile = self.tiles[key_text]

        self.execute_tile(tile)

        event.accept()
###

