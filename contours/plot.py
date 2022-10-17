import matplotlib.pyplot as plt

def plot_surf()
    fig, ax = plt.subplots(figsize=(10,8))
    surf = ax.contourf(X, Y, G, levels=CUTS, colors=[COLOR[c] for c in COLORS], alpha=0, zorder=0)
    # contour = ax.contour(X, Y, G, levels=CUTS, colors=[COLOR[c] for c in COLORS], alpha=1, zorder=0)
    contour = ax.contour(X, Y, G, levels=CUTS, colors='black', alpha=1, zorder=0)
    ax.axis('off')
    ax.axis('scaled')
    ax.set_ylim(-2,2)
    ax.set_xlim(-3,3)
    plt.tight_layout()


# max_plot = plot_rips(ax, P[:,:2], K, THRESH, COLOR['blue'], False, zorder=2)
# min_plot = plot_rips(ax, P[:,:2], K2, args.mult*THRESH, COLOR['red'], not args.comp, zorder=1)
#
#
#
# if args.save and not os.path.exists(args.dir):
#     os.makedirs(args.dir)
#
# Fmin, Fmax = F.min(), F.max()
# levels = [Fmin-Fmax/2] + CUTS + [1.3*Fmax]
# for i, t in enumerate(levels):
#     # if args.no_max:
#     for s in K[2]:
#         if Tmax[s] <= t:
#             max_plot[2][s].set_visible(True)
#     for s in K[1]:
#         if Emax[s] <= t:
#             max_plot[1][s].set_visible(True)
#     # if args.no_min:
#     if args.comp:
#         for s in K2[2]:
#             if Tmin[s] <= t:
#                 min_plot[2][s].set_visible(True)
#         for s in K2[1]:
#             if Emin[s] <= t:
#                 min_plot[1][s].set_visible(True)
#     else:
#         for s in K2[2]:
#             if Tmin[s] <= t:
#                 min_plot[2][s].set_visible(False)
#         for s in K2[1]:
#             if Emin[s] <= t:
#                 min_plot[1][s].set_visible(False)
#     plt.pause(args.wait)
#     if args.save:
#         cmult_s = ('cx' + np.format_float_scientific(args.cmult, trim='-')) if int(args.cmult) != args.mult else ''
#         plt.savefig(os.path.join(args.dir, '%s_lips_tri%s%d%s.png' % (label, '_comp' if args.comp else '',i,cmult_s)), dpi=args.dpi)
