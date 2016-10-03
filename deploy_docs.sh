#!/bin/sh
git add ./docs/build/html
git commit -m "Deploy updated documentation"
git subtree push --prefix docs/build/html origin gh-pages
git reset --hard HEAD^
