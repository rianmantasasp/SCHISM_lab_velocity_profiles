# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:44:52 2026

@author: rianm
"""

"""
Four-Panel Velocity Profile Summary Figure 
==========================================================
Run:  python Figure 2.py
Output: four_panel_velocity_profiles_journal.png
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# =============================================================================
# ── LAYOUT CONTROLS──────────────
# =============================================================================
BASE_FONT   = 18        # base font size (pt) — all others scale from this
FIG_W       = 18        # figure width  (inches)
FIG_H       = 14        # figure height (inches)
FIG_DPI     = 300       # output DPI

# GridSpec spacing — reduce HSPACE/WSPACE to close gaps between panels
HSPACE      = 0.25      # vertical gap between rows   (0 = touching, ~0.4 = wide)
WSPACE      = 0.28      # horizontal gap between cols (0 = touching, ~0.4 = wide)
LEFT        = 0.08      # left margin fraction
RIGHT       = 0.97      # right margin fraction
TOP         = 0.91      # top margin fraction   (leaves room for suptitle)
BOTTOM      = 0.07      # bottom margin fraction

# Suptitle alignment
TITLE_X     = 0.5       # 0.0 = left, 0.5 = centre, 1.0 = right
TITLE_HA    = 'center'  # 'left', 'center', 'right'
TITLE_Y     = 0.97      # vertical position of suptitle

# X-axis tick settings — same pattern across ALL panels
# Set XSTEP to 0.05 or 0.10 as preferred; xlims per panel set below
XSTEP       = 0.05      # tick interval on x-axis  (m/s)
XLIM_A      = (0.00, 0.35)   # panel a  x-limits
XLIM_B      = (0.00, 0.35)   # panel b  x-limits
XLIM_C      = (0.00, 0.35)   # panel c  x-limits
XLIM_D      = (0.00, 0.35)   # panel d  x-limits
YLIM        = (0, 82)        # y-limits — same for all panels (mm)

# =============================================================================
# ── PANEL LABEL STRINGS ───────────
# =============================================================================
PANEL_TITLES = {
    'a': 'Layer configuration sensitivity',
    'b': 'Turbulence closure scheme',
    'c': 'Turbulence closure with diffusivity',
    'd': 'Best configuration agreement with Case A',
}

# Legend label strings — edit here to rename any entry
LAB_LAB   = 'Lab data (Case A)'
BASE_LAB  = 'Base model (ZH)'

# Panel A
LAB_A18   = 'ML2' #2-layer H-18
LAB_B6    = 'ML3' #3-layer I-6
LAB_C1    = 'ML4' #4-layer J-1

# Panel B — turbulence closures
LAB_KE    = r'K-$\varepsilon$'
LAB_KKL   = r'K-KL'
LAB_MY    = r'MY'
LAB_KW    = r'K-$\omega$'
LAB_UB    = r'UB'

# Panel C — diffmin
LAB_KE_DM  = r'K-$\varepsilon$'
LAB_KKL_DM = r'K-KL'
LAB_MY_DM  = r'MY'
LAB_KW_DM  = r'K-$\omega$'
LAB_UB_DM  = r'UB'
LAB_BESTNU = r'Best dfv'

# Panel D — multilayer
LAB_NU_ML  = r'Best dfv-ML'
LAB_KW_ML  = r'K-$\omega$-ML'
LAB_UB_ML  = r'UB-ML'

# =============================================================================
# ── COLOURS — each profile line colour ───────────────────
# =============================================================================
COL_LAB   = 'black'
COL_BASE  = '#555555'   # grey dashed — base model

# Panel A
COL_A18   = '#D84315'   # dark orange
COL_B6    = '#2E7D32'   # dark green
COL_C1    = '#6A1B9A'   # purple

# Panel B
COL_KE    = '#1565C0'   # blue
COL_KKL   = '#6A1B9A'   # purple
COL_MY    = '#00695C'   # teal
COL_KW    = '#E65100'   # orange
COL_UB    = '#AD1457'   # rose

# Panel C
COL_KE_DM  = '#1565C0'
COL_KKL_DM = '#6A1B9A'
COL_MY_DM  = '#E65100'
COL_KW_DM  = '#004D40'
COL_UB_DM  = '#880E4F'
COL_BESTNU = '#B71C1C'  # bold red — highlighted best

# Panel D
COL_NU_ML  = '#1B5E20'  # dark green
COL_KW_ML  = '#0D47A1'  # dark blue
COL_UB_ML  = '#880E4F'  # dark rose

# Vegetation top line
COL_VEGTOP = '#00838F'  # teal annotation

# =============================================================================
# ── DATA — laboratory and base model ─────────────────────────────────────────
# =============================================================================
z_lab = np.array([0.00266,0.0112,0.0158,0.0228,0.028,0.0317,0.0339,0.0364,
                  0.041,0.0445,0.0483,0.0522,0.0561,0.0592,0.0623,0.0653,0.0683,0.0714])
v_lab = np.array([0.075,0.07501,0.0817,0.0898,0.0963,0.1021,0.1111,0.1226,
                  0.1424,0.1594,0.181,0.1904,0.2063,0.2092,0.2333,0.2204,0.2341,0.2439])

z_r32 = np.array([0,0.003731393,0.007462786,0.01119418,0.014925572,0.018656966,
                  0.022388358,0.026119753,0.029851145,0.033582537,0.037313935,
                  0.041045325,0.044776718,0.04850811,0.052239505,0.055970899,
                  0.059702291,0.063433685,0.067165075,0.070896465,0.074627865])
v_r32 = np.array([0,0.079701796,0.08226374,0.08538936,0.0890451,0.09314218,
                  0.09768254,0.10270345,0.10826698,0.114685744,0.12255151,
                  0.13263074,0.14371431,0.15439147,0.16524877,0.17663364,
                  0.18881863,0.20221882,0.21757713,0.2366384,0.2596746])

VEG_TOP = 0.041   # m  (41 mm)
H_TOT   = 0.0747  # m  (74.7 mm)
hv      = VEG_TOP

# =============================================================================
# ── DATA — Panel A ────────────────────────────────────────────────────────────
# =============================================================================
z_A18 = np.array([0.,0.00360764,0.00721529,0.01082293,0.01443057,
                  0.01803821,0.02164586,0.0252535,0.02886115,0.03246879,
                  0.03607643,0.03968407,0.04329171,0.04689936,0.050507,
                  0.05411464,0.05772228,0.06132993,0.06493757,0.06854522,0.07215286])
v_A18 = np.array([0.,0.0792391,0.08265544,0.08676658,0.09149509,
                  0.096736,0.10251022,0.10889041,0.11604163,0.12433522,
                  0.13384758,0.14409713,0.15453953,0.16481389,0.17516206,
                  0.18609236,0.19787937,0.21095192,0.22608855,0.24512823,0.26849657])

z_B6  = np.array([0.,0.00371644,0.00743288,0.01114933,0.01486577,
                  0.01858221,0.02229865,0.02601509,0.02973154,0.03344798,
                  0.03716442,0.04088086,0.0445973,0.04831374,0.05203018,
                  0.05574663,0.05946307,0.06317951,0.06689595,0.07061239,0.07432884])
v_B6  = np.array([0.,0.0796098,0.08219844,0.08536651,0.08907203,
                  0.09322352,0.09782391,0.10291293,0.1085565,0.11508047,
                  0.12298866,0.13237599,0.14286205,0.1538102,0.1649768,
                  0.17669778,0.18927665,0.20317468,0.21921873,0.23934849,0.2641159])

z_C1  = np.array([0.,0.00364263,0.00728526,0.01092789,0.01457052,
                  0.01821316,0.02185578,0.02549841,0.02914104,0.03278368,
                  0.03642631,0.04006894,0.04371157,0.0473542,0.05099683,
                  0.05463947,0.05828209,0.06192473,0.06556735,0.06920999,0.07285262])
v_C1  = np.array([0.,0.07928451,0.08241529,0.08619825,0.09056491,
                  0.09541225,0.1007515,0.10663879,0.11316458,0.12083283,
                  0.13013476,0.14066313,0.15141094,0.16186745,0.17242672,
                  0.1835726,0.19558573,0.20890316,0.22431761,0.24369933,0.26751497])

# =============================================================================
# ── DATA — Panel B ────────────────────────────────────────────────────────────
# =============================================================================
z_ke_best  = np.array([0,0.0037464667,0.0074929353,0.011239404,0.014985872,0.018732341,
                       0.02247881,0.026225278,0.029971747,0.033718213,0.037464686,
                       0.04121115,0.044957623,0.048704088,0.05245056,0.056197025,
                       0.059943497,0.06368996,0.067436434,0.0711829,0.07492937])
v_ke_best  = np.array([0,0.07947127,0.08136112,0.08376118,0.08672072,0.09017917,
                       0.094254576,0.09932515,0.105839856,0.11420499,0.12500161,
                       0.1390819,0.15414214,0.1675455,0.17966385,0.19132657,
                       0.20349316,0.21663465,0.23137939,0.24910466,0.26984936])
z_kkl_best = np.array([0,0.0037406813,0.007481361,0.01122204,0.01496272,0.018703403,
                       0.022444082,0.026184762,0.029925441,0.03366612,0.037406802,
                       0.041147485,0.04488816,0.048628844,0.05236952,0.056110203,
                       0.05985088,0.06359156,0.06733224,0.07107292,0.074813604])
v_kkl_best = np.array([0,0.08303369,0.085222214,0.087958746,0.091245465,0.0950158,
                       0.09927684,0.10406638,0.10944434,0.11567699,0.12334054,
                       0.13320744,0.14425024,0.15507571,0.1660644,0.17763613,
                       0.1901084,0.20395492,0.22002168,0.2403499,0.26572546])
z_my_best  = np.array([0,0.0037392937,0.007478589,0.011217883,0.014957178,0.018696472,
                       0.022435766,0.02617506,0.029914357,0.03365365,0.037392944,
                       0.041132238,0.044871535,0.048610825,0.052350122,0.05608942,
                       0.05982871,0.06356801,0.06730729,0.07104659,0.07478589])
v_my_best  = np.array([0,0.0795125,0.08208169,0.08521957,0.08889729,0.09302566,
                       0.09761125,0.102695785,0.10834517,0.11495437,0.12315965,
                       0.13367218,0.14519846,0.15620077,0.16729286,0.17892398,
                       0.191376,0.2050839,0.22083418,0.24045031,0.2643697])
z_kw_best  = np.array([0,0.0033710543,0.0067421068,0.010113161,0.0134842135,0.016855266,
                       0.020226318,0.02359737,0.026968423,0.03033948,0.033710532,
                       0.037081584,0.040452637,0.04382369,0.04719474,0.050565794,
                       0.053936847,0.0573079,0.06067896,0.06405001,0.067421064])
v_kw_best  = np.array([0,0.06693635,0.0689987,0.07142523,0.07426022,0.077691525,
                       0.08186698,0.08711633,0.09382956,0.102495566,0.11385835,
                       0.12890255,0.14876916,0.1614558,0.1822593,0.20462133,
                       0.22703205,0.25285238,0.28103107,0.312192,0.34494343])
z_ub_best  = np.array([0,0.00356506,0.00713012,0.01069518,0.01426024,0.017825302,
                       0.02139036,0.024955422,0.02852048,0.03208554,0.035650603,
                       0.03921566,0.04278072,0.046345785,0.049910843,0.0534759,
                       0.057040967,0.060606025,0.06417108,0.06773614,0.07130121])
v_ub_best  = np.array([0,0.06843214,0.07023195,0.07192768,0.07379398,0.07623031,
                       0.07942986,0.0837899,0.089817174,0.09824436,0.11016467,
                       0.12725271,0.15130629,0.17644922,0.19688208,0.21386865,
                       0.228599,0.24282838,0.25826743,0.276512,0.29806107])

# =============================================================================
# ── DATA — Panel C ────────────────────────────────────────────────────────────
# =============================================================================
z_ke_dm  = np.array([0,0.0037445668,0.0074891336,0.011233702,0.014978269,0.018722838,
                     0.022467406,0.026211971,0.02995654,0.033701107,0.03744567,
                     0.041190244,0.04493481,0.048679374,0.052423947,0.05616851,
                     0.059913076,0.06365765,0.067402214,0.07114678,0.07489135])
v_ke_dm  = np.array([0,0.08331418,0.08377742,0.08522299,0.087870225,0.09146278,
                     0.0956078,0.10072294,0.107326485,0.11582204,0.12676653,
                     0.14093554,0.1560046,0.16941436,0.18154553,0.19329327,
                     0.20574974,0.2189735,0.2302072,0.23703586,0.2393396])
z_kkl_dm = np.array([0,0.0037318766,0.007463755,0.011195634,0.01492751,0.01865939,
                     0.022391267,0.026123144,0.029855024,0.0335869,0.03731878,
                     0.041050658,0.044782534,0.04851441,0.052246295,0.05597817,
                     0.05971005,0.063441925,0.0671738,0.07090568,0.07463756])
v_kkl_dm = np.array([0,0.082852915,0.08345349,0.085334815,0.088761665,0.09327497,
                     0.09818635,0.10351593,0.109323815,0.115976416,0.12411227,
                     0.13452663,0.14601448,0.15711582,0.16848516,0.18063508,
                     0.19395548,0.20800032,0.21957208,0.22651477,0.2288289])
z_my_dm  = np.array([0,0.003729755,0.00745951,0.011189265,0.01491902,0.018648773,
                     0.02237853,0.026108284,0.029838037,0.033567794,0.037297547,
                     0.041027304,0.044757057,0.04848681,0.052216563,0.055946324,
                     0.059676077,0.06340583,0.06713559,0.07086533,0.074595094])
v_my_dm  = np.array([0,0.08283765,0.08344081,0.08533016,0.08874635,0.09320386,
                     0.09803315,0.10327844,0.10903812,0.11574383,0.1240524,
                     0.13470943,0.14642735,0.15763776,0.16899422,0.18105651,
                     0.19425444,0.20821717,0.21975644,0.22667965,0.22898729])
z_kw_dm  = np.array([0,0.003672447,0.007344894,0.011017339,0.0146897845,0.018362232,
                     0.022034679,0.025707126,0.029379573,0.033052016,0.036724463,
                     0.04039691,0.044069357,0.047741804,0.051414248,0.0550867,
                     0.05875914,0.062431585,0.06610404,0.069776475,0.073448926])
v_kw_dm  = np.array([0,0.07819344,0.07843552,0.07917815,0.08048579,0.08247444,
                     0.08532433,0.089301795,0.09479448,0.10236831,0.112862185,
                     0.12755138,0.14752382,0.16897416,0.18756802,0.2033041,
                     0.21618111,0.22619796,0.23335366,0.23764746,0.23907882])
z_ub_dm  = np.array([0,0.0036774334,0.0073548667,0.011032298,0.01470973,0.018387165,
                     0.022064596,0.025742028,0.029419463,0.033096895,0.036774326,
                     0.04045176,0.044129193,0.047806624,0.05148406,0.055161487,
                     0.058838923,0.06251636,0.06619379,0.06987122,0.07354866])
v_ub_dm  = np.array([0,0.07832325,0.07856589,0.07931032,0.08062147,0.08261619,
                     0.08547604,0.08946955,0.094987735,0.10260189,0.11315966,
                     0.127951,0.14806399,0.16931191,0.18721415,0.2021348,
                     0.21469106,0.22477594,0.23198016,0.23630305,0.23774408])
z_best_nu = np.array([0,0.003672447,0.007344894,0.011017339,0.0146897845,0.018362232,
                      0.022034679,0.025707126,0.029379573,0.033052016,0.036724463,
                      0.04039691,0.044069357,0.047741804,0.051414248,0.0550867,
                      0.05875914,0.062431585,0.06610404,0.069776475,0.073448926])
v_best_nu = np.array([0,0.07819344,0.07843552,0.07917815,0.08048579,0.08247444,
                      0.08532433,0.089301795,0.09479448,0.10236831,0.112862185,
                      0.12755138,0.14752382,0.16897416,0.18756802,0.2033041,
                      0.21618111,0.22619796,0.23335366,0.23764746,0.23907882])

# =============================================================================
# ── DATA — Panel D ────────────────────────────────────────────────────────────
# =============================================================================
z_best_nu_ml = np.array([0,0.003633704,0.007267408,0.010901112,0.014534816,0.01816852,
                          0.021802224,0.025435928,0.029069632,0.032703336,0.03633704,
                          0.039970744,0.043604452,0.047238152,0.05087186,0.05450556,
                          0.05813927,0.06177297,0.06540668,0.06904037,0.07267408])
v_best_nu_ml = np.array([0,0.07816249,0.07843518,0.07927184,0.08074362,0.08297857,
                          0.08617588,0.090630434,0.096772596,0.1052333,0.116953135,
                          0.1333731,0.15389355,0.17437638,0.1921331,0.20716189,
                          0.21946105,0.22902901,0.23586446,0.2399663,0.24133371])
z_kw_ml = np.array([0,0.003633704,0.007267408,0.010901112,0.014534816,0.01816852,
                    0.021802224,0.025435928,0.029069632,0.032703336,0.03633704,
                    0.039970744,0.043604452,0.047238152,0.05087186,0.05450556,
                    0.05813927,0.06177297,0.06540668,0.06904037,0.07267408])
v_kw_ml = np.array([0,0.07816249,0.07843518,0.07927184,0.08074362,0.08297857,
                    0.08617588,0.090630434,0.096772596,0.1052333,0.116953135,
                    0.1333731,0.15389355,0.17437638,0.1921331,0.20716189,
                    0.21946105,0.22902901,0.23586446,0.2399663,0.24133371])
z_ub_ml = np.array([0,0.0036413576,0.0072827134,0.010924071,0.014565427,0.018206783,
                    0.021848142,0.025489498,0.029130854,0.03277221,0.03641357,
                    0.040054925,0.043696284,0.047337636,0.050978996,0.054620348,
                    0.058261707,0.061903067,0.06554442,0.06918578,0.07282714])
v_ub_ml = np.array([0,0.07837505,0.078648545,0.07948784,0.08096484,0.08320898,
                    0.08642168,0.090901405,0.09708414,0.105609775,0.11743365,
                    0.13402183,0.15461856,0.17457733,0.191323,0.20532547,
                    0.21724313,0.22691694,0.23382783,0.23797487,0.23935734])

# =============================================================================
# ── LAYER ANNOTATION ──────────────────────────────────────────────────
# =============================================================================
def draw_layer_band(ax, z_bot_m, z_top_m, color, alpha=0.10):
    ax.axhspan(z_bot_m*1000, z_top_m*1000, color=color, alpha=alpha, zorder=2)
    ax.axhline(z_top_m*1000, color=color, lw=0.7, ls='-', alpha=0.4, zorder=3)

def draw_thickness_arrow(ax, z_bot_m, z_top_m, label, x_frac,
                         color='#333', fsize=None, right_offset=0.010):
    """Double-headed arrow showing layer thickness — all in black/dark by default."""
    if fsize is None:
        fsize = BASE_FONT - 3
    xlim = ax.get_xlim()
    xpos = xlim[0] + (xlim[1] - xlim[0]) * x_frac
    y0, y1 = z_bot_m*1000, z_top_m*1000
    if abs(y1 - y0) < 0.5:
        return
    ax.annotate('', xy=(xpos, y0), xytext=(xpos, y1),
                annotation_clip=False,
                arrowprops=dict(arrowstyle='<->', color=color,
                                lw=0.9, mutation_scale=5))
    ax.text(xpos + (xlim[1]-xlim[0])*right_offset, (y0+y1)/2,
            label, ha='left', va='center', fontsize=fsize,
            color=color, clip_on=False)

# =============================================================================
# ── FIGURE SETUP ──────────────────────────────────────────────────────────────
# =============================================================================
plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'font.size':          BASE_FONT,
    'text.color':         'black',
    'axes.labelcolor':    'black',
    'xtick.color':        'black',
    'ytick.color':        'black',
    'axes.edgecolor':     'black',
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.grid':          False,       #white background, no grid
    'axes.facecolor':     'white',
    'figure.facecolor':   'white',
    'axes.labelsize':     BASE_FONT,
    'axes.titlesize':     BASE_FONT + 1,
    'xtick.labelsize':    BASE_FONT - 1,
    'ytick.labelsize':    BASE_FONT - 1,
    'legend.fontsize':    BASE_FONT - 2,
    'legend.framealpha':  0.90,
    'legend.edgecolor':   '#cccccc',
})

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=FIG_DPI)

gs = gridspec.GridSpec(2, 2, figure=fig,
                       hspace=HSPACE, wspace=WSPACE,
                       left=LEFT, right=RIGHT,
                       top=TOP, bottom=BOTTOM)

axes = [fig.add_subplot(gs[0, 0]),
        fig.add_subplot(gs[0, 1]),
        fig.add_subplot(gs[1, 0]),
        fig.add_subplot(gs[1, 1])]

# =============================================================================
# ── AXIS FORMAT───────────────────────────────────────────────────
# =============================================================================
def fmt_ax(ax, letter, xlim, veg_label_right=False):
    """Apply consistent journal formatting to an axes."""
    ax.set_xlabel(r'Velocity (m s$^{-1}$)', fontsize=BASE_FONT, color='black', labelpad=3)
    ax.set_ylabel('Height above bed (mm)', fontsize=BASE_FONT, color='black', labelpad=3)
    ax.set_ylim(*YLIM)
    ax.set_xlim(*xlim)

    # Consistent x-axis ticks — same step everywhere
    # The x=0 tick label is suppressed because 0 already appears on the y-axis,
    # so the two zeros would overlap at the origin corner.
    xticks = np.arange(xlim[0], xlim[1] + XSTEP*0.01, XSTEP)
    ax.set_xticks(xticks)
    ax.set_xticklabels(['' if np.isclose(t, 0.0) else f'{t:.2f}'.rstrip('0').rstrip('.')
                        for t in xticks])
    ax.tick_params(axis='both', which='both', direction='in',
                   labelcolor='black', color='black')

    # Panel label and title — all black, left-aligned
    ax.set_title(f'({letter})  {PANEL_TITLES[letter]}',
                 fontsize=BASE_FONT + 1, fontweight='bold',
                 color='black', loc='left', pad=6)

    # Vegetation top reference line + annotation (black/dark, no colour)
    ax.axhline(VEG_TOP*1000, color=COL_VEGTOP, lw=1.2, ls='--', alpha=0.75, zorder=1)
    xlim_cur = ax.get_xlim()
    if veg_label_right:
        ax.text(xlim_cur[1] - (xlim_cur[1]-xlim_cur[0])*0.02,
                VEG_TOP*1000 + 0.8,
                f'veg height = {VEG_TOP*1000:.0f} mm',
                fontsize=BASE_FONT - 3, color=COL_VEGTOP,
                va='bottom', ha='right', style='italic')
    else:
        ax.text(xlim_cur[0] + (xlim_cur[1]-xlim_cur[0])*0.02,
                VEG_TOP*1000 + 0.8,
                f'veg height = {VEG_TOP*1000:.0f} mm',
                fontsize=BASE_FONT - 3, color=COL_VEGTOP,
                va='bottom', ha='left', style='italic')

    ax.legend(loc='upper left', frameon=True,
              handlelength=2.0, labelspacing=0.30,
              borderpad=0.5, handletextpad=0.5)

def add_lab(ax):
    ax.scatter(v_lab, z_lab*1000, s=28, c=COL_LAB, zorder=10,
               label=LAB_LAB, marker='o')

def add_base(ax):
    ax.plot(v_r32, z_r32*1000, color=COL_BASE, lw=1.6, ls='--',
            zorder=6, label=BASE_LAB)

# =============================================================================
# ── PANEL A — Layer configuration sensitivity ─────────────────────────────────
# =============================================================================
ax = axes[0]
add_lab(ax)
add_base(ax)

# Shaded canopy bands — subtle, same colour as their profile line
draw_layer_band(ax, hv-0.30*hv, hv,         COL_A18, alpha=0.10)
draw_layer_band(ax, 0.,          hv-0.30*hv, COL_A18, alpha=0.05)
draw_layer_band(ax, hv-0.10*hv, hv,          COL_B6,  alpha=0.10)
draw_layer_band(ax, hv-0.40*hv, hv-0.10*hv, COL_B6,  alpha=0.06)
draw_layer_band(ax, 0.,          hv-0.40*hv, COL_B6,  alpha=0.03)

ax.plot(v_A18, z_A18*1000, color=COL_A18, lw=1.9, ls='-',  zorder=7, label=LAB_A18)
ax.plot(v_B6,  z_B6*1000,  color=COL_B6,  lw=1.9, ls='-',  zorder=7, label=LAB_B6)
ax.plot(v_C1,  z_C1*1000,  color=COL_C1,  lw=1.9, ls='-',  zorder=7, label=LAB_C1)

fmt_ax(ax, 'a', XLIM_A)

# Layer thickness arrows — colour matches profile, label in same dark colour
xlim = ax.get_xlim()
af = BASE_FONT - 3
# ML2
draw_thickness_arrow(ax, hv-0.30*hv, hv,         'd1', 0.76, COL_A18, af)
draw_thickness_arrow(ax, 0.,          hv-0.30*hv, 'd2', 0.76, COL_A18, af)
ax.text(xlim[0]+(xlim[1]-xlim[0])*0.76, hv*1000+1.0, 'ML2',
        fontsize=af, color=COL_A18, ha='left', clip_on=False, fontweight='bold')
# ML3
draw_thickness_arrow(ax, hv-0.10*hv, hv,          'd1', 0.86, COL_B6, af)
draw_thickness_arrow(ax, hv-0.40*hv, hv-0.10*hv, 'd2', 0.86, COL_B6, af)
draw_thickness_arrow(ax, 0.,          hv-0.40*hv, 'd3', 0.86, COL_B6, af)
ax.text(xlim[0]+(xlim[1]-xlim[0])*0.86, hv*1000+1.0, 'ML3',
        fontsize=af, color=COL_B6, ha='left', clip_on=False, fontweight='bold')
# ML4
draw_thickness_arrow(ax, hv-0.10*hv, hv,          'd1', 0.96, COL_C1, af)
draw_thickness_arrow(ax, hv-0.20*hv, hv-0.10*hv, 'd2', 0.96, COL_C1, af)
draw_thickness_arrow(ax, hv-0.30*hv, hv-0.20*hv, 'd3', 0.96, COL_C1, af)
draw_thickness_arrow(ax, 0.,          hv-0.30*hv, 'd4', 0.96, COL_C1, af)
ax.text(xlim[0]+(xlim[1]-xlim[0])*0.96, hv*1000+1.0, 'ML4',
        fontsize=af, color=COL_C1, ha='left', clip_on=False, fontweight='bold')

# =============================================================================
# ── PANEL B — Best turbulence closure per scheme ──────────────────────────────
# =============================================================================
ax = axes[1]
add_lab(ax)
add_base(ax)

closures_B = [
    (LAB_KE,  z_ke_best,  v_ke_best,  COL_KE,  '-'),
    (LAB_KKL, z_kkl_best, v_kkl_best, COL_KKL, '--'),
    (LAB_MY,  z_my_best,  v_my_best,  COL_MY,  '-.'),
    (LAB_KW,  z_kw_best,  v_kw_best,  COL_KW,  ':'),
    (LAB_UB,  z_ub_best,  v_ub_best,  COL_UB,  '-'),
]
for lbl, zm, vm, col, ls in closures_B:
    ax.plot(vm, zm*1000, color=col, lw=1.8, ls=ls, zorder=7, label=lbl)

fmt_ax(ax, 'b', XLIM_B)

# =============================================================================
# ── PANEL C — Best diffmin per turbulence closure ─────────────────────────────
# =============================================================================
ax = axes[2]
add_lab(ax)
add_base(ax)

diffmin_cases = [
    (LAB_KE_DM,  z_ke_dm,  v_ke_dm,  COL_KE_DM,  '--'),
    (LAB_KKL_DM, z_kkl_dm, v_kkl_dm, COL_KKL_DM, '-.'),
    (LAB_MY_DM,  z_my_dm,  v_my_dm,  COL_MY_DM,  ':'),
    (LAB_KW_DM,  z_kw_dm,  v_kw_dm,  COL_KW_DM,  '-'),
    (LAB_UB_DM,  z_ub_dm,  v_ub_dm,  COL_UB_DM,  '--'),
]
for lbl, zm, vm, col, ls in diffmin_cases:
    ax.plot(vm, zm*1000, color=col, lw=1.7, ls=ls, zorder=7, label=lbl)

# Highlighted best nu — bold solid line
ax.plot(v_best_nu, z_best_nu*1000, color=COL_BESTNU, lw=2.8, ls='-',
        zorder=9, label=LAB_BESTNU)

fmt_ax(ax, 'c', XLIM_C, veg_label_right=True)

# =============================================================================
# ── PANEL D — Best diffusivity + multilayer (ML) ──────────────────────────────
# =============================================================================
ax = axes[3]
add_lab(ax)
add_base(ax)

# Thin top-layer band — 1% of hv
d_ml = 0.01 * hv
draw_layer_band(ax, hv - d_ml, hv, '#444444', alpha=0.08)

ax.plot(v_best_nu_ml, z_best_nu_ml*1000, color=COL_NU_ML, lw=2.2, ls='-',
        zorder=8, label=LAB_NU_ML)
ax.plot(v_kw_ml,      z_kw_ml*1000,      color=COL_KW_ML, lw=2.0, ls='--',
        zorder=7, label=LAB_KW_ML)
ax.plot(v_ub_ml,      z_ub_ml*1000,      color=COL_UB_ML, lw=2.0, ls='-.',
        zorder=7, label=LAB_UB_ML)

fmt_ax(ax, 'd', XLIM_D)

# 1% layer thickness arrow
draw_thickness_arrow(ax, hv - d_ml, hv, 'dv1 = 1%\n(all ML)',
                     0.88, '#333333', BASE_FONT - 3)

# =============================================================================
# ── FIGURE TITLE ──────────────────────────────────────────────────────────────
# =============================================================================
# TITLE_X:  0.0=left edge, 0.5=centre, 1.0=right edge
# TITLE_HA: 'left', 'center', 'right'
#fig.suptitle(
#    'Velocity Profile Sensitivity Analysis — Shimizu & Tsujimoto (1994)\n'
#    'SCHISM model configurations vs laboratory data',
#    fontsize=BASE_FONT + 2,
#    fontweight='bold',
#    color='black',            # if want color black
#    x=TITLE_X,
#    ha=TITLE_HA,
#    y=TITLE_Y,
#)
# i think this title is not necessary after revision yesterday
# =============================================================================
# ── SAVE ─────────────────────────────────────────────────
# =============================================================================
os.makedirs('output', exist_ok=True)
fig.savefig('output/four_panel_velocity_profiles_journal.png',
            dpi=FIG_DPI, bbox_inches='tight', facecolor='white')
print('Saved: output/four_panel_velocity_profiles_journal.png')
plt.show()
