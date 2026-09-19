from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional


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
    QMessageBox,
)               

from .style_manager import load_stylesheet
from ..interface.mainHud import ActionDeckHUD   
from ..core.action import Action



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