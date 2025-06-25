import tkinter
from typing import Union, Tuple, Any, List


class Utils:
    __scaling_factor = 1  # Private class variable to scale dimensions (can be adjusted if needed)

    @staticmethod
    def _required_width(text: Any, font: Tuple[str, int, str]) -> float:
        """
        Calculate the required width for a given text and font.

        Args:
            text (Any): The text to measure.
            font (Tuple[str, int, str]): The font used for the label.

        Returns:
            float: The required width.
        """
        label = tkinter.Label(font=font, text=str(text))
        return label.winfo_reqwidth() / Utils.__scaling_factor

    @staticmethod
    def _required_height(text: Any, font: Tuple[str, int, str]) -> float:
        """
        Calculate the required height for a given text and font.

        Args:
            text (Any): The text to measure.
            font (Tuple[str, int, str]): The font used for the label.

        Returns:
            float: The required height.
        """
        label = tkinter.Label(font=font, text=str(text))
        return label.winfo_reqheight() / Utils.__scaling_factor

    @staticmethod
    def _format_float_with_precision(value: Union[float, int], decimals: int) -> str:
        """
        Format a float value to a fixed number of decimal places with trailing zeros.

        Args:
            value (float | int): The value to format.
            decimals (int): The number of decimal places.

        Returns:
            str: The formatted string.
        """
        if decimals > 0:
            value = round(float(value), decimals)
            value_str = str(value)
            decimals_part = value_str.split(".")[-1]
            padded = value_str + "0" * (decimals - len(decimals_part))
            return padded
        return str(int(value))

    @staticmethod
    def _get_max_required_label_width(data: List[Any], font: Tuple[str, int, str]) -> float:
        """
        Get the maximum required width among multiple text labels.

        Args:
            data (List[Any]): A list of text values.
            font (Tuple[str, int, str]): Font for the labels.

        Returns:
            float: Maximum required width.
        """
        return max(Utils._required_width(d, font) for d in data)

    @staticmethod
    def _get_max_required_label_height(data: List[Any], font: Tuple[str, int, str]) -> float:
        """
        Get the maximum required height among multiple text labels.

        Args:
            data (List[Any]): A list of text values.
            font (Tuple[str, int, str]): Font for the labels.

        Returns:
            float: Maximum required height.
        """
        return max(Utils._required_height(d, font) for d in data)

    @staticmethod
    def _sort_tuple(values: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Sort and deduplicate a tuple of integers.

        Args:
            values (Tuple[int, ...]): The input tuple.

        Returns:
            Tuple[int, ...]: A sorted, unique tuple.
        """
        return tuple(sorted(set(values)))

    @staticmethod
    def _to_int(value: Union[int, str]) -> int:
        """
        Convert a value to integer.

        Args:
            value (int | str): The value to convert.

        Returns:
            int: The integer result.
        """
        return int(value)
