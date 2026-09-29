import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 11), dpi=150)
ax.set_xlim(0, 160); ax.set_ylim(0, 110); ax.axis("off")
fig.patch.set_facecolor("white")

INK = "#1f2937"; MUTED = "#6b7280"
C_USR = "#2563eb"; C_FGT = "#dc2626"; C_SW = "#0f766e"; C_ISP = "#7c3aed"; C_WEB = "#d97706"
C_MG = "#9ca3af"; C_RT = "#0369a1"; C_OK = "#16a34a"


def box(x, y, w, h, title, lines, color, fs=9.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.8",
                                linewidth=2, edgecolor=color, facecolor="white", zorder=3))
    ax.text(x + w/2, y + h - 3.0, title, ha="center", va="center", fontsize=12, fontweight="bold", color=color, zorder=4)
    for i, t in enumerate(lines):
        ax.text(x + w/2, y + h - 6.8 - i*3.1, t, ha="center", va="center", fontsize=fs,
                color=INK, family="DejaVu Sans Mono", zorder=4)


def link(p1, p2, label=None, color=INK, lw=2.2, ls="-", off=(0, 1.8), fs=8.5):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, ls=ls, zorder=2, solid_capstyle="round")
    if label:
        ax.text((p1[0]+p2[0])/2 + off[0], (p1[1]+p2[1])/2 + off[1], label, ha="center", va="center",
                fontsize=fs, color=MUTED, zorder=5, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))


ax.text(80, 107, "Infraestructura 3 — VPN de Acceso Remoto con FortiGate (IPsec + FortiClient)",
        ha="center", fontsize=17, fontweight="bold", color=INK)
ax.text(80, 103.3, "Jose Gabriel Feliz Maria · Matrícula 2025-0742 · Seguridad de Redes (ITLA)",
        ha="center", fontsize=10.5, color=MUTED)

# Internet cloud
ax.add_patch(Ellipse((80, 91), 50, 12.5, facecolor="#f3f4f6", edgecolor=C_MG, lw=2, zorder=1))
ax.text(80, 92.7, "NAT-INTERNET (Cloud0)", ha="center", fontsize=11.5, fontweight="bold", color="#4b5563")
ax.text(80, 89, "192.168.182.0/24 · Internet vía NAT de VMware", ha="center", fontsize=8.8, color=INK,
        family="DejaVu Sans Mono")

# Devices
box(64, 56, 32, 21, "ISP (Cisco IOL)", ["e0/0  200.7.42.1/30", "e0/1  200.7.42.5/30", "e0/2  DHCP (Internet)",
                                         "NAT/PAT hacia Internet"], C_ISP)
box(10, 52, 36, 27, "R-USUARIOS", ["Cisco IOL · Sitio Usuarios", "e0/0 WAN  200.7.42.2/30", "e0/1 LAN  10.7.42.1/25",
                                   "DHCP VLAN 10 (.10 – .126)", "NAT/PAT de los usuarios"], C_RT)
box(114, 52, 36, 27, "FGT-SERVIDOR", ["FortiGate · Sitio Servidor", "port1 MGMT 192.168.182.50", "port2 WAN  200.7.42.6/30",
                                      "port3 LAN  10.7.42.129/28", "VIP 200.7.42.6:443 → .130"], C_FGT)
box(14, 14, 28, 20, "SW-A (Cisco L2)", ["e0/0 acceso VLAN 10", "e0/1 VLAN 10 +", "  port-security (máx 3)",
                                        "e0/2-3 VLAN 999 off"], C_SW, fs=8.6)
box(50, 11, 36, 23, "PC-USUARIO (Cloud4)", ["VM Windows 10 + FortiClient", "DHCP 10.7.42.11/25", "GW 10.7.42.1",
                                              "IP del túnel 10.7.42.162", "(PC host 10.7.42.10)"], C_USR, fs=8.6)
box(118, 14, 28, 20, "Kali-WEB (Cloud1)", ["HTTPS :443 · SSH :22", "10.7.42.130/28", "GW 10.7.42.129"], C_WEB)

# Physical links
link((46.5, 67), (63.5, 67), "e0/0 ↔ e0/0")
link((96.5, 67), (113.5, 67), "e0/1 ↔ port2")
link((80, 77.5), (80, 84.8), "e0/2", off=(4, 0))
link((28, 51.5), (28, 34.5), "e0/1 ↔ e0/0", off=(0, 0))
link((42.5, 24), (49.5, 24), "e0/1", off=(0, 2))
link((132, 51.5), (132, 34.5), "port3", off=(0, 0))

# Management (dashed)
link((98, 88), (132, 79.5), "port1 (gestión)", color=C_MG, ls="--", lw=1.6, off=(3, 2))

# Remote-access IPsec tunnel (FortiClient -> FGT port2)
arc = FancyArrowPatch((86.5, 22), (124, 51.5), connectionstyle="arc3,rad=0.45", arrowstyle="<|-|>",
                      mutation_scale=16, lw=2.6, color=C_FGT, ls="--", zorder=2)
ax.add_patch(arc)
ax.text(77, 48.8, "Túnel IPsec dialup VPN_REMOTO (FortiClient → 200.7.42.6)", ha="center", fontsize=10.2,
        fontweight="bold", color=C_FGT, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"), zorder=6)
ax.text(77, 45.6, "IKEv1 Aggressive · XAuth GRUPO_VPN · DES/SHA1 · DH 14", ha="center", fontsize=9,
        color=INK, family="DejaVu Sans Mono", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=6)
ax.text(77, 42.6, "Pool 10.7.42.161–174 · split tunnel → SSH y PING a 10.7.42.130", ha="center", fontsize=9,
        color=INK, family="DejaVu Sans Mono", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=6)

# HTTPS without VPN
ax.text(77, 38.4, "Sin VPN: https://200.7.42.6 → VIP_WEB_HTTPS → 10.7.42.130:443 (solo HTTPS)",
        ha="center", fontsize=9.6, fontweight="bold", color=C_OK,
        bbox=dict(boxstyle="round,pad=0.25", fc="#f0fdf4", ec=C_OK, lw=1), zorder=6)

ax.text(80, 4.5, "Sin VPN el Usuario solo llega a la web (HTTPS por el VIP); el SSH al servidor solo se permite a los "
        "clientes conectados con FortiClient (política vpn_VPN_REMOTO_remote_0).", ha="center", fontsize=9.3, color=MUTED)

plt.savefig("topologia_infra3.png", bbox_inches="tight", facecolor="white")
print("ok")
