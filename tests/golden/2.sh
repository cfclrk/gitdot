#!/usr/bin/env bash

touch A && git add A && git commit -m "A"
git tag -a "v0.0.1" -m "Initial Release"
touch B && git add B && git commit -m "B"
git checkout -b B1
touch C && git add C && git commit -m "C"
git checkout main
git checkout -b B2
touch D && git add D && git commit -m "D"
