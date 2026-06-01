# -*- coding: utf-8 -*-
"""
Professional diagram generator for the WeatherBot project report.
Every diagram is laid out on an explicit grid; connectors attach to box
borders (never centres), so no arrow crosses text and nothing overlaps.
"""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Circle
from matplotlib.lines import Line2D

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

# ---- palette -----------------------------------------------------------
NAVY   = "#0b1f3a"
BLUE   = "#2563eb"
SKY    = "#7dd3fc"
SKYBG  = "#e0f2fe"
INDIGO = "#4f46e5"
INDBG  = "#e8e7fb"
GREEN  = "#0e9f6e"
GRNBG  = "#dcfce7"
AMBER  = "#b45309"
AMBBG  = "#fef3c7"
PINK   = "#be185d"
PNKBG  = "#fce7f3"
GREY   = "#475569"
GREYBG = "#eef2f7"
LINE   = "#334155"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
})

# ---- geometry helpers --------------------------------------------------
class Box:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    @property
    def left(self):   return self.x - self.w / 2
    @property
    def right(self):  return self.x + self.w / 2
    @property
    def top(self):    return self.y + self.h / 2
    @property
    def bottom(self): return self.y - self.h / 2
    def edge(self, tx, ty):
        """Point on this box's border on the ray toward (tx,ty)."""
        dx, dy = tx - self.x, ty - self.y
        if dx == 0 and dy == 0:
            return (self.x, self.y)
        sx = (self.w / 2) / abs(dx) if dx else math.inf
        sy = (self.h / 2) / abs(dy) if dy else math.inf
        s = min(sx, sy)
        return (self.x + dx * s, self.y + dy * s)


def box(ax, x, y, w, h, text, fc=SKYBG, ec=BLUE, tc=NAVY, fs=11,
        bold=True, rounded=0.12, lw=1.6):
    b = Box(x, y, w, h)
    p = FancyBboxPatch((b.left, b.bottom), w, h,
                       boxstyle=f"round,pad=0.02,rounding_size={rounded}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=tc, weight="bold" if bold else "normal", zorder=3,
            linespacing=1.25)
    return b


def rect(ax, x, y, w, h, text, fc=GREYBG, ec=LINE, tc=NAVY, fs=11, bold=True, lw=1.6):
    return box(ax, x, y, w, h, text, fc, ec, tc, fs, bold, rounded=0.001, lw=lw)


def arrow(ax, a, b, label=None, color=LINE, ls="-", lw=1.7, rad=0.0,
          fs=9.5, loff=(0, 0), double=False, tc=None):
    """Arrow between two Box borders (or raw points)."""
    if isinstance(a, Box) and isinstance(b, Box):
        p1 = a.edge(b.x, b.y)
        p2 = b.edge(a.x, a.y)
    elif isinstance(a, Box):
        p1 = a.edge(*b); p2 = b
    elif isinstance(b, Box):
        p1 = a; p2 = b.edge(*a)
    else:
        p1, p2 = a, b
    style = "<|-|>" if double else "-|>"
    ap = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=15,
                         linewidth=lw, color=color, linestyle=ls,
                         connectionstyle=f"arc3,rad={rad}", zorder=1.5,
                         shrinkA=0, shrinkB=0)
    ax.add_patch(ap)
    if label:
        mx, my = (p1[0] + p2[0]) / 2 + loff[0], (p1[1] + p2[1]) / 2 + loff[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=tc or color, zorder=4,
                bbox=dict(boxstyle="round,pad=0.18", fc="white",
                          ec="none", alpha=0.9))


def new(figsize, xlim, ylim, title=None):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.text((xlim[0]+xlim[1])/2, ylim[1]-0.35, title, ha="center",
                va="top", fontsize=13.5, weight="bold", color=NAVY)
    return fig, ax


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white", pad_inches=0.15)
    plt.close(fig)
    print("wrote", path)


# =======================================================================
# 1. HIGH-LEVEL SYSTEM ARCHITECTURE  (layered)
# =======================================================================
def fig_architecture():
    fig, ax = new((9.2, 7.6), (0, 16), (0, 14))
    ax.text(8, 13.4, "WeatherBot — High-Level System Architecture",
            ha="center", fontsize=14, weight="bold", color=NAVY)

    # Browser container band
    ax.add_patch(FancyBboxPatch((0.6, 4.4), 14.8, 8.0,
                 boxstyle="round,pad=0.02,rounding_size=0.2",
                 fc="#f8fafc", ec=BLUE, lw=2.2, ls="--", zorder=0.5))
    ax.text(1.0, 12.05, "Client (Web Browser — single HTML file)",
            ha="left", fontsize=10.5, style="italic", color=BLUE)

    # Presentation layer
    pres = box(ax, 8, 11.0, 12.6, 1.15,
               "Presentation Layer  —  HTML structure + CSS glassmorphism UI",
               INDBG, INDIGO, NAVY, 10.5)
    # Application logic layer (with sub-boxes)
    ax.add_patch(FancyBboxPatch((1.5, 7.0), 13.0, 2.7,
                 boxstyle="round,pad=0.02,rounding_size=0.12",
                 fc="#f1f5ff", ec=INDIGO, lw=1.6, zorder=1.2))
    ax.text(8, 9.42, "Application-Logic Layer  (vanilla JavaScript)",
            ha="center", fontsize=10.5, weight="bold", color=INDIGO)
    nlp   = box(ax, 3.3, 7.9, 3.0, 1.0, "NLU\nparse()", SKYBG, BLUE, NAVY, 9.5)
    geo   = box(ax, 6.6, 7.9, 3.0, 1.0, "Geocoding\ngeocode()", SKYBG, BLUE, NAVY, 9.5)
    rep   = box(ax, 9.9, 7.9, 3.0, 1.0, "report()\n(core hub)", "#dbeafe", BLUE, NAVY, 9.5)
    rend  = box(ax, 13.0, 7.9, 2.6, 1.0, "Renderers\naddMsg()", SKYBG, BLUE, NAVY, 9.5)

    # Browser capabilities layer
    bcap = box(ax, 8, 5.4, 12.6, 1.1,
               "Native Browser Capabilities  —  Geolocation API · Web Speech API · Fetch API · DOM",
               GRNBG, GREEN, NAVY, 9.5)

    # External services band
    ax.text(8, 3.55, "External Services  (free · key-less · HTTPS)",
            ha="center", fontsize=10.5, weight="bold", color=AMBER)
    s1 = box(ax, 2.7, 2.1, 3.0, 1.25, "Open-Meteo\nGeocoding API", AMBBG, AMBER, NAVY, 9)
    s2 = box(ax, 6.4, 2.1, 3.0, 1.25, "Open-Meteo\nForecast API", AMBBG, AMBER, NAVY, 9)
    s3 = box(ax, 10.1, 2.1, 3.0, 1.25, "BigDataCloud\nReverse-Geocode", AMBBG, AMBER, NAVY, 9)
    s4 = box(ax, 13.5, 2.1, 2.7, 1.25, "OpenStreetMap\nTiles (Leaflet)", AMBBG, AMBER, NAVY, 9)

    # vertical layer links
    arrow(ax, pres, Box(8, 9.7, 13, 0.01), color=INDIGO, lw=2, double=True)
    arrow(ax, Box(8, 7.0, 13, 0.01), bcap, color=INDIGO, lw=2, double=True)

    # service links (over HTTPS)
    arrow(ax, geo, s1, color=AMBER, rad=-0.05)
    arrow(ax, rep, s2, color=AMBER, rad=0.05)
    arrow(ax, bcap, s3, color=AMBER, rad=0.0)
    arrow(ax, pres, s4, color=AMBER, rad=0.32, ls="--")

    save(fig, "fig_architecture.png")


# =======================================================================
# 2. COMPONENT ARCHITECTURE (hub-and-spoke around report())
# =======================================================================
def fig_components():
    fig, ax = new((9.4, 8.2), (0, 16), (0, 15))
    ax.text(8, 14.4, "WeatherBot — Component Architecture",
            ha="center", fontsize=14, weight="bold", color=NAVY)

    hub = box(ax, 8, 7.4, 3.4, 1.5, "report()\nWeather Reporting\nHub", "#dbeafe", BLUE, NAVY, 10.5)

    ui   = box(ax, 8, 12.6, 3.6, 1.3, "User Interface\nComponent", INDBG, INDIGO, NAVY, 10)
    srch = box(ax, 2.6, 11.0, 3.3, 1.3, "Search /\nNLU Module", SKYBG, BLUE, NAVY, 10)
    api  = box(ax, 13.4, 11.0, 3.3, 1.3, "Weather API\nModule", AMBBG, AMBER, NAVY, 10)
    proc = box(ax, 13.6, 6.8, 3.3, 1.3, "Data Processing\nModule", GRNBG, GREEN, NAVY, 10)
    loc  = box(ax, 2.4, 6.8, 3.3, 1.3, "Location Services\nModule", GRNBG, GREEN, NAVY, 10)
    err  = box(ax, 4.2, 2.7, 3.3, 1.3, "Error Handling\nModule", PNKBG, PINK, NAVY, 10)
    voice= box(ax, 11.8, 2.7, 3.3, 1.3, "Voice / Speech\nModule", PNKBG, PINK, NAVY, 10)
    resp = box(ax, 8, 2.2, 3.4, 1.3, "Responsive Design\nModule (CSS)", INDBG, INDIGO, NAVY, 10)

    arrow(ax, ui, hub, "events", color=INDIGO, fs=9, double=True)
    arrow(ax, srch, hub, "city + intent", color=BLUE, fs=9)
    arrow(ax, hub, api, "fetch", color=AMBER, fs=9, double=True)
    arrow(ax, api, proc, "JSON", color=AMBER, fs=9)
    arrow(ax, proc, hub, "formatted text", color=GREEN, fs=9, loff=(0, 0.2))
    arrow(ax, loc, hub, "lat/lon", color=GREEN, fs=9)
    arrow(ax, ui, srch, "text/voice", color=INDIGO, fs=9, rad=0.18)
    arrow(ax, ui, loc, "GPS/map", color=INDIGO, fs=9, rad=-0.18)
    arrow(ax, hub, err, "on failure", color=PINK, fs=9, rad=0.1)
    arrow(ax, hub, voice, "speak()", color=PINK, fs=9, rad=-0.1)
    arrow(ax, hub, resp, "render", color=BLUE, fs=9)
    arrow(ax, err, ui, "message", color=PINK, fs=9, rad=0.2)

    save(fig, "fig_components.png")


# =======================================================================
# 3. CONTEXT DIAGRAM (DFD Level 0 context)
# =======================================================================
def fig_context():
    fig, ax = new((9.6, 6.6), (0, 16), (0, 11))
    ax.text(8, 10.4, "Context Diagram (DFD — Context Level)",
            ha="center", fontsize=14, weight="bold", color=NAVY)

    core = Circle((8, 5.5), 1.9, fc="#dbeafe", ec=BLUE, lw=2.2, zorder=2)
    ax.add_patch(core)
    ax.text(8, 5.5, "0\nWeatherBot\nSystem", ha="center", va="center",
            fontsize=11, weight="bold", color=NAVY, zorder=3)
    coreb = Box(8, 5.5, 3.8, 3.8)

    user = rect(ax, 8, 9.2, 3.0, 1.1, "User", "#fff", LINE, NAVY, 10.5)
    geoS = rect(ax, 1.9, 7.2, 3.0, 1.1, "Open-Meteo\nGeocoding", "#fff", LINE, NAVY, 9.5)
    fcS  = rect(ax, 1.9, 3.6, 3.0, 1.1, "Open-Meteo\nForecast", "#fff", LINE, NAVY, 9.5)
    rgS  = rect(ax, 14.1, 7.2, 3.0, 1.1, "BigDataCloud\nReverse-Geo", "#fff", LINE, NAVY, 9.5)
    osmS = rect(ax, 14.1, 3.6, 3.0, 1.1, "OpenStreetMap\nTiles", "#fff", LINE, NAVY, 9.5)

    arrow(ax, user, coreb, "query / voice / GPS / map tap", color=BLUE, fs=8.5,
          rad=0.30, loff=(-1.5, 0.15))
    arrow(ax, coreb, user, "weather reply", color=GREEN, fs=8.5, rad=0.30,
          loff=(1.5, 0.15))
    arrow(ax, coreb, geoS, "city name", color=AMBER, fs=8.5, rad=0.22, loff=(0, 0.32))
    arrow(ax, geoS, coreb, "coordinates", color=GREEN, fs=8.5, rad=0.22, loff=(0, -0.32))
    arrow(ax, coreb, fcS, "lat/lon", color=AMBER, fs=8.5, rad=-0.22, loff=(0, -0.32))
    arrow(ax, fcS, coreb, "forecast JSON", color=GREEN, fs=8.5, rad=-0.22, loff=(0, 0.32))
    arrow(ax, coreb, rgS, "lat/lon", color=AMBER, fs=8.5, rad=-0.22, loff=(0, 0.32))
    arrow(ax, rgS, coreb, "place name", color=GREEN, fs=8.5, rad=-0.22, loff=(0, -0.32))
    arrow(ax, coreb, osmS, "tile request", color=AMBER, fs=8.5, rad=0.22, loff=(0, -0.32))
    arrow(ax, osmS, coreb, "map tiles", color=GREEN, fs=8.5, rad=0.22, loff=(0, 0.32))

    save(fig, "fig_context.png")


# =======================================================================
# 4. LEVEL-1 DFD
# =======================================================================
def fig_dfd0():
    fig, ax = new((10.4, 7.4), (0, 18), (0, 13))
    ax.text(9, 12.4, "Level-0 Data Flow Diagram", ha="center",
            fontsize=14, weight="bold", color=NAVY)

    user = rect(ax, 9, 11.2, 3.0, 1.0, "User", "#fff", LINE, NAVY, 10)

    def proc(x, y, num, name, fc=SKYBG, ec=BLUE):
        e = Ellipse((x, y), 3.4, 1.7, fc=fc, ec=ec, lw=1.8, zorder=2)
        ax.add_patch(e)
        ax.text(x, y, f"{num}\n{name}", ha="center", va="center",
                fontsize=9, weight="bold", color=NAVY, zorder=3)
        return Box(x, y, 3.4, 1.7)

    p1 = proc(9, 8.6, "1.0", "Capture &\nParse Input")
    p2 = proc(3.4, 6.0, "2.0", "Resolve\nLocation")
    p3 = proc(9, 4.2, "3.0", "Fetch & Process\nForecast", GRNBG, GREEN)
    p4 = proc(14.6, 6.0, "4.0", "Render &\nSpeak Reply", INDBG, INDIGO)

    geoS = rect(ax, 3.4, 10.6, 3.2, 1.0, "Open-Meteo Geocoding /\nBigDataCloud", "#fff", LINE, NAVY, 8.5)
    fcS  = rect(ax, 14.6, 10.6, 3.2, 1.0, "Open-Meteo\nForecast API", "#fff", LINE, NAVY, 8.5)
    store= rect(ax, 9, 1.4, 4.2, 0.95, "D1 | Weather-code lookup table (in-memory)", "#fff7ed", AMBER, NAVY, 8.5)

    arrow(ax, user, p1, "raw input", color=BLUE, fs=8.5)
    arrow(ax, p1, p2, "city / coords", color=BLUE, fs=8.5, rad=0.1)
    arrow(ax, p2, geoS, "name / lat-lon", color=AMBER, fs=8, rad=0.12)
    arrow(ax, geoS, p2, "location obj", color=GREEN, fs=8, rad=0.12, loff=(0,-0.2))
    arrow(ax, p2, p3, "location + intent", color=BLUE, fs=8.5, rad=0.1)
    arrow(ax, p3, fcS, "lat/lon", color=AMBER, fs=8, rad=-0.12)
    arrow(ax, fcS, p3, "forecast JSON", color=GREEN, fs=8, rad=-0.12, loff=(0,-0.2))
    arrow(ax, store, p3, "code → text/emoji", color=AMBER, fs=8, rad=0.0)
    arrow(ax, p3, p4, "formatted report", color=GREEN, fs=8.5, rad=0.1)
    arrow(ax, p4, user, "chat reply / speech", color=INDIGO, fs=8.5, rad=0.22)

    save(fig, "fig_dfd0.png")


def fig_dfd1():
    """Level-1: decomposition of Process 1.0 (Capture & Parse Input)."""
    fig, ax = new((10.6, 7.0), (0, 18), (0, 12))
    ax.text(9, 11.4, "Level-1 DFD — Decomposition of Process 1.0 (Capture & Parse Input)",
            ha="center", fontsize=12.5, weight="bold", color=NAVY)

    user = rect(ax, 2.3, 9.2, 2.8, 1.0, "User", "#fff", LINE, NAVY, 10)
    down = rect(ax, 15.4, 9.2, 3.1, 1.1, "To 2.0\nResolve Location", "#eef6ff", BLUE, NAVY, 9)

    def proc(x, y, num, name, fc=SKYBG, ec=BLUE):
        e = Ellipse((x, y), 3.4, 1.7, fc=fc, ec=ec, lw=1.8, zorder=2)
        ax.add_patch(e)
        ax.text(x, y, f"{num}\n{name}", ha="center", va="center",
                fontsize=8.8, weight="bold", color=NAVY, zorder=3)
        return Box(x, y, 3.4, 1.7)

    p11 = proc(7.6, 9.2, "1.1", "Detect\nInput Mode")
    p12 = proc(7.6, 5.6, "1.2", "Normalise\nFree Text", INDBG, INDIGO)
    p13 = proc(12.0, 6.4, "1.3", "Detect Time\nIntent", GRNBG, GREEN)
    p14 = proc(12.0, 2.9, "1.4", "Extract City\nName", GRNBG, GREEN)

    store = rect(ax, 4.0, 2.9, 4.2, 0.95, "D2 | Filler-word & keyword lists", "#fff7ed", AMBER, NAVY, 8.5)

    arrow(ax, user, p11, "raw input", color=BLUE, fs=8.5)
    arrow(ax, p11, down, "coords (GPS / map)", color=BLUE, fs=8, loff=(0, 0.3))
    arrow(ax, p11, p12, "text string", color=INDIGO, fs=8.5)
    arrow(ax, p12, p13, "lower-cased text", color=GREEN, fs=8, rad=-0.1)
    arrow(ax, p12, p14, "stripped text", color=GREEN, fs=8, rad=0.1)
    arrow(ax, store, p14, "filter words", color=AMBER, fs=8, rad=0.0)
    arrow(ax, p13, down, "time intent", color=GREEN, fs=8, rad=-0.15, loff=(0.3, 0))
    arrow(ax, p14, down, "city name", color=GREEN, fs=8, rad=-0.2, loff=(0.5, 0))

    save(fig, "fig_dfd1.png")


# =======================================================================
# 5. USE-CASE DIAGRAM
# =======================================================================
def fig_usecase():
    fig, ax = new((9.4, 8.0), (0, 16), (0, 14))
    ax.text(8, 13.4, "Use-Case Diagram", ha="center", fontsize=14,
            weight="bold", color=NAVY)

    # system boundary
    ax.add_patch(FancyBboxPatch((4.7, 1.4), 7.4, 11.0,
                 boxstyle="round,pad=0.02,rounding_size=0.1",
                 fc="#f8fafc", ec=BLUE, lw=2))
    ax.text(8.4, 11.95, "WeatherBot System", ha="center", fontsize=10.5,
            style="italic", color=BLUE)

    # actor (stick figure)
    def actor(x, y, name):
        ax.add_patch(Circle((x, y+0.6), 0.32, fc="white", ec=LINE, lw=1.8, zorder=3))
        ax.plot([x, x], [y+0.28, y-0.5], color=LINE, lw=1.8, zorder=3)
        ax.plot([x-0.5, x+0.5], [y, y], color=LINE, lw=1.8, zorder=3)
        ax.plot([x, x-0.45], [y-0.5, y-1.15], color=LINE, lw=1.8, zorder=3)
        ax.plot([x, x+0.45], [y-0.5, y-1.15], color=LINE, lw=1.8, zorder=3)
        ax.text(x, y-1.6, name, ha="center", fontsize=10, weight="bold", color=NAVY)
        return Box(x, y-0.1, 1.0, 2.2)

    user = actor(1.9, 7.0, "User")

    def uc(y, label):
        e = Ellipse((8.4, y), 5.6, 1.35, fc=SKYBG, ec=BLUE, lw=1.6, zorder=2)
        ax.add_patch(e)
        ax.text(8.4, y, label, ha="center", va="center", fontsize=9.5,
                color=NAVY, zorder=3)
        return Box(8.4, y, 5.6, 1.35)

    u1 = uc(10.7, "Ask weather by typing")
    u2 = uc(8.7,  "Ask weather by voice")
    u3 = uc(6.7,  "Use my GPS location")
    u4 = uc(4.7,  "Pick a point on the map")
    u5 = uc(2.7,  "Hear reply read aloud")

    for u in (u1, u2, u3, u4, u5):
        arrow(ax, user, u, color=LINE, lw=1.5)

    # <<include>> common reporting
    save(fig, "fig_usecase.png")


# =======================================================================
# 6. SEQUENCE DIAGRAM (typed query)
# =======================================================================
def fig_sequence():
    fig, ax = new((11.5, 8.4), (0, 23), (0, 16))
    ax.text(11.5, 15.4, 'Sequence Diagram — "Will it rain in Paris tomorrow?"',
            ha="center", fontsize=13.5, weight="bold", color=NAVY)

    actors = [
        (2.2,  "User"),
        (6.0,  "UI / form"),
        (9.8,  "parse()"),
        (13.2, "geocode()"),
        (16.6, "report()"),
        (20.4, "Open-Meteo\nAPIs"),
    ]
    life_top, life_bot = 13.4, 1.2
    cols = {}
    for x, name in actors:
        box(ax, x, 14.1, 3.0, 1.1, name, INDBG, INDIGO, NAVY, 9)
        ax.plot([x, x], [life_top, life_bot], color=GREY, ls="--", lw=1.2, zorder=0.5)
        cols[name] = x

    def msg(y, a, b, label, color=LINE, dashed=False, fs=8.6):
        x1, x2 = cols[a], cols[b]
        ap = FancyArrowPatch((x1, y), (x2, y), arrowstyle="-|>",
                             mutation_scale=13, lw=1.5, color=color,
                             linestyle="--" if dashed else "-", zorder=2)
        ax.add_patch(ap)
        midx = (x1 + x2) / 2
        ax.text(midx, y + 0.22, label, ha="center", va="bottom",
                fontsize=fs, color=color, zorder=3)

    U, UI, P, G, R, API = "User", "UI / form", "parse()", "geocode()", "report()", "Open-Meteo\nAPIs"
    msg(12.6, U, UI, "submit text")
    msg(11.6, UI, P, "parse(text)")
    msg(10.6, P, UI, "{city:'Paris', when:'tomorrow'}", BLUE, dashed=True)
    msg(9.6,  UI, G, "geocode('Paris')")
    msg(8.6,  G, API, "GET /v1/search", AMBER)
    msg(7.6,  API, G, "lat/lon + name", GREEN, dashed=True)
    msg(6.6,  G, R, "report(loc,'tomorrow')")
    msg(5.6,  R, API, "GET /v1/forecast", AMBER)
    msg(4.6,  API, R, "forecast JSON", GREEN, dashed=True)
    msg(3.4,  R, UI, "addMsg(reply)", INDIGO)
    msg(2.4,  UI, U, "render bubble (+ optional speech)", INDIGO)

    save(fig, "fig_sequence.png")


# =======================================================================
# 7. ACTIVITY DIAGRAM
# =======================================================================
def fig_activity():
    fig, ax = new((8.4, 11.2), (0, 14), (0, 20))
    ax.text(7, 19.4, "Activity Diagram — Weather Request",
            ha="center", fontsize=14, weight="bold", color=NAVY)

    # start
    ax.add_patch(Circle((7, 18.4), 0.32, fc=NAVY, ec=NAVY, zorder=3))
    a1 = box(ax, 7, 17.2, 6.2, 1.0, "Receive user input", SKYBG, BLUE, NAVY, 10)
    a2 = box(ax, 7, 15.7, 6.2, 1.0, "Determine input mode", SKYBG, BLUE, NAVY, 10)

    # decision: text/voice vs gps/map
    d1 = Box(7, 13.9, 3.6, 1.7)
    ax.add_patch(plt.Polygon([(7,14.75),(8.8,13.9),(7,13.05),(5.2,13.9)],
                 closed=True, fc=AMBBG, ec=AMBER, lw=1.6, zorder=2))
    ax.text(7, 13.9, "Free text?", ha="center", va="center", fontsize=9.5,
            weight="bold", color=NAVY, zorder=3)

    a3 = box(ax, 3.0, 13.9, 3.6, 1.0, "parse() →\ncity + intent", INDBG, INDIGO, NAVY, 9)
    a4 = box(ax, 3.0, 12.0, 3.6, 1.0, "geocode\ncity name", INDBG, INDIGO, NAVY, 9)
    a5 = box(ax, 11.0, 12.9, 4.0, 1.0, "reverse-geocode\nGPS / map coords", GRNBG, GREEN, NAVY, 9)

    # decision: location found?
    ax.add_patch(plt.Polygon([(7,11.4),(8.9,10.4),(7,9.4),(5.1,10.4)],
                 closed=True, fc=AMBBG, ec=AMBER, lw=1.6, zorder=2))
    ax.text(7, 10.4, "Location\nfound?", ha="center", va="center", fontsize=9,
            weight="bold", color=NAVY, zorder=3)
    dloc = Box(7, 10.4, 3.8, 2.0)

    aerr = box(ax, 12.2, 10.4, 3.2, 1.0, "Show error /\nask again", PNKBG, PINK, NAVY, 9)
    a6 = box(ax, 7, 8.2, 6.2, 1.0, "Fetch 7-day forecast (Open-Meteo)", GRNBG, GREEN, NAVY, 9.5)
    a7 = box(ax, 7, 6.7, 6.2, 1.0, "Map weather code → text + emoji", GRNBG, GREEN, NAVY, 9.5)
    a8 = box(ax, 7, 5.2, 6.2, 1.0, "Format reply by time intent", INDBG, INDIGO, NAVY, 9.5)
    a9 = box(ax, 7, 3.7, 6.2, 1.0, "Render bubble (+ optional speech)", INDBG, INDIGO, NAVY, 9.5)
    ax.add_patch(Circle((7, 2.3), 0.32, fc="white", ec=NAVY, lw=2, zorder=3))
    ax.add_patch(Circle((7, 2.3), 0.17, fc=NAVY, ec=NAVY, zorder=4))

    arrow(ax, Box(7,18.08,0,0), a1)
    arrow(ax, a1, a2)
    arrow(ax, a2, Box(7,14.75,0,0))
    arrow(ax, Box(5.2,13.9,0,0), a3, "yes", color=GREEN, fs=9, loff=(0,0.2))
    arrow(ax, a3, a4)
    arrow(ax, Box(8.8,13.9,0,0), a5, "no", color=AMBER, fs=9, loff=(0,0.2))
    arrow(ax, a4, Box(5.6,10.8,0,0), rad=-0.1)
    arrow(ax, a5, Box(8.4,10.8,0,0), rad=0.1)
    arrow(ax, Box(8.9,10.4,0,0), aerr, "no", color=PINK, fs=9, loff=(0,0.2))
    arrow(ax, aerr, a2, color=PINK, rad=0.4, ls="--")
    arrow(ax, dloc, a6, "yes", color=GREEN, fs=9, loff=(0.35,0))
    arrow(ax, a6, a7); arrow(ax, a7, a8); arrow(ax, a8, a9)
    arrow(ax, a9, Box(7,2.62,0,0))

    save(fig, "fig_activity.png")


# =======================================================================
# 8. CLASS / MODULE DIAGRAM
# =======================================================================
def fig_class():
    fig, ax = new((11.0, 7.6), (0, 22), (0, 15))
    ax.text(11, 14.4, "Module (Class-Style) Diagram",
            ha="center", fontsize=14, weight="bold", color=NAVY)

    def cls(x, y, w, title, attrs, ops, fc=SKYBG, ec=BLUE):
        n = max(len(attrs), 1); m = max(len(ops), 1)
        title_h, pad, step = 0.66, 0.16, 0.40
        attr_h = pad + step*n + pad
        op_h   = pad + step*m + pad
        hh = title_h + attr_h + op_h
        top = y + hh/2
        left = x - w/2
        ax.add_patch(plt.Rectangle((left, y-hh/2), w, hh, fc="white",
                     ec=ec, lw=1.7, zorder=2))
        ax.add_patch(plt.Rectangle((left, top-title_h), w, title_h, fc=fc,
                     ec=ec, lw=1.7, zorder=2.1))
        ax.text(x, top-title_h/2, title, ha="center", va="center", fontsize=9.5,
                weight="bold", color=NAVY, zorder=3)
        # attribute compartment
        ay = top - title_h - pad - step/2
        for a in attrs:
            ax.text(left+0.2, ay, a, ha="left", va="center",
                    fontsize=8.2, color=GREY, zorder=3)
            ay -= step
        div_y = top - title_h - attr_h
        ax.plot([left, x+w/2], [div_y, div_y], color=ec, lw=1.0, zorder=2.2)
        # operations compartment
        oy = div_y - pad - step/2
        for o in ops:
            ax.text(left+0.2, oy, o, ha="left", va="center",
                    fontsize=8.2, color=NAVY, zorder=3)
            oy -= step
        return Box(x, y, w, hh)

    loc = cls(11, 11.6, 5.2, "«data» Location",
              ["+ lat : float", "+ lon : float", "+ name : string",
               "+ admin : string", "+ country : string"],
              ["+ place() : string"], INDBG, INDIGO)

    nlu = cls(3.4, 8.0, 5.4, "NLU",
              ["- fillerWords", "- timeKeywords"],
              ["+ parse(text) : {city, when}"])

    gc = cls(10.2, 6.0, 5.6, "GeocodingService",
             ["- geocodeURL", "- reverseURL"],
             ["+ geocode(city) : Location", "+ reverseGeocode(lat,lon) : Location"],
             GRNBG, GREEN)

    ws = cls(18.0, 8.0, 6.0, "WeatherService",
             ["- forecastURL", "- WEATHER[] (code→text)"],
             ["+ getWeather(lat,lon) : JSON", "+ describe(code) : [text,emoji]",
              "+ report(loc, when)"], AMBBG, AMBER)

    ui = cls(4.0, 3.0, 5.6, "UIController",
             ["- chat, form, input", "- voiceOut : bool"],
             ["+ addMsg(text, who)", "+ addChips(items)", "+ answer(text)", "+ speak(text)"],
             PNKBG, PINK)

    arrow(ax, ui, nlu, "uses", color=LINE, fs=8.5)
    arrow(ax, ui, gc, "uses", color=LINE, fs=8.5, rad=0.05)
    arrow(ax, gc, ws, "calls", color=LINE, fs=8.5, rad=0.05)
    arrow(ax, gc, loc, "creates", color=LINE, fs=8.5, ls="--", rad=-0.1)
    arrow(ax, ws, loc, "reads", color=LINE, fs=8.5, ls="--", rad=0.12)

    save(fig, "fig_class.png")


# =======================================================================
# 9. COMPONENT DIAGRAM (UML component)
# =======================================================================
def fig_component_uml():
    fig, ax = new((10.6, 6.8), (0, 20), (0, 12))
    ax.text(10, 11.4, "UML Component Diagram", ha="center",
            fontsize=14, weight="bold", color=NAVY)

    def comp(x, y, w, h, name, fc=SKYBG, ec=BLUE):
        ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, fc=fc, ec=ec,
                     lw=1.7, zorder=2))
        # UML component icon
        ax.add_patch(plt.Rectangle((x-w/2+0.15, y+h/2-0.55), 0.7, 0.4,
                     fc="white", ec=ec, lw=1.3, zorder=3))
        ax.add_patch(plt.Rectangle((x-w/2+0.05, y+h/2-0.48), 0.22, 0.12,
                     fc="white", ec=ec, lw=1.3, zorder=3))
        ax.add_patch(plt.Rectangle((x-w/2+0.05, y+h/2-0.72), 0.22, 0.12,
                     fc="white", ec=ec, lw=1.3, zorder=3))
        ax.text(x+0.35, y, name, ha="center", va="center", fontsize=9.2,
                weight="bold", color=NAVY, zorder=3)
        return Box(x, y, w, h)

    ui  = comp(4.0, 8.6, 5.2, 2.0, "«component»\nChat UI", INDBG, INDIGO)
    eng = comp(10.0, 8.6, 5.2, 2.0, "«component»\nWeather Engine\n(report)", SKYBG, BLUE)
    bro = comp(4.0, 3.4, 5.2, 2.0, "«component»\nBrowser APIs", GRNBG, GREEN)
    ext = comp(16.0, 6.0, 6.0, 2.2, "«component»\nExternal Web APIs", AMBBG, AMBER)

    arrow(ax, ui, eng, "IWeatherQuery", color=LINE, fs=8.5)
    arrow(ax, bro, eng, "ILocation / ISpeech", color=LINE, fs=8.5, rad=0.05)
    arrow(ax, eng, ext, "HTTPS / REST", color=AMBER, fs=8.5, rad=0.05)
    arrow(ax, bro, ui, "DOM events", color=GREEN, fs=8.5, rad=-0.15)

    save(fig, "fig_component_uml.png")


# =======================================================================
# 10. UI WIREFRAME
# =======================================================================
def fig_wireframe():
    fig, ax = new((6.6, 9.6), (0, 11), (0, 16))
    ax.text(5.5, 15.4, "User-Interface Wireframe", ha="center",
            fontsize=14, weight="bold", color=NAVY)

    # phone frame
    ax.add_patch(FancyBboxPatch((1.2, 1.2), 8.6, 13.4,
                 boxstyle="round,pad=0.02,rounding_size=0.5",
                 fc="#0b1026", ec=NAVY, lw=2.5, zorder=1))
    # header
    ax.add_patch(FancyBboxPatch((1.7, 12.7), 7.6, 1.4,
                 boxstyle="round,pad=0.02,rounding_size=0.2",
                 fc=INDBG, ec=INDIGO, lw=1.4, zorder=2))
    ax.add_patch(FancyBboxPatch((1.95, 12.95), 0.85, 0.85,
                 boxstyle="round,pad=0.02,rounding_size=0.15",
                 fc="white", ec=INDIGO, lw=1.2, zorder=3))
    ax.text(2.38, 13.37, "W", ha="center", va="center", fontsize=12,
            weight="bold", color=INDIGO, zorder=4)
    ax.text(3.05, 13.45, "WeatherBot", ha="left", va="center", fontsize=11,
            weight="bold", color=NAVY, zorder=3)
    ax.text(2.4, 12.95, "Ask me the weather for any city", ha="left",
            va="center", fontsize=7.5, color=GREY, zorder=3)

    # bot bubble
    ax.add_patch(FancyBboxPatch((1.9, 10.2), 5.2, 1.7,
                 boxstyle="round,pad=0.02,rounding_size=0.25",
                 fc=GREYBG, ec=GREY, lw=1.2, zorder=2))
    ax.text(2.2, 11.05, "Hi! I'm WeatherBot. Ask me\nabout the weather anywhere.",
            ha="left", va="center", fontsize=8, color=NAVY, zorder=3)
    # chips
    for i, t in enumerate(["My location", "Weather in Tokyo"]):
        ax.add_patch(FancyBboxPatch((2.0+i*2.6, 9.3), 2.4, 0.6,
                     boxstyle="round,pad=0.02,rounding_size=0.3",
                     fc=SKYBG, ec=BLUE, lw=1, zorder=2))
        ax.text(3.2+i*2.6, 9.6, t, ha="center", va="center", fontsize=7, color=NAVY, zorder=3)
    # user bubble
    ax.add_patch(FancyBboxPatch((4.6, 7.7), 4.4, 1.1,
                 boxstyle="round,pad=0.02,rounding_size=0.25",
                 fc="#cfe3ff", ec=BLUE, lw=1.2, zorder=2))
    ax.text(6.8, 8.25, "Weather in Tokyo", ha="center", va="center",
            fontsize=8, color=NAVY, zorder=3)
    # bot reply bubble
    ax.add_patch(FancyBboxPatch((1.9, 5.3), 6.0, 2.1,
                 boxstyle="round,pad=0.02,rounding_size=0.25",
                 fc=GREYBG, ec=GREY, lw=1.2, zorder=2))
    ax.text(2.2, 6.35, "Right now in Tokyo:\n- Clear sky, 24 C\n- Humidity 60%, Wind 9 km/h",
            ha="left", va="center", fontsize=7.5, color=NAVY, zorder=3)

    # tool buttons
    for i, t in enumerate(["GPS", "Map", "Mic", "Spk"]):
        ax.add_patch(FancyBboxPatch((1.9+i*1.85, 3.6), 1.6, 0.9,
                     boxstyle="round,pad=0.02,rounding_size=0.2",
                     fc=GRNBG, ec=GREEN, lw=1.2, zorder=2))
        ax.text(2.7+i*1.85, 4.05, t, ha="center", va="center", fontsize=9,
                weight="bold", color=NAVY, zorder=3)
    # input row
    ax.add_patch(FancyBboxPatch((1.9, 2.2), 5.4, 1.0,
                 boxstyle="round,pad=0.02,rounding_size=0.4",
                 fc="white", ec=GREY, lw=1.2, zorder=2))
    ax.text(2.3, 2.7, "e.g. Will it rain in Paris…", ha="left", va="center",
            fontsize=7.5, color=GREY, zorder=3)
    ax.add_patch(FancyBboxPatch((7.5, 2.2), 1.8, 1.0,
                 boxstyle="round,pad=0.02,rounding_size=0.4",
                 fc=BLUE, ec=BLUE, lw=1.2, zorder=2))
    ax.text(8.4, 2.7, "Send", ha="center", va="center", fontsize=8.5,
            weight="bold", color="white", zorder=3)

    # callouts
    notes = [(9.9, 13.4, "Header / branding"),
             (9.9, 11.0, "Bot message bubble"),
             (9.9, 9.6,  "Suggestion chips"),
             (9.9, 8.25, "User message bubble"),
             (9.9, 4.05, "Tool buttons:\nGPS · Map · Mic · Speaker"),
             (9.9, 2.7,  "Text input + Send")]
    for x, y, t in notes:
        ax.annotate(t, xy=(9.8, y), xytext=(x+0.05, y), fontsize=7.3,
                    va="center", ha="left", color=GREY)
    save(fig, "fig_wireframe.png")


# =======================================================================
# 11. INPUT-MODE CONVERGENCE
# =======================================================================
def fig_inputs():
    fig, ax = new((9.6, 6.2), (0, 16), (0, 10))
    ax.text(8, 9.4, "Four Input Modes Converge on One Pipeline",
            ha="center", fontsize=13.5, weight="bold", color=NAVY)

    typ = box(ax, 2.4, 8.0, 3.0, 1.0, "Typed text", INDBG, INDIGO, NAVY, 9.5)
    voc = box(ax, 2.4, 6.3, 3.0, 1.0, "Voice input", INDBG, INDIGO, NAVY, 9.5)
    gps = box(ax, 2.4, 4.6, 3.0, 1.0, "GPS location", GRNBG, GREEN, NAVY, 9.5)
    mp  = box(ax, 2.4, 2.9, 3.0, 1.0, "Map tap", GRNBG, GREEN, NAVY, 9.5)

    parse = box(ax, 7.2, 7.15, 3.2, 1.1, "parse()\ntext → city+intent", SKYBG, BLUE, NAVY, 9)
    rgeo  = box(ax, 7.2, 3.75, 3.2, 1.1, "reverseGeocode()\ncoords → place", SKYBG, BLUE, NAVY, 9)
    geo   = box(ax, 11.0, 7.15, 2.8, 1.0, "geocode()", SKYBG, BLUE, NAVY, 9)

    rep = box(ax, 13.6, 5.45, 2.6, 1.4, "report()\n→ reply", "#dbeafe", BLUE, NAVY, 10)

    arrow(ax, typ, parse, color=INDIGO, rad=-0.05)
    arrow(ax, voc, parse, color=INDIGO, rad=0.08)
    arrow(ax, gps, rgeo, color=GREEN, rad=-0.05)
    arrow(ax, mp, rgeo, color=GREEN, rad=0.08)
    arrow(ax, parse, geo, color=BLUE)
    arrow(ax, geo, rep, color=BLUE, rad=-0.1)
    arrow(ax, rgeo, rep, color=BLUE, rad=0.1)

    save(fig, "fig_inputs.png")


if __name__ == "__main__":
    fig_architecture()
    fig_components()
    fig_context()
    fig_dfd0()
    fig_dfd1()
    fig_usecase()
    fig_sequence()
    fig_activity()
    fig_class()
    fig_component_uml()
    fig_wireframe()
    fig_inputs()
    print("ALL DIAGRAMS DONE")
