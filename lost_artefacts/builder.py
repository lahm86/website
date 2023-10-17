from dataclasses import dataclass

from jinjax import Catalog

from lost_artefacts.common import BUILD_DIR, COMPONENTS_DIR, STATIC_DIR


@dataclass
class Page:
    out: str
    component: str
    title: str


@dataclass
class TopNav:
    title: str
    href: str
    components: list[str]
    active: bool = False


PAGES: list[Page] = [
    Page(out="index.html", component="PageHome", title="Home"),
    Page(out="projects.html", component="PageProjects", title="PRojects"),
    Page(out="tr1x.html", component="PageTR1XHome", title="TR1X"),
    Page(out="tr1x_changes.html", component="PageTR1XChanges", title="TR1X"),
    Page(out="tr2x.html", component="PageTR2X", title="TR2X"),
    Page(out="rando.html", component="PageRando", title="TR-Rando"),
    Page(out="contact.html", component="PageContact", title="Contact"),
]

TOP_NAV: list[Page] = [
    TopNav(title="LostArtefacts", href="index.html", components=["PageHome"]),
    TopNav(
        title="Projects",
        href="projects.html",
        components=[
            "PageProjects",
            "PageTR1XHome",
            "PageTR1XChanges",
            "PageTR2X",
            "PageRando",
        ],
    ),
    TopNav(title="Contact", href="contact.html", components=["PageContact"]),
]


def build() -> None:
    catalog = Catalog()
    catalog.add_folder(COMPONENTS_DIR)
    catalog.jinja_env.globals.update(nav=TOP_NAV)

    for page in PAGES:
        for nav_item in TOP_NAV:
            nav_item.active = page.component in nav_item.components

        target_path = BUILD_DIR / page.out
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(
            catalog.render(page.component, title=page.title)
        )

    if not (BUILD_DIR / "static").exists():
        (BUILD_DIR / "static").symlink_to(STATIC_DIR)
