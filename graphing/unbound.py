#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright (C) 2022, Jan-Philipp Litza (PLUTEX) <jpl@plutex.de>.
# Copyright (C) 2025, Marius Rieder <marius.rieder@scs.ch>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from cmk.graphing.v1 import graphs, metrics, Title

metric_unbound_answers_NOERROR = metrics.Metric(
    name='unbound_answers_NOERROR',
    title=Title('Rate of NOERROR answers'),
    unit=metrics.Unit(metrics.DecimalNotation("1/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.GREEN,
)

metric_unbound_answers_FORMERR = metrics.Metric(
    name='unbound_answers_FORMERR',
    title=Title('Rate of FORMERR answers'),
    unit=metrics.Unit(metrics.DecimalNotation("1/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.DARK_YELLOW,
)

metric_unbound_answers_SERVFAIL = metrics.Metric(
    name='unbound_answers_SERVFAIL',
    title=Title('Rate of SERVFAIL answers'),
    unit=metrics.Unit(metrics.DecimalNotation("1/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.DARK_PURPLE,
)

metric_unbound_answers_NXDOMAIN = metrics.Metric(
    name='unbound_answers_NXDOMAIN',
    title=Title('Rate of NXDOMAIN answers'),
    unit=metrics.Unit(metrics.DecimalNotation("1/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.GRAY,
)

metric_unbound_answers_NOTIMPL = metrics.Metric(
    name='unbound_answers_NOTIMPL',
    title=Title('Rate of NOTIMPL answers'),
    unit=metrics.Unit(metrics.DecimalNotation("1/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.DARK_BLUE,
)

metric_unbound_answers_REFUSED = metrics.Metric(
    name='unbound_answers_REFUSED',
    title=Title('Rate of REFUSED answers'),
    unit=metrics.Unit(metrics.DecimalNotation("1/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.RED,
)

metric_unbound_answers_nodata = metrics.Metric(
    name='unbound_answers_nodata',
    title=Title('Rate of answers without data'),
    unit=metrics.Unit(metrics.DecimalNotation("1/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.DARK_BROWN,
)

graph_unbound_answers = graphs.Graph(
    name='unbound_answers',
    title=Title('Rate of answers'),
    simple_lines=[
        f'unbound_answers_{answer}'
        for answer in ('NOERROR', 'FORMERR', 'SERVFAIL', 'NXDOMAIN', 'NOTIMPL', 'REFUSED', 'nodata')
    ],
)

metric_cache_hit_rate = metrics.Metric(
    name='cache_hit_rate',
    title=Title('Cache hits per second'),
    unit=metrics.Unit(metrics.DecimalNotation("/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.GREEN,
)

metric_cache_misses_rate = metrics.Metric(
    name='cache_misses_rate',
    title=Title('Cache misses per second'),
    unit=metrics.Unit(metrics.DecimalNotation("/s"), metrics.StrictPrecision(2)),
    color=metrics.Color.RED,
)

graph_cache_hit_misses = graphs.Graph(
    name='cache_hit_misses',
    title=Title('Cache Hits and Misses'),
    compound_lines=[
        'cache_hit_rate',
        'cache_misses_rate',
    ],
)
