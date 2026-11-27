"""Write every SVG into <out>/ (assets layout used by the README)."""
import os, sys
import hero, parts, lib

out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sizes = {}
import xml.dom.minidom as _md
def put(rel, svg):
    _md.parseString(svg.encode("utf-8"))  # strict XML check: fail the build on any markup error
    sizes[rel] = lib.write(os.path.join(out, rel), svg)

put("hero.svg", hero.build())
put("typing.svg", parts.typing())
for num, title, sub, acc, slug in parts.SECTIONS:
    put(f"sections/{num}-{slug}.svg", parts.header(num, title, sub, acc))
put("identity.svg", parts.identity())
put("career.svg", parts.career())
put("skills.svg", parts.skills())
for c in parts.CARDS:
    put(f"projects/{c['slug']}.svg", parts.card(c))
for slug, label, sub, acc, ic in parts.BUTTONS:
    put(f"buttons/{slug.replace('btn-', '')}.svg", parts.button(slug, label, sub, acc, ic))
put("footer.svg", parts.footer())
tot = sum(sizes.values())
for k, v in sizes.items():
    print(f"{v/1024:7.1f} KB  {k}")
print(f"{tot/1024:7.1f} KB  TOTAL ({len(sizes)} files)")
