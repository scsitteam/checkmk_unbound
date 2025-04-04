#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright (C) 2022, Jan-Philipp Litza (PLUTEX) <jpl@plutex.de>.
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

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    graph_info,
)

metric_info['unbound_answers_NOERROR'] = {
    'title': _('Rate of NOERROR answers'),
    'unit': '1/s',
    'color': '31/a',
}

metric_info['unbound_answers_FORMERR'] = {
    'title': _('Rate of FORMERR answers'),
    'unit': '1/s',
    'color': '21/a',
}

metric_info['unbound_answers_SERVFAIL'] = {
    'title': _('Rate of SERVFAIL answers'),
    'unit': '1/s',
    'color': '11/a',
}

metric_info['unbound_answers_NXDOMAIN'] = {
    'title': _('Rate of NXDOMAIN answers'),
    'unit': '1/s',
    'color': '51/a',
}

metric_info['unbound_answers_NOTIMPL'] = {
    'title': _('Rate of NOTIMPL answers'),
    'unit': '1/s',
    'color': '41/a',
}

metric_info['unbound_answers_REFUSED'] = {
    'title': _('Rate of REFUSED answers'),
    'unit': '1/s',
    'color': '26/a',
}

metric_info['unbound_answers_nodata'] = {
    'title': _('Rate of answers without data'),
    'unit': '1/s',
    'color': '52/a',
}


graph_info['unbound_answers'] = {
    'title': _('Rate of answers'),
    'metrics': [
        (f'unbound_answers_{answer}', 'line')
        for answer in ('NOERROR', 'FORMERR', 'SERVFAIL', 'NXDOMAIN', 'NOTIMPL', 'REFUSED', 'nodata')
    ],
}


metric_info['cache_hit_rate'] = {
    'title': _('Cache hits per second'),
    'unit': '1/s',
    'color': '26/a',
}

graph_info['cache_hit_misses'] = {
    'title': _('Cache Hits and Misses'),
    'metrics': [('cache_hit_rate', 'line'), ('cache_misses_rate', 'line')],
}
