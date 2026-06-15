import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.ticker as ticker
import os, json

# ── Global font settings ──────────────────────────────────────────────────────
BASE_FONT = 22
plt.rcParams.update({"font.family": "sans-serif", "font.size": BASE_FONT})

# ── Physical parameters ───────────────────────────────────────────────────────
h  = 0.0747   # flow depth
hv = 0.041    # vegetation height
y_min = -0.005
y_max = h * 1.14   # a bit of headroom above water surface

# ── Colour palette ────────────────────────────────────────────────────────────
C_WATER    = "#1565C0"
C_ABOVE    = "#EBF5FB"
C_BED      = "#BCA99A"
C_BED_ED   = "#795548"
LAYER_COLS = ["#26C6DA", "#42A5F5", "#1E88E5", "#283593"]
C_DIVIDER  = "#90CAF9"
C_ABOVE_T  = "#5D6D7E"
C_BED_T    = "#795548"
HATCH      = "////"

# ── Figure: 2 rows × 2 cols, taller panels, more whitespace ──────────────────
fig = plt.figure(figsize=(18, 20))
fig.patch.set_facecolor("#FAFAFA")
#fig.suptitle("Multi-layer vegetation parameterisation",
#             fontsize=22, fontweight="bold", y=0.998, color="#222")

gs = fig.add_gridspec(2, 2, hspace=0.18, wspace=0.50,
                      left=0.08, right=0.96, top=0.96, bottom=0.03)
axes = [fig.add_subplot(gs[r, c]) for r in range(2) for c in range(2)]

# Panels are now (a) 1-layer, (b) 2-layer, (c) 3-layer, (d) 4-layer
panel_labels = ["(a)", "(b)", "(c)", "(d)"]
panel_titles  = ["1-layer (ZH)", "2-layer (ML2)", "3-layer (ML3)", "4-layer (ML4)"]

# ── Axis setup ────────────────────────────────────────────────────────────────
def setup_ax(ax, idx):
    ax.set_facecolor("#FAFAFA")
    ax.set_xlim(0, 1)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([])
    ax.set_yticks([0, hv, h])
    ax.set_yticklabels(["0", f"{hv}", f"{h}"], fontsize=BASE_FONT)
    ax.yaxis.set_minor_locator(ticker.NullLocator())
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.spines["left"].set_linewidth(1.0)
    ax.spines["left"].set_color("#888")
    ax.set_title(f"{panel_labels[idx]}  {panel_titles[idx]}",
                 fontsize=BASE_FONT + 3, color="#333", pad=8, fontweight="semibold")
    # Show y-axis label on left column only
    if idx in [0, 2]:
        ax.set_ylabel("z  [m]", fontsize=BASE_FONT + 2, labelpad=5, color="#444")
    else:
        ax.set_yticklabels([])

# ── Shared drawing ────────────────────────────────────────────────────
def draw_above_canopy(ax):
    """Shaded 'free water above canopy' region with hatching."""
    ax.axhspan(hv, h, color=C_ABOVE, alpha=1.0, zorder=1)
    ax.add_patch(plt.Rectangle((0, hv), 1, h - hv,
        fill=True, facecolor="none", hatch=HATCH,
        edgecolor="#C5D8E8", linewidth=0.0, alpha=0.55, zorder=2))
    ax.text(0.5, (hv + h) / 2, "Free water above canopy",
            ha="center", va="center", fontsize=BASE_FONT - 0.5,
            color=C_ABOVE_T, zorder=5, style="italic")

def draw_water_surface(ax):
    """Horizontal water-surface line + label."""
    ax.axhline(h, color=C_WATER, linewidth=2.0, alpha=0.90, zorder=6)
    ax.text(0.02, h + h * 0.022, "water surface",
            ha="left", va="bottom", fontsize=BASE_FONT,
            color=C_WATER, zorder=7)

def draw_bed(ax):
    """Hatched bed region below z = 0."""
    ax.axhspan(y_min, 0, color=C_BED, alpha=0.55, zorder=3)
    ax.axhline(0, color=C_BED_ED, linewidth=1.1, alpha=0.7, zorder=4)
    ax.text(0.5, y_min * 0.52, "bed",
            ha="center", va="center", fontsize=BASE_FONT,
            color=C_BED_T, zorder=5)

def draw_braces(ax, layer_bottoms, layer_tops, n_layers):
    """
    Individual layer-thickness arrows (d1…dn) on the right,
    plus a cumulative-height arrow (dv1…dvn-1) further right for n >= 2.

    layer_bottoms / layer_tops are ordered topmost-first (Layer 1 on top).
    """
    bx  = 1.04   # x-position for d_i arrows
    dvx = 1.18   # x-position for dv arrow

    # --- individual layer-thickness arrows ---
    for i, (zb, zt) in enumerate(zip(layer_bottoms, layer_tops)):
        ax.annotate("", xy=(bx, zb), xytext=(bx, zt),
                    xycoords="data", textcoords="data",
                    annotation_clip=False,
                    arrowprops=dict(arrowstyle="<->", color="#555", lw=1.2,
                                   mutation_scale=8))
        ax.text(bx + 0.045, (zb + zt) / 2, f"d{i+1}",
                ha="left", va="center", fontsize=BASE_FONT,
                color="#444", clip_on=False, transform=ax.transData)

    # --- cumulative vegetation height arrow (n_layers >= 2 only) ---
    if n_layers >= 2:
        # dv spans bed (0) → top of the second-from-bottom layer
        # layer_tops is topmost-first, so index n_layers-2 = second from bottom
        dv_top = layer_tops[n_layers - 2]
        dv_idx = n_layers - 1   # label: dv1, dv2, dv3

        ax.annotate("", xy=(dvx, 0), xytext=(dvx, dv_top),
                    xycoords="data", textcoords="data",
                    annotation_clip=False,
                    arrowprops=dict(arrowstyle="<->", color="#888", lw=1.1,
                                   mutation_scale=8))
        ax.text(dvx + 0.045, dv_top / 2, f"dv{dv_idx}",
                ha="left", va="center", fontsize=BASE_FONT,
                color="#666", clip_on=False, transform=ax.transData)

# ── Main layer-panel drawing ──────────────────────────────────────────────────
def draw_layer_panel(ax, layer_bottoms, layer_tops, n_layers):
    draw_above_canopy(ax)

    for i, (zb, zt) in enumerate(zip(layer_bottoms, layer_tops)):
        col = LAYER_COLS[min(i, len(LAYER_COLS) - 1)]
        ax.axhspan(zb, zt, color=col, alpha=0.88, zorder=3)
        ax.text(0.5, (zb + zt) / 2, f"Layer {i+1}",
                ha="center", va="center",
                fontsize=BASE_FONT,
                color="white", fontweight="bold", zorder=5)

    # Divider lines between layers
    for zt in layer_tops[1:]:
        ax.axhline(zt, color=C_DIVIDER, linewidth=1.1,
                   linestyle=(0, (5, 3)), alpha=0.8, zorder=4)

    # Canopy-top dashed line
    ax.axhline(hv, color="#7FBBDD", linewidth=1.0,
               linestyle=(0, (5, 3)), alpha=0.75, zorder=4)

    draw_water_surface(ax)
    draw_bed(ax)
    draw_braces(ax, layer_bottoms, layer_tops, n_layers)

# ── Draw panels (a)–(d): 1-layer through 4-layer ─────────────────────────────
for idx, n_layers in enumerate([1, 2, 3, 4]):
    ax = axes[idx]
    edges    = np.linspace(0, hv, n_layers + 1)
    ltops    = edges[1:][::-1]    # topmost first
    lbottoms = edges[:-1][::-1]
    draw_layer_panel(ax, lbottoms, ltops, n_layers)
    setup_ax(ax, idx)

# ── Save ──────────────────────────────────────────────────────────────────────
os.makedirs("output", exist_ok=True)
out_path = "output/veg_multilayer_revised_2026.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="#FAFAFA")

print(f"Saved to {out_path}")
