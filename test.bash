#!/bin/bash -xv
# SPDX-FileCopyrightText: 2025 Yusaku Aka
# SPDX-License-Identifier: BSD-3-Clause

ng () {
	echo ${1}行目が違うよ
	res=1
}

res=0
a=$(seq 5 | ./plus)
test "$a" = 15 || ng "$LINENO"
test "$res" = 0 && echo OK

exit $res

