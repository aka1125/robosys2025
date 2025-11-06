#!/usr/bin/python3

from decimal import Decimal, getcontext, ROUND_HALF_UP

# decimalの精度
getcontext().prec = 50

class ErrorValue:
    #数値とその誤差（不確かさ）を保持するクラス
    def __init__(self, value_str):
        self.value_str = value_str
        self.value = Decimal(value_str)
        self.error = self._calculate_initial_error()

    def _calculate_initial_error(self):
        #入力値の末尾の桁から、対応する誤差を計算
        if '.' in self.value_str:
            decimal_part = self.value_str.split('.')[-1]
            num_decimals = len(decimal_part)
            error_power = -num_decimals
        else:
            error_power = 0

        return Decimal('0.5') * (Decimal(10) ** error_power)

    def __add__(self, other):
        """数値、誤差は単純和で伝播させる。"""
        if not isinstance(other, ErrorValue):
            raise TypeError("ErrorValue can only be added to another ErrorValue.")

        new_value = self.value + other.value
        new_error = self.error + other.error

        # 演算結果用の新しいオブジェクトを作成
        result = ErrorValue(str(new_value))
        result.value = new_value
        result.error = new_error
        return result

    def format_output(self):
        #結果を「数値 ± 誤差」の形式で、誤差の桁に合わせて丸めて出力
        error_exponent = self.error.as_tuple().exponent

        # 丸める桁数の指定 (誤差の小数点以下の桁数)
        rounding_point = error_exponent * (-1)

        # 丸めの基準となるDecimalオブジェクト
        quantizer = Decimal(10) ** (error_exponent)
        rounded_value = self.value.quantize(quantizer, rounding=ROUND_HALF_UP)

        # 出力フォーマットの調整
        if rounding_point <= 0:
            # 誤差が0.5 (一の位) の場合など、整数部のみを表示
            formatted_value = str(int(rounded_value))
            # 誤差は小数点以下なしの表示にする (例: 0.6 -> 0.6)
            formatted_error = f"{self.error.normalize():g}"
        else:
            # 小数点以下の表示を桁数に合わせて調整
            formatted_value = f"{rounded_value:.{rounding_point}f}"
            formatted_error = f"{self.error:.{rounding_point}f}"


        return f"{formatted_value} ± {formatted_error}"

# --- 電卓実行部分 ---

def run_simple_calculator():
    """標準入力から受け取り、丸め誤差の足し算を実行する簡易電卓関数。"""

    # 標準入力から計算式を文字列として受け取る
    input_str = input("計算式を入力してください（例: 1+2.0+3.0）: ")

    # 🌟 ここがご要望の「標準入力を文字列として読み取り+で区切る」処理です
    parts = [p.strip() for p in input_str.split('+') if p.strip()]

    if not parts:
        print("有効な入力がありませんでした。")
        return

    try:
        # 最初の数値で初期化
        current_result = ErrorValue(parts[0])

        # 2番目以降の数値を順に加算
        for part in parts[1:]:
            next_value = ErrorValue(part)
            print(f"  > 中間計算: {current_result.value} ± {current_result.error} + {next_value.value} ± {next_value.error}")
            current_result = current_result + next_value

        # --- 結果の表示 ---

        # 元の入力値とその初期誤差を表示
        initial_errors = [f'{p}±{ErrorValue(p).error}' for p in parts]
        print("---")
        print(f"入力値と初期誤差: {', '.join(initial_errors)}")
        print(f"誤差の合計: {sum(ErrorValue(p).error for p in parts)}")
        print("---")

        # 最終結果の出力
        print(f"最終計算結果: {current_result.format_output()}")

    except Exception as e:
        print(f"\nエラーが発生しました。入力形式を確認してください。({e})")


if __name__ == "__main__":
    run_simple_calculator()
