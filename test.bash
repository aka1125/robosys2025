#!/bin/bash
# SPDX-FileCopyrightText: 2025 Yusaku Aka
# SPDX-License-Identifier: BSD-3-Clause

ng () {
	echo ${1}行目が違うよ
	res=1
}

res=0
a=山田
test "$a" = 上田 || ng "$LINENO"
test "$a" = 山田 || ng "$LINENO"

exit $res

