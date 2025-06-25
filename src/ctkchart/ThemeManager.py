import customtkinter as ctk
import time
import threading
from typing import List, Tuple, Any, Union


class ThemeManager:
    running_state: bool = False
    child_objects: List[Any] = []
    theme: str = "-"

    @staticmethod
    def get_color_by_theme(color: Union[Tuple[str, str], str]) -> str:
        """
        Returns the appropriate color based on the current theme.

        Args:
            color (Tuple[str, str] | str): A tuple of (light_color, dark_color) or a single color string.

        Returns:
            str: The color corresponding to the current theme.
        """
        if isinstance(color, tuple):
            return color[0] if ThemeManager.theme == "Light" else color[1]
        return color

    @staticmethod
    def theme_tracker() -> None:
        """
        Monitors and applies theme changes across all registered widgets.
        """
        while ThemeManager.child_objects:
            current_theme = ctk.get_appearance_mode()
            if current_theme != ThemeManager.theme:
                ThemeManager.theme = current_theme
                for widget in ThemeManager.child_objects:
                    try:
                        widget._CTkLineChart__configure_theme_mode()
                    except Exception as e:
                        print(f"[ThemeManager] Theme update failed for widget: {e}")
            time.sleep(1)

        ThemeManager.running_state = False

    @staticmethod
    def run() -> None:
        """
        Starts the background theme tracking thread if not already running.
        """
        if not ThemeManager.running_state:
            ThemeManager.running_state = True
            thread = threading.Thread(target=ThemeManager.theme_tracker, daemon=True)
            thread.start()

    @staticmethod
    def bind_widget(widget: Any) -> None:
        """
        Registers a widget with the theme manager.

        Args:
            widget (Any): Widget instance with a `_CTkLineChart__configure_theme_mode` method.
        """
        ThemeManager.child_objects.append(widget)
        if not ThemeManager.running_state:
            ThemeManager.run()

    @staticmethod
    def unbind_widget(widget: Any) -> None:
        """
        Unregisters a widget from the theme manager.

        Args:
            widget (Any): The widget to remove.
        """
        try:
            ThemeManager.child_objects.remove(widget)
        except ValueError:
            print(f"[ThemeManager] Widget not found.")
        except Exception as e:
            print(f"[ThemeManager] Error removing widget: {e}")
