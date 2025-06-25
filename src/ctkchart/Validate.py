from typing import Tuple, Any
from .FontStyle import FontStyle
import tkinter


class Validate:
    @staticmethod
    def _error_font(value: str) -> str:
        """Return a formatted error message."""
        return FontStyle._apply(value, "red", "black", "underline")

    @staticmethod
    def _var_font(value: str) -> str:
        """Return a formatted variable name."""
        return FontStyle._apply(value, "green", "black", "italic")

    @staticmethod
    def _is_tuple(value: Any, var: str) -> None:
        """Check if value is a tuple."""
        if type(value) is not tuple:
            raise TypeError(f"{Validate._var_font(var)} {Validate._error_font('must be tuple.')}")

    @staticmethod
    def _is_list(value: Any, var: str) -> None:
        """Check if value is a list."""
        if type(value) is not list:
            raise TypeError(f"{Validate._var_font(var)} {Validate._error_font('must be list.')}")

    @staticmethod
    def _is_int(value: Any, var: str) -> None:
        """Check if value is an integer."""
        if type(value) is not int:
            raise TypeError(f"{Validate._var_font(var)} {Validate._error_font('must be int.')}")

    @staticmethod
    def _is_bool(value: Any, var: str) -> None:
        """Check if value is a boolean."""
        if type(value) is not bool:
            raise TypeError(f"{Validate._var_font(var)} {Validate._error_font('must be bool.')}")

    @staticmethod
    def _is_str(value: Any, var: str) -> None:
        """Check if value is a string."""
        if type(value) is not str:
            raise TypeError(f"{Validate._var_font(var)} {Validate._error_font('must be str.')}")

    @staticmethod
    def _is_valid_color(value: Any, var: str) -> None:
        """Check if value is a valid color string or tuple."""
        valid = True
        if type(value) is tuple and len(value) == 2:
            try:
                tkinter.Label(bg=value[0])
                tkinter.Label(bg=value[1])
            except:
                valid = False
        elif type(value) is str:
            try:
                tkinter.Label(bg=value)
            except:
                valid = False
        else:
            valid = False
        if not valid:
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be valid color. eg:- '#ff0000'/ 'red'/ ('#ffffff', '#000000')")}''')

    @staticmethod
    def _is_valid_font(value: Any, var: str) -> None:
        """Check if value is a valid font tuple."""
        Validate._is_tuple(value, var)
        try:
            tkinter.Label(font=value)
        except:
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be valid font. eg:- ('arial',10,'bold')")}''')

    @staticmethod
    def _is_valid_function(value: Any, var: str) -> None:
        """Check if value is a callable function or None."""
        if not callable(value) and value is not None:
            raise TypeError(f'''{Validate._var_font(var)} {Validate._error_font("must be function with two parameters or *args.")}''')

    @staticmethod
    def _is_valid_x_axis_indices(values: Tuple[Any, ...], indices: Tuple[int, ...], var: str) -> None:
        """Validate x-axis indices within bounds."""
        if indices is not None:
            Validate._is_tuple(indices, var)
            Validate._is_valid_indices(indices, var)
            for index in indices:
                if index >= len(values):
                    raise IndexError(f'''{Validate._var_font(var)} {Validate._error_font("values must be lower than length of x_axis_values.")}''')

    @staticmethod
    def _is_valid_x_axis_label_count(values: Any, var: str) -> None:
        """Check x-axis label count is an int."""
        if values is not None:
            Validate._is_int(values, var)

    @staticmethod
    def _is_valid_style_type(value: Any, var: str) -> None:
        """Check style type as a tuple of two integers."""
        Validate._is_tuple(value, var)
        if len(value) == 2 and isinstance(value[0], int) and isinstance(value[1], int):
            return
        elif len(value) != 2:
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("length must be two.")}''')
        else:
            raise TypeError(f'''{Validate._var_font(var)} {Validate._error_font("values must be integers.")}''')

    @staticmethod
    def _is_valid_data_position(value: Any, var: str) -> None:
        """Check if data position is 'top' or 'side'."""
        Validate._is_str(value, var)
        if value not in ("top", "side"):
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be 'top' or 'side'.")}''')

    @staticmethod
    def _is_valid_line_style(value: Any, var: str) -> None:
        """Check line style is 'normal', 'dotted' or 'dashed'."""
        Validate._is_str(value, var)
        if value not in ("normal", "dotted", "dashed"):
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be 'normal' or 'dotted' or 'dashed'.")}''')

    @staticmethod
    def _is_valid_section_style(value: Any, var: str) -> None:
        """Check section style is 'normal' or 'dashed'."""
        Validate._is_str(value, var)
        if value not in ("normal", "dashed"):
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be 'normal' or 'dashed'.")}''')

    @staticmethod
    def _is_valid_x_axis_point_spacing(value: Any, var: str) -> None:
        """Check point spacing is integer or 'auto'."""
        if isinstance(value, int) or (isinstance(value, str) and value == "auto"):
            return
        raise TypeError(f'''{Validate._var_font(var)} {Validate._error_font("must be integer or 'auto'.")}''')

    @staticmethod
    def _is_valid_pointer_state_lock(value: Any, var: str) -> None:
        """Check if pointer lock state is valid."""
        Validate._is_str(value, var)
        if value not in ("enabled", "disabled"):
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be 'disabled' or 'enabled'.")}''')

    @staticmethod
    def _is_valid_line_highlight(value: Any, var: str) -> None:
        """Check if line highlight is enabled or disabled."""
        Validate._is_str(value, var)
        if value not in ("enabled", "disabled"):
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be 'disabled' or 'enabled'.")}''')

    @staticmethod
    def _is_valid_line_fill(value: Any, var: str) -> None:
        """Check if line fill is enabled or disabled."""
        Validate._is_str(value, var)
        if value not in ("enabled", "disabled"):
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be 'disabled' or 'enabled'.")}''')

    @staticmethod
    def _is_valid_y_axis_values(value: Any, var: str) -> None:
        """Validate y-axis value tuple with two ascending numbers."""
        Validate._is_tuple(value, var)
        if value == (None, None):
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be provide.")}''')
        if len(value) != 2:
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("length must be two.")}''')
        if not all(isinstance(v, (int, float)) for v in value):
            raise TypeError(f'''{Validate._var_font(var)} {Validate._error_font("values must be integer or float.")}''')
        if value[0] >= value[1]:
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("first value must be less than second value.")}''')

    @staticmethod
    def _is_valid_x_axis_values(value: Any, var: str) -> None:
        """Check x-axis values are valid and not placeholders."""
        if value == (None, "None", None, "None"):
            raise ValueError(f'''{Validate._var_font(var)} {Validate._error_font("must be provide.")}''')
        Validate._is_tuple(value, var)

    @staticmethod
    def _is_valid_ctk_line(value: Any, var: str) -> None:
        """Check if value is instance of CTkLine."""
        from .CTkLine import CTkLine
        if type(value) is not CTkLine:
            raise TypeError(f'''{Validate._var_font(var)} {Validate._error_font("type must be ctkchart.CTkLine")}''')

    @staticmethod
    def _is_valid_ctk_line_chart(value: Any, var: str) -> None:
        """Check if value is instance of CTkLineChart."""
        from .CTkLineChart import CTkLineChart
        if type(value) is not CTkLineChart:
            raise TypeError(f'''{Validate._var_font(var)} {Validate._error_font("type must be ctkchart.CTkLineChart")}''')

    @staticmethod
    def _is_valid_data(value: Any, var: str) -> None:
        """Ensure list contains only numeric values."""
        Validate._is_list(value, var)
        if not all(isinstance(v, (int, float)) for v in value):
            raise TypeError(f'''{Validate._var_font(var)} {Validate._error_font("all values in the list should be either int or float.")}''')

    @staticmethod
    def _is_valid_indices(value: Any, var: str) -> None:
        """Ensure all indices are integers."""
        if not all(isinstance(v, int) for v in value):
            raise TypeError(f'''{Validate._var_font(var)} {Validate._error_font("all values should be int.")}''')

    @staticmethod
    def _invalid_cget(var: str) -> None:
        """Raise error for invalid attribute access."""
        raise TypeError(f'''{Validate._var_font(str(var))} {Validate._error_font("Invalid attribute.")}''')

    @staticmethod
    def _invalid_ctk_line(line) -> None:
        """Raise error when line not part of chart."""
        raise ValueError(f'''{Validate._var_font(str(line))} {Validate._error_font("The line is not part of this line chart.")}''')

    @staticmethod
    def _invalid_master(value):
        """Raise error for invalid chart master."""
        raise ValueError(f'''{Validate._var_font(str(value))} {Validate._error_font("Invalid Master for chart.")}''')

    @staticmethod
    def _master_att_not_provide_for_line(value):
        """Raise error when master not provided for line."""
        raise ValueError(f'''{Validate._var_font(str(value))} {Validate._error_font("master must be provide for CTkLine")}''')
