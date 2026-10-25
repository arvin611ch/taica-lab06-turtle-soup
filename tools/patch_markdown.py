"""把 tools/sections/*.md 塞進已執行的 notebook 對應的 markdown 格（依 metadata.id），不用重新執行程式格。"""
import json, sys, nbformat
NB = sys.argv[1] if len(sys.argv) > 1 else "lab06_turtle_soup_chatbot.ipynb"
PLACEHOLDERS = {"design": "__DESIGN_SECTION__", "shots": "__SHOTS_SECTION__",
                "ai-help": "__AIHELP_SECTION__", "reflection": "__REFLECTION_SECTION__"}
nb = nbformat.read(NB, as_version=4)
done = []
for cell in nb.cells:
    cid = cell.metadata.get("id")
    if cell.cell_type == "markdown" and cid in PLACEHOLDERS:
        try:
            cell.source = open(f"tools/sections/{cid}.md", encoding="utf-8").read().strip("\n")
            done.append(cid)
        except FileNotFoundError:
            print("missing section file for", cid)
nbformat.write(nb, NB)
left = [c.metadata.get("id") for c in nb.cells if c.cell_type == "markdown" and "__" in c.source and "_SECTION__" in c.source]
print("patched:", done, "| placeholders left:", left)
