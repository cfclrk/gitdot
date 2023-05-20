#!/usr/bin/env bash

touch A && git add A && git commit -m "A"
touch B && git add B && git commit -m "B"
git checkout -b "feat-1"
touch C && git add C && git commit -m "C"
touch D && git add D && git commit -m "D"
