# -*- coding: utf-8 -*-
import matplotlib.pyplot as _plt
import itertools as _itertools
import warnings as _warnings
import matplotlib as _mpl
import numpy as _np
import sys as _sys
import os as _os

def mtext(s):
    """
    Puts string into a latex math environment.

    :param s: string to be placed in math environment
    :type s: str
    """
    return r'$\mathtt{%s}$' % s

def convert(ifile, ofile, density=300):
    command = r'convert -density %d -quality 100%% %s %s' % (density, ifile,
                                                             ofile)
    _os.system(command)

def crop(name, border=10):
    if not _os.path.isfile(name):
        return
    stub, ext = _os.path.splitext(name)
    if ext == '.pdf':
        command = 'pdfcrop -margins %d %s %s' % (border, name, name)
    else:
        command = 'convert -trim -border %d -bordercolor white %s %s' % (
            border, name, name)
    _os.system(command)

def save(name, border=10, **kwargs):
    _plt.savefig(name, **kwargs)
    crop(name, border)

def square(axis=None):
    if axis is None: axis = _plt.gca()
    xmin, xmax = axis.get_xlim()
    ymin, ymax = axis.get_ylim()
    axis.set_aspect((xmax-xmin)/(ymax-ymin))

def zoom(axis=None, factor=0.05, l=None, r=None, t=None, b=None):
    if axis is None: axis = _plt.gca()
    if l == None: l = factor
    if r == None: r = factor
    if t == None: t = factor
    if b == None: b = factor
    l = 0 - l
    r = 1 + r
    b = 0 - b
    t = 1 + t
    transform = lambda x,y : axis.transData.inverted().transform(
        axis.transAxes.transform((x,y)))
    xmin, ymin = transform(l,b)
    xmax, ymax = transform(r,t)
    axis.set_xlim(xmin=xmin, xmax=xmax)
    axis.set_ylim(ymin=ymin, ymax=ymax)

def shift_subplots(fig=None, horizontal=0.0, vertical=0.0):
    if fig is None:
        fig = _plt.gcf()
    subplot = fig.subplotpars
    l = subplot.left + horizontal
    r = subplot.right + horizontal
    t = subplot.top + vertical
    b = subplot.bottom + vertical
    _plt.subplots_adjust(left=l, right=r, top=t, bottom=b)

def create_colorbar_axes(axis=None, shift=0.01, width=0.05):
    if axis is None:
        axis = _plt.gca()
    box = axis.get_position()
    cax = _plt.axes([box.x1 + shift, box.y0, width, box.height])
    _plt.sca(axis)
    return cax

def fix_colorbar_labels(cax):
    _plt.draw()
    shift = max([t.get_window_extent().width
        for t in cax.yaxis.get_ticklabels()])
    for t in cax.yaxis.get_ticklabels():
        t.set_ha('right')
        trans = t.get_transform()
        x, y  = t.get_position()
        x, y  = trans.transform([(x, y)])[0]
        x, y  = trans.inverted().transform([(x + shift, y)])[0]
        t.set_position((x, y))

def fake_alpha(rgb, alpha):
    rgb = _mpl.colors.colorConverter.to_rgb(rgb)
    rgb = [1 - alpha + alpha * c for c in rgb]
    return rgb

colors = {}
colors['r1'] = '#fe2712'
colors['r2'] = '#fd5308'
colors['o1'] = '#fb9902'
colors['o2'] = '#fabc02'
colors['y1'] = '#fefe33'
colors['g1'] = '#d0ea2b'
colors['g2'] = '#66b032'
colors['b1'] = '#0392ce'
colors['b2'] = '#0247fe'
colors['p1'] = '#3d01a4'
colors['p2'] = '#8601af'
colors['p3'] = '#a7194b'

def subplots(w=6, h=6, l=1.75, r=0.5, t=1.0, b=1.25, twinx=False):
    w = float(l + w + r)
    h = float(b + h + t)
    fig, ax1 = _plt.subplots(1, 1, figsize=(w, h))
    _plt.subplots_adjust(left=l/w, right=(w-r)/w, bottom=b/h, top=(h-t)/h)
    if twinx:
        ax2 = _plt.twinx(ax1)
        _plt.sca(ax2)
        _plt.tick_params(axis='y', labelright=False)
        _plt.sca(ax1)
        return fig, (ax1, ax2)
    return fig, ax1

def rectangle(x0, y0, x1, y1, axis=None, **kwargs):
    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
    _kwargs = dict(fc='r', lw=0, alpha=0.5)
    _kwargs.update(kwargs)
    rect = _mpl.patches.Rectangle((x0, y0), x1 - x0, y1 - y0, **_kwargs)
    _plt.gca().add_patch(rect)
    return rect

def errorbar(x, y, color='r', **kwargs):
    """wrapper around errorbar"""
    _kwargs = {}
    _kwargs.update(color=color, lw=2, ls='-', marker='o', mfc='none',
        mec=color, ms=5, elinewidth=1, capsize=5, ecolor=color)
    _kwargs.update(**kwargs)
    return _plt.errorbar(x, y, **_kwargs)

def transformA(x, y, a=None):
    """
    transform angle from data to screen coordinates
    """
    a = _np.array((a,))
    p = _np.array([(x, y)])
    r = _plt.gca().transData.transform_angles(a, p)[0]
    return r

def transformX(x, transform_from=None, transform_to=None):
    """transform x from axes to data coords"""
    if not transform_to:
        transform_to = _plt.gca().transData

    if not transform_from:
        transform_from = _plt.gca().transAxes

    x = transform_to.inverted().transform(transform_from.transform((x, 1)))[0]
    return x

def transformY(y, transform_from=None, transform_to=None):
    """transform y from axes to data coords"""
    if not transform_to:
        transform_to = _plt.gca().transData

    if not transform_from:
        transform_from = _plt.gca().transAxes

    y = transform_to.inverted().transform(transform_from.transform((1, y)))[1]
    return y

class BarPlot(object):
    def __init__(self, groups, members, rwidth=0.5, gshift=1.0):
        self.xdata = _np.zeros((groups, members))
        self.ydata = _np.zeros((groups, members))
        self.edata = _np.zeros((groups, members))

        self.gwidth = float(gshift * rwidth)
        self.bwidth = self.gwidth / float(members)
        self.centers = _np.arange(0, groups, 1) * gshift

        self.xdata[:,0] = self.centers - 0.5 * self.gwidth
        for i in range(1, members):
            self.xdata[:,i] = self.xdata[:,0] + i * self.bwidth

        self.xmin = self.centers[+0] - self.gwidth
        self.xmax = self.centers[-1] + self.gwidth

        self.xmin = self.centers[+0] - gshift
        self.xmax = self.centers[-1] + gshift

        cmap = _mpl.cm.get_cmap('gist_rainbow')
        self.bcolors = [cmap(v) for v in _np.linspace(0, 1, members)]
        self.blabels = ['bar%d' % i for i in range(members)]
        self.xlabels = ['%d' % i for i in range(groups)]

    def bar(self, index, **kwargs):
        _plt.bar(self.xdata[:,index], self.ydata[:,index], self.bwidth,
             color=self.bcolors[index], yerr=self.edata[:,index], ecolor='k',
             label=mtext(self.blabels[index]))

    def break_axes(self, x0_id, x1_id, bottom=True, w=0.025, h=0.04,
                   zorder=99999):
        taxes = _plt.gca().transAxes
        tdata = _plt.gca().transData
        blend = _mpl.transforms.blended_transform_factory(tdata, taxes)
        x0 = 0.5 * (self.centers[x1_id] + self.centers[x0_id])
        y0 = 1.0
        if bottom:
            y0 = 0.0
        x0, y0 = taxes.inverted().transform(blend.transform((x0, y0)))
        x0 = x0 - 0.5 * w
        y0 = y0 - 0.5 * h
        line_kwargs = dict(transform=taxes, clip_on=False, zorder=zorder + 1,
                           color='k', lw=2, ls='-')
        rect_kwargs = dict(transform=taxes, clip_on=False, zorder=zorder,
                           fc='w', ec='w')
        _plt.plot([x0, x0], [y0, y0 + h], 'k-', **line_kwargs)
        _plt.plot([x0 + w, x0 + w], [y0, y0 + h], **line_kwargs)
        rect = _plt.Rectangle((x0, y0), w, h, **rect_kwargs)
        _plt.gca().add_patch(rect)

    def plot(self):
        self.edata[_np.isnan(self.edata)] = 0
        for i in range(self.xdata.shape[1]):
            self.bar(i)
        _plt.xticks(self.centers, self.xlabels)
        _plt.xlim(self.xmin, self.xmax)

class PeakFinder:
    def __init__(self, figure=None, mode='fit', handle=None, callback=None,
                 savename='plot.pdf'):
        if figure is None:
            self.figure = _plt.gcf()
        else:
            self.figure = figure

        self.figure.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.figure.canvas.mpl_connect('pick_event', self.on_pick)

        self.selectors = []
        for axis in self.figure.axes:
            selector = _mpl.widgets.RectangleSelector(axis, self.on_select,
                minspanx=10, minspany=10, spancoords='pixels', button=1,
                rectprops=dict(lw=1, ls='dashed', ec='k', fc='none'))
            self.selectors.append(selector)

        modes = ['min', 'max', 'fit']
        assert mode in modes
        self.mode_iter = _itertools.cycle(modes)
        self.mode = self.mode_iter.next()
        while not self.mode == mode:
            self.mode = self.mode_iter.next()

        self.x_data = None
        self.y_data = None
        self.axis = None
        self.results = []
        self.refs = []

        self.plot_xline = True
        self.plot_yline = False
        self.plot_point = False
        self.plot_xtext = True
        self.plot_ytext = False
        self.prop_point = dict(color='w', marker='o', zorder=-99)
        self.prop_xline = dict(color='k', ls='-', lw=1, zorder=-100)
        self.prop_yline = dict(color='k', ls='-', lw=1, zorder=-100)

        self.prop_xtext = dict(size=8, ha='center', va='bottom', rotation=90,
                               bbox=dict(fc='white', ec='none'))
        self.prop_xtext_fmt = '%.3f'
        self.prop_xtext_loc = 1.02

        self.prop_ytext = dict(size=8, ha='left', va='center', rotation=0,
                               bbox=dict(fc='white', ec='none'))
        self.prop_ytext_fmt = '%.3f'
        self.prop_ytext_loc = 1.02

        self.handle = handle
        if self.handle == None:
            self.handle = 'peaks.dat'

        self.callback = callback
        self.savename = savename

        self.message('init = ok')

    def on_key_press(self, event):
        if event.key == 'm':
            self.next_mode()

        elif event.key == 'h':
            self.help_message()

        elif event.key == 'p':
            self.save(_sys.stdout)

        elif event.key == 'w':
            self.save(self.handle)
            save(self.savename)

        elif event.key == 'c':
            if hasattr(self.callback, '__call__'):
                self.message('callback function called')
                try:
                    self.callback(self)
                except:
                    self.callback()
            else:
                self.message('no callback function installed')

        elif event.key == 'ctrl+z':
            self.undo()

    def on_pick(self, event):
        if event.mouseevent.button == 1:

            if isinstance(event.artist, _mpl.lines.Line2D):
                self.x_data = event.artist.get_xdata(orig=True)
                self.y_data = event.artist.get_ydata(orig=True)

            elif isinstance(event.artist, _mpl.patches.Polygon):
                xy = event.artist.get_xy()
                self.x_data = xy[:,0]
                self.y_data = xy[:,1]

            elif isinstance(event.artist, _mpl.patches.Rectangle):
                x = event.artist.get_x()
                #w = event.artist.get_width()
                h = event.artist.get_height()
                self.x_data = _np.array([x])
                self.y_data = _np.array([h])

            else:
                self.message('can not select %s' % event.artist)

            try:
                self.x_data.size
                self.y_data.size
                self.axis = event.artist.get_axes()
                self.message('selected %s' % event.artist)
            except:
                self.x_data = None
                self.y_data = None
                self.axis = None

    def on_select(self, pos_0, pos_1):

        if not self.axis:
            self.message('selector not in axis')
            return

        if self.x_data is None or self.y_data is None:
            self.message('first click on an artist, then select data region')
            self.x_data = None
            self.y_data = None
            return

        x0, x1 = sorted((pos_0.xdata, pos_1.xdata))
        y0, y1 = sorted((pos_0.ydata, pos_1.ydata))

        slicer = (self.x_data >= x0) & (self.x_data <= x1) & \
                 (self.y_data >= y0) & (self.y_data <= y1)

        x_narrow = self.x_data[slicer]
        y_narrow = self.y_data[slicer]

        if not x_narrow.size or not y_narrow.size:
            self.message('no data in selection')
            return

        if self.mode is 'max':
            x, y = self.find_ymax(x_narrow, y_narrow)

        elif self.mode is 'min':
            x, y = self.find_ymin(x_narrow, y_narrow)

        elif self.mode is 'fit':
            x, y = self.find_extrema(x_narrow, y_narrow)

        else:
            self.message('invalid mode - %s' % self.mode)
            self.mode = 'min'
            return

        if not x is None and not y is None:
            axis_id = self.figure.axes.index(self.axis)
            result = (x, y, axis_id, self.mode)
            if not result in self.results:
                self.results.append(result)
                self.label_peak(x, y)
                self.message('(%g, %g)' % (x, y))
                self.sort_results()

    def sort_results(self):
        self.results.sort(key=lambda x : (x[2], x[0]))

    def label_peak(self, x_val, y_val):

        ref = []

        if self.plot_yline:
            ref.append(self.axis.axhline(y_val, **self.prop_yline))

        if self.plot_xline:
            ref.append(self.axis.axvline(x_val, **self.prop_xline))

        if self.plot_point:
            ref.extend(self.axis.plot(x_val, y_val, **self.prop_point))

        if self.plot_xtext:
            if self.prop_xtext_loc == 'inside':
                x, y = self.axis.transData.transform((x_val, y_val))
                x, y = self.axis.transAxes.inverted().transform((x, y))
                x, y = x_val, 0.5 * (y + 1)
                self.prop_xtext.update(va='center')
            else:
                x, y = x_val, self.prop_xtext_loc
            transform = _mpl.transforms.blended_transform_factory(
                self.axis.transData, self.axis.transAxes)
            ref.append(self.axis.text(x, y, self.prop_xtext_fmt % (x_val),
                transform=transform, **self.prop_xtext))

        if self.plot_ytext:
            transform = _mpl.transforms.blended_transform_factory(
                self.axis.transAxes, self.axis.transData)
            ref.append(self.axis.text(self.prop_ytext_loc, y_val,
                self.prop_ytext_fmt % (y_val), transform=transform,
                **self.prop_ytext))

        self.refs.append(ref)
        self.draw()


    def find_ymax(self, x_data, y_data):
        i = _np.argmax(y_data)
        x = x_data[i]
        y = y_data[i]
        return x, y

    def find_ymin(self, x_data, y_data):
        i = _np.argmin(y_data)
        x = x_data[i]
        y = y_data[i]
        return x, y

    def find_extrema(self, x_data, y_data):
        if x_data.size == 1 and y_data.size == 1:
            return x_data[0], y_data[0]

        xmin, xmax = _np.amin(x_data), _np.amax(x_data)
        ymin, ymax = _np.amin(y_data), _np.amax(y_data)

        with _warnings.catch_warnings():
            _warnings.simplefilter('error', _np.RankWarning)
            try:
                fit = _np.polyfit(x_data, y_data, 2)
            except _np.RankWarning:
                return None, None

        func = _np.poly1d(fit)
        a, b, c = fit
        x = - b / (2*a)
        y = func(x)
        s = 1.025
        if x >= s*xmin and x <= s*xmax and y >= s*ymin and y <= s*ymax:
            return x, y
        return None, None

    def undo(self):
        if self.results:
            assert len(self.refs) == len(self.results)
            for ref in self.refs[-1]:
                ref.remove()
            self.refs.pop()
            self.results.pop()
            self.draw()
            self.message('removed last result')
        else:
            self.message('nothing to undo')

    def next_mode(self):
        self.mode = self.mode_iter.next()
        self.message('mode = %s' % self.mode)

    def help_message(self):
        print ''
        self.message('R-mouse : artist select')
        self.message('L-mouse : data select')
        self.message('ctrl+z  : undo')
        self.message('w       : save')
        self.message('p       : print')
        self.message('c       : callback')
        self.message('m       : mode')
        self.message('h       : help')

    def save(self, out=_sys.stdout):
        if self.results:
            if isinstance(out, str):
                out = open(out, 'w')
            self.message('saving to %s' % out.name)
            print >> out, '%2s %2s %4s %23s %23s' % (
                'id', 'ax', 'mode', 'x', 'y')
            for i, (x, y, a, m) in enumerate(self.results):
                print >> out, '%2d %2d %4s %23.15e %23.15e' % (
                    i, a, m, x, y)
        else:
            self.message('no peaks')

    def message(self, string):
        print 'PeakFinder : %s' % string

    def draw(self):
        self.figure.canvas.draw()
