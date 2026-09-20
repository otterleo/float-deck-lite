import sys
from typing import Any, Dict, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont 

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



from ..core.action import Action
from .style_manager import load_stylesheet

class KeyTile(QPushButton):

    triggered = Signal()

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

        self.clicked.connect(self.on_clicked)

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

    def set_default_style(self) -> None:

        self.setProperty("feedback", False)
        

        self.style().unpolish(self)
        self.style().polish(self)

    # ---------------------------------------------------------
    # Feedback visual
    # ---------------------------------------------------------

    def trigger_visual_feedback(self) -> None:

        self.setProperty("feedback", True)

        print(f">>> [KeyTile] Triggered: {self.key_char}")
        
        
    

        self.style().unpolish(self)
        self.style().polish(self)

        QTimer.singleShot(
            120,
            self.set_default_style,
        )

        

    def on_clicked(self, checked: bool = False) -> None:
        self.triggered.emit()

    