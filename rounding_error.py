#!/usr/bin/python3
# SPDX-FileCopyrightText: 2025 Yusaku Aka
# SPDX-License-Identifier: BSD-3-Clause

from decimal import Decimal, getcontext, ROUND_HALF_UP

getcontext().prec = 50

class ErrorValue:
    def __init__(self, value_str):
        self.value_str = value_str
        self.value = Decimal(value_str)
        self.error = self._calculate_initial_error()

    def _calculate_initial_error(self):
        if '.' in self.value_str:
            decimal_part = self.value_str.split('.')[-1]
            num_decimals = len(decimal_part)
            error_power = -num_decimals
        else:
            error_power = 0

        return Decimal('0.5') * (Decimal(10) ** error_power)

    def __add__(self, other):
        if not isinstance(other, ErrorValue):
            raise TypeError("ErrorValue can only be added to another ErrorValue.")

        new_value = self.value + other.value
        new_error = self.error + other.error

        result = ErrorValue(str(new_value))
        result.value = new_value
        result.error = new_error
        return result

    def format_output(self):
        error_exponent = self.error.as_tuple().exponent

        rounding_point = error_exponent * (-1)

        quantizer = Decimal(10) ** (error_exponent)
        rounded_value = self.value.quantize(quantizer, rounding=ROUND_HALF_UP)

        if rounding_point <= 0:
            formatted_value = str(int(rounded_value))
            formatted_error = f"{self.error.normalize():g}"
        else:
            formatted_value = f"{rounded_value:.{rounding_point}f}"
            formatted_error = f"{self.error:.{rounding_point}f}"


        return f"{formatted_value} ± {formatted_error}"

def run_simple_calculator():
    input_str = input("計算式を入力してください（例: 1+2.0+3.0）: ")

    parts = [p.strip() for p in input_str.split('+') if p.strip()]

    if not parts:
        print("有効な入力がありませんでした。")
        return

    try:
        current_result = ErrorValue(parts[0])

        for part in parts[1:]:
            next_value = ErrorValue(part)
            current_result = current_result + next_value

        # 最終結果の出力のみ
        print(f"計算結果: {current_result.format_output()}")

    except Exception as e:
        print(f"\nエラーが発生しました。入力形式を確認してください。({e})")


if __name__ == "__main__":
    run_simple_calculator()
