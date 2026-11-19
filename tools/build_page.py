"""Wrap web/page.html (an Artifact-style page body) into site/index.html."""
HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""
page = open("web/page.html", encoding="utf-8").read()
cut = page.index("</style>") + len("</style>")
open("site/index.html", "w", encoding="utf-8").write(HEAD + page[:cut] + "\n</head><body>\n" + page[cut:] + "\n</body></html>\n")
