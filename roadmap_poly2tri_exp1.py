# install the poly2tri.python first
# https://github.com/davidcarne/poly2tri.python
import sys

from time import clock
from poly2tri.p2t import *

import pickle

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.patches import Polygon

matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True



def visualize_traj(ws, tri, wp, name=None):
    figure = plt.figure()
    ax = figure.add_subplot(1,1,1)
    # plot boundary
    boundary = ws[0]
    verts = boundary[:] + [boundary[0]]
    codes = [Path.MOVETO] + [Path.LINETO]*(len(verts)-2) + [Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=6, edgecolor='#00bfff')
    ax.add_patch(patch)
    # plot holes
    for hole in ws[1::]:
        verts = hole[:] + [hole[0]]
        codes = [Path.MOVETO] + [Path.LINETO]*(len(verts)-2) + [Path.CLOSEPOLY]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor='#00bfff', lw=2, edgecolor='#00bfff')
        ax.add_patch(patch)
    # ---plot triangles---
    for t in tri:
        polygon = Polygon(t, facecolor='none', edgecolor='black')
        ax.add_patch(polygon)
    # ---plot waypoints---
    for w in wp:
        #ax.text(w[0][0], w[0][1], r'$%s$' %str(w[0]), fontsize=15, fontweight = 'bold')
        plt.plot([w[0][0], w[1][0]], [w[0][1], w[1][1]], 'r', zorder=1, lw=1.5)
        plt.scatter([w[0][0], w[1][0]], [w[0][1], w[1][1]], s=25, c='r', zorder=2)
        #ax.text(w[1][0], w[1][1], r'$%s$' %str(w[1]), fontsize=15, fontweight = 'bold')
        plt.plot([w[0][0], w[2][0]], [w[0][1], w[2][1]], 'r', zorder=1, lw=1.5)
        plt.scatter([w[0][0], w[2][0]], [w[0][1], w[2][1]], s=25, c='r', zorder=2)
        #ax.text(w[2][0], w[2][1], r'$%s$' %str(w[2]), fontsize=15, fontweight = 'bold')
        plt.plot([w[0][0], w[3][0]], [w[0][1], w[3][1]], 'r', zorder=1, lw=1.5)
        plt.scatter([w[0][0], w[3][0]], [w[0][1], w[3][1]], s=25, c='r', zorder=2)
        #ax.text(w[3][0], w[3][1], r'$%s$' %str(w[3]), fontsize=15, fontweight = 'bold')
        plt.plot([w[1][0], w[3][0]], [w[1][1], w[3][1]], 'r', zorder=1, lw=1.5)
        plt.plot([w[1][0], w[2][0]], [w[1][1], w[2][1]], 'r', zorder=1, lw=1.5)
        plt.plot([w[3][0], w[2][0]], [w[3][1], w[2][1]], 'r', zorder=1, lw=1.5)                
    # ---set axes ---
    ax.set_aspect('equal')
    xmax = max([p[0] for p in ws[0]])
    xmin = min([p[0] for p in ws[0]])    
    ymax = max([p[1] for p in ws[0]])
    ymin = min([p[1] for p in ws[0]])
    ax.set_xlim(xmin-0.2, xmax+0.2)
    ax.set_ylim(ymin-0.2, ymax+0.2)
    ax.set_xlabel('$x (m)$')
    ax.set_ylabel('$y (m)$')
    ax.grid('on')
    # plt.axis('off')
    if name:
        plt.savefig('data/%s.pdf' %name,bbox_inches='tight')
    return figure
    
    

boundary = [[0, 0], [2.5, 0.0], [2.5, 2.0], [0.0, 2.0],] # out bound
hole1 = [ [0.6, 0.6], [0.9, 0.6], [0.9, 0.9], [0.6, 0.9],] #obs1
hole2 = [ [1.6, 1.1], [1.9, 1.1], [1.9, 1.4], [1.6, 1.4], ]   #obs2
ws = [boundary, hole1, hole2]


pickle.dump(ws, open('data/ws_lab.p','wb'))

# construct polyline
polyline = []
for p in boundary:
    polyline.append(Point(p[0], p[1]))


# triangulate
print '----triangulate initialize---'
t0 = clock()
cdt = CDT(polyline)

# add holes
print '----add holes---'
holeline1 = []
for p in hole1:
    holeline1.append(Point(p[0], p[1]))
cdt.add_hole(holeline1)    

holeline2 = []
for p in hole2:
    holeline2.append(Point(p[0], p[1]))
cdt.add_hole(holeline2)    

#visualize_traj(ws, set(), set(), 'ws')

# triangulate
print '----triangulation ---'
triangles = cdt.triangulate()
print ("Elapsed time (ms) = " + str(clock()*1000.0))


# parse and draw the triangles
tri = set()
wp = set()
for t in triangles:
    tri.add(((t.a.x, t.a.y), (t.b.x, t.b.y), (t.c.x, t.c.y)))
    wp.add((((t.a.x+t.b.x+t.c.x)/3.0, (t.a.y+t.b.y+t.c.y)/3.0),
            ((t.a.x+t.b.x)*0.5, (t.a.y+t.b.y)*0.5),
            ((t.c.x+t.b.x)*0.5, (t.c.y+t.b.y)*0.5),
            ((t.c.x+t.a.x)*0.5, (t.c.y+t.a.y)*0.5),
        ))

visualize_traj(ws, tri, wp, 'ws_tri_lab')

# print 'Triangles'
# print tri
# print 'Waypoints'
#print wp

pickle.dump(tri, open('data/tris_lab.p','wb'))
pickle.dump(wp, open('data/wps_lab.p','wb'))

# # save the triangles to file
# file_tri = open('tris_lab.txt', 'w')
# for t in tri:
#     file_tri.write(str(t) + '\n')
# file_tri.close()    


# # save the waypoints to file
# file_wps = open('wps_lab.txt', 'w')
# for w in wp:
#     file_wps.write(str(w) + '\n')
# file_wps.close()    
    
















