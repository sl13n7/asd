"""
Mô phỏng Trái Tim 3D - Python
Chạy: python heart_3d.py
Yêu cầu: pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings('ignore')

# ── Tạo colormap trái tim đẹp ──
heart_colors = LinearSegmentedColormap.from_list(
    'heart',
    ['#1a0010', '#660020', '#cc0033', '#ff1a4d', '#ff6699', '#ffb3cc', '#ffe0ec'],
    N=256
)

# ── Tham số hóa bề mặt trái tim 3D ──
U = np.linspace(-np.pi, np.pi, 160)
V = np.linspace(0, 2 * np.pi, 160)
U, V = np.meshgrid(U, V)

# Công thức trái tim 3D
X = np.sin(U)**3 * np.cos(V) * 2.2
Y = (13*np.cos(U) - 5*np.cos(2*U) - 2*np.cos(3*U) - np.cos(4*U)) / 16 * 2.2
Z = np.sin(U)**3 * np.sin(V) * 2.2

# ── Màu sắc theo chiều sâu ──
C = (Y - Y.min()) / (Y.max() - Y.min())

# ── Các điểm hạt xung quanh (hiệu ứng phát sáng) ──
rng = np.random.default_rng(42)
n_particles = 220
theta_p = rng.uniform(0, 2*np.pi, n_particles)
phi_p   = rng.uniform(0, np.pi, n_particles)
r_p     = rng.uniform(2.8, 4.5, n_particles)
px = r_p * np.sin(phi_p) * np.cos(theta_p)
py = r_p * np.sin(phi_p) * np.sin(theta_p)
pz = r_p * np.cos(phi_p)
p_alpha = rng.uniform(0.2, 0.8, n_particles)
p_size  = rng.uniform(4, 28, n_particles)
p_colors = rng.choice(['#ff1a4d','#ff69b4','#ff99cc','#ff6fce','#c77dff','#ffffff','#ffd700'], n_particles)

# ── Thiết lập figure ──
fig = plt.figure(figsize=(10, 9), facecolor='#02000f')
ax = fig.add_subplot(111, projection='3d', facecolor='#02000f')

# Xóa viền trục
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('none')
ax.yaxis.pane.set_edgecolor('none')
ax.zaxis.pane.set_edgecolor('none')
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
ax.grid(False)
for spine in ax.spines.values():
    spine.set_visible(False)

# ── Tiêu đề ──
title = fig.text(0.5, 0.96, '💖  Trái Tim Vũ Trụ  💖',
                  fontsize=20, color='#ff6fce', ha='center', va='top',
                  fontweight='bold',
                  bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a0010',
                            edgecolor='#ff1a4d', alpha=0.8))
subtitle = fig.text(0.5, 0.02, 'Chúc Mừng Ngày Tết Thiếu Nhi 1.6  ✦',
                     fontsize=13, color='#cc99ff', ha='center', va='bottom',
                     style='italic')

# ── Đèn nền: vòng tròn ánh sáng ──
ring_theta = np.linspace(0, 2*np.pi, 200)
ring_x = 2.6 * np.cos(ring_theta)
ring_y = 2.6 * np.sin(ring_theta)
ring_z = np.zeros_like(ring_theta) - 0.5

# ── Surface plot ──
surf = ax.plot_surface(X, Y, Z,
                        facecolors=heart_colors(C),
                        alpha=0.88,
                        rstride=1, cstride=1,
                        antialiased=True,
                        shade=True,
                        lightsource=plt.matplotlib.colors.LightSource(azdeg=315, altdeg=45))

# ── Wireframe nhẹ ──
wire = ax.plot_wireframe(X, Y, Z,
                          color='#ff1a4d', alpha=0.08,
                          rstride=8, cstride=8, linewidth=0.4)

# ── Hạt hào quang ──
scatter = ax.scatter(px, pz, py,
                      c=p_colors, s=p_size,
                      alpha=0.55, depthshade=True,
                      zorder=5)

# ── Vòng sáng ──
ring_line, = ax.plot(ring_x, ring_z, ring_y,
                      color='#ff1a4d', alpha=0.25, linewidth=1.2)

ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_zlim(-3, 4)
ax.view_init(elev=18, azim=0)

# ── Chú thích ──
info = fig.text(0.02, 0.96, 'Python 3D Heart\nNumPy + Matplotlib',
                fontsize=9, color='rgba(255,255,255,0.3)',
                va='top', ha='left',
                color='#554466')

frame_count = [0]

def update(frame):
    fc = frame_count[0]
    frame_count[0] += 1

    # Xoay trái tim
    azim = fc * 1.2
    elev = 18 + np.sin(fc * 0.03) * 8
    ax.view_init(elev=elev, azim=azim)

    # Nhịp đập (pulse)
    pulse = 1.0 + 0.06 * np.sin(fc * 0.18)
    scale = pulse

    # Cập nhật bề mặt với nhịp đập
    ax.collections.clear()

    Xs = X * scale
    Ys = Y * scale
    Zs = Z * scale

    # Cập nhật màu sắc theo frame (chuyển màu nhẹ)
    hue_shift = (np.sin(fc * 0.05) + 1) / 2
    shifted_colors = LinearSegmentedColormap.from_list(
        'shifted',
        [
            f'#{max(0,int(20+hue_shift*20)):02x}0010',
            f'#{max(0,int(80+hue_shift*30)):02x}0025',
            f'#cc0033',
            f'#ff{max(0,int(20+hue_shift*60)):02x}{max(0,int(40+hue_shift*20)):02x}',
            '#ff6699', '#ffb3cc', '#ffe0ec'
        ], N=256
    )
    face_colors = shifted_colors(C)

    ax.plot_surface(Xs, Ys, Zs,
                    facecolors=face_colors,
                    alpha=0.88,
                    rstride=1, cstride=1,
                    antialiased=True,
                    shade=True,
                    lightsource=plt.matplotlib.colors.LightSource(
                        azdeg=315 - fc * 0.8, altdeg=45 + np.sin(fc*0.04)*15))

    ax.plot_wireframe(Xs, Ys, Zs,
                      color='#ff1a4d', alpha=0.07,
                      rstride=8, cstride=8, linewidth=0.4)

    # Hạt quay theo
    ang = fc * 0.025
    cos_a, sin_a = np.cos(ang), np.sin(ang)
    rpx = px * cos_a - py * sin_a
    rpy = px * sin_a + py * cos_a
    ax.scatter(rpx * scale, pz * scale, rpy * scale,
               c=p_colors, s=p_size * (0.8 + 0.2*pulse),
               alpha=0.5 * (0.8 + 0.2 * np.sin(fc*0.12)),
               depthshade=True)

    # Vòng quay
    r_ang = fc * 0.04
    rx2 = ring_x * np.cos(r_ang) - ring_y * np.sin(r_ang)
    ry2 = ring_x * np.sin(r_ang) + ring_y * np.cos(r_ang)
    ax.plot(rx2 * scale, ring_z * scale, ry2 * scale,
            color='#ff1a4d',
            alpha=0.18 + 0.07*np.sin(fc*0.15),
            linewidth=1.0)

    # Thêm vòng thứ hai nghiêng
    rx3 = ring_x * np.cos(r_ang + 1.2) - ring_z * np.sin(r_ang + 1.2)
    rz3 = ring_x * np.sin(r_ang + 1.2) + ring_z * np.cos(r_ang + 1.2)
    ax.plot(rx3 * scale * 1.1, rz3 * scale, ring_y * scale * 1.1,
            color='#c77dff',
            alpha=0.13 + 0.05*np.sin(fc*0.2),
            linewidth=0.8)

    # Nhịp tiêu đề
    alpha_t = 0.85 + 0.15 * np.sin(fc * 0.18)
    title.set_color(f'#{int(255):02x}{int(80+60*np.sin(fc*0.18)):02x}{int(180+40*np.sin(fc*0.12)):02x}')

    ax.set_xlim(-3.8, 3.8)
    ax.set_ylim(-3.8, 3.8)
    ax.set_zlim(-3.2, 4.2)

    return []


print("╔══════════════════════════════════════╗")
print("║   💖  Mô Phỏng Trái Tim 3D  💖      ║")
print("║   Python · NumPy · Matplotlib        ║")
print("╠══════════════════════════════════════╣")
print("║  Đang tải animation...               ║")
print("║  Nhấn Q hoặc đóng cửa sổ để thoát  ║")
print("╚══════════════════════════════════════╝")

ani = animation.FuncAnimation(
    fig, update,
    frames=300,
    interval=40,
    blit=False,
    repeat=True
)

plt.tight_layout(pad=0)
plt.subplots_adjust(left=0, right=1, top=0.95, bottom=0.04)
plt.show()
