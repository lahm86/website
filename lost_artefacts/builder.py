from jinjax import Catalog
from dataclasses import dataclass

from lost_artefacts.common import BUILD_DIR, COMPONENTS_DIR, STATIC_DIR

@dataclass
class Page:
    out: str
    component: str
    title: str
    active: bool = False


PAGES: list[Page] = [
    Page(out="index.html", component="PageHome", title="Home"),
    Page(out="tr1x.html", component="PageTR1X", title="TR1X"),
    Page(out="tr2x.html", component="PageTR2X", title="TR2X"),
    Page(out="rando.html", component="PageRando", title="TR-Rando"),
    Page(out="contact.html", component="PageContact", title="Contact"),
]


def build() -> None:
    catalog = Catalog()
    catalog.add_folder(COMPONENTS_DIR)
    catalog.jinja_env.globals.update(nav=PAGES)

    for page in PAGES:
        for other_page in PAGES:
            other_page.active = other_page is page

        target_path = BUILD_DIR / page.out
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(catalog.render(page.component, title=page.title))

    if not (BUILD_DIR / "static").exists():
        (BUILD_DIR / "static").symlink_to(STATIC_DIR)
