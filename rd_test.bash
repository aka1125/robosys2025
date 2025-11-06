#!/bin/bash -xv
# SPDX-FileCopyrightText: 2025 Yusaku Aka
# SPDX-License-Identifier: BSD-3-Clause

ng () {
        echo ${1}行目が違うよ
        res=1
}

res=0

### NORMAL INSERT ###
expected_a="最終計算結果: 2.00 ± 0.55"
a=$(echo "1+1.0" | ./rounding_error.py | tail -n 1)
test "$a" = "$expected_a" || ng "$LINENO"

### STRANGE INSERT ###
a=$(echo "あ" | ./rounding_error.py | grep "エラーが発生しました")
test "$?" = 0 || ng "$LINENO" 
test "$a" != "" || ng "$LINENO"


# 空入力のテスト
expected_empty_output="有効な入力がありませんでした。"
# プロンプトを除去する sed コマンドを追加
a=$(echo "" | ./rounding_error.py | tail -n 1 | sed 's/.*: //')
test "$a" = "$expected_empty_output" || ng "$LINENO"

# --- 最終結果 ---
test "$res" = 0 && echo "OK"
exit $res
