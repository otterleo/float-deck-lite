import subprocess
import sys
import os
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional

import keyboard

from .hudActions import HudActions

from .action import Action
from .action import ActionType


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