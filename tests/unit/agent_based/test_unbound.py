#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Checks for the Unbound DNS Server status-
#
# Copyright (C) 2025 Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pytest  # type: ignore[import]
from cmk.agent_based.v2 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import unbound


EXAMPLE_STRING_TABLE = [
    ['thread0.num.queries', '205'],
    ['thread0.num.queries_ip_ratelimited', '0'],
    ['thread0.num.queries_cookie_valid', '0'],
    ['thread0.num.queries_cookie_client', '0'],
    ['thread0.num.queries_cookie_invalid', '0'],
    ['thread0.num.cachehits', '171'],
    ['thread0.num.cachemiss', '34'],
    ['thread0.num.prefetch', '0'],
    ['thread0.num.queries_timed_out', '0'],
    ['thread0.query.queue_time_us.max', '0'],
    ['thread0.num.expired', '0'],
    ['thread0.num.recursivereplies', '34'],
    ['thread0.requestlist.avg', '0.294118'],
    ['thread0.requestlist.max', '2'],
    ['thread0.requestlist.overwritten', '0'],
    ['thread0.requestlist.exceeded', '0'],
    ['thread0.requestlist.current.all', '0'],
    ['thread0.requestlist.current.user', '0'],
    ['thread0.recursion.time.avg', '0.001525'],
    ['thread0.recursion.time.median', '0.001536'],
    ['thread0.tcpusage', '0'],
    ['total.num.queries', '205'],
    ['total.num.queries_ip_ratelimited', '0'],
    ['total.num.queries_cookie_valid', '0'],
    ['total.num.queries_cookie_client', '0'],
    ['total.num.queries_cookie_invalid', '0'],
    ['total.num.cachehits', '171'],
    ['total.num.cachemiss', '34'],
    ['total.num.prefetch', '0'],
    ['total.num.queries_timed_out', '0'],
    ['total.query.queue_time_us.max', '0'],
    ['total.num.expired', '0'],
    ['total.num.recursivereplies', '34'],
    ['total.requestlist.avg', '0.294118'],
    ['total.requestlist.max', '2'],
    ['total.requestlist.overwritten', '0'],
    ['total.requestlist.exceeded', '0'],
    ['total.requestlist.current.all', '0'],
    ['total.requestlist.current.user', '0'],
    ['total.recursion.time.avg', '0.001525'],
    ['total.recursion.time.median', '0.001536'],
    ['total.tcpusage', '0'],
    ['time.now', '1743744886.505331'],
    ['time.up', '1130.640860'],
    ['time.elapsed', '1130.640860'],
    ['mem.cache.rrset', '68548'],
    ['mem.cache.message', '68831'],
    ['mem.mod.iterator', '16748'],
    ['mem.mod.validator', '66384'],
    ['mem.mod.respip', '0'],
    ['mem.mod.subnet', '0'],
    ['mem.streamwait', '0'],
    ['mem.http.query_buffer', '0'],
    ['mem.http.response_buffer', '0'],
    ['histogram.000000.000000.to.000000.000001', '0'],
    ['histogram.000000.000001.to.000000.000002', '0'],
    ['histogram.000000.000002.to.000000.000004', '0'],
    ['histogram.000000.000004.to.000000.000008', '0'],
    ['histogram.000000.000008.to.000000.000016', '0'],
    ['histogram.000000.000016.to.000000.000032', '0'],
    ['histogram.000000.000032.to.000000.000064', '0'],
    ['histogram.000000.000064.to.000000.000128', '0'],
    ['histogram.000000.000128.to.000000.000256', '0'],
    ['histogram.000000.000256.to.000000.000512', '0'],
    ['histogram.000000.000512.to.000000.001024', '5'],
    ['histogram.000000.001024.to.000000.002048', '24'],
    ['histogram.000000.002048.to.000000.004096', '5'],
    ['histogram.000000.004096.to.000000.008192', '0'],
    ['histogram.000000.008192.to.000000.016384', '0'],
    ['histogram.000000.016384.to.000000.032768', '0'],
    ['histogram.000000.032768.to.000000.065536', '0'],
    ['histogram.000000.065536.to.000000.131072', '0'],
    ['histogram.000000.131072.to.000000.262144', '0'],
    ['histogram.000000.262144.to.000000.524288', '0'],
    ['histogram.000000.524288.to.000001.000000', '0'],
    ['histogram.000001.000000.to.000002.000000', '0'],
    ['histogram.000002.000000.to.000004.000000', '0'],
    ['histogram.000004.000000.to.000008.000000', '0'],
    ['histogram.000008.000000.to.000016.000000', '0'],
    ['histogram.000016.000000.to.000032.000000', '0'],
    ['histogram.000032.000000.to.000064.000000', '0'],
    ['histogram.000064.000000.to.000128.000000', '0'],
    ['histogram.000128.000000.to.000256.000000', '0'],
    ['histogram.000256.000000.to.000512.000000', '0'],
    ['histogram.000512.000000.to.001024.000000', '0'],
    ['histogram.001024.000000.to.002048.000000', '0'],
    ['histogram.002048.000000.to.004096.000000', '0'],
    ['histogram.004096.000000.to.008192.000000', '0'],
    ['histogram.008192.000000.to.016384.000000', '0'],
    ['histogram.016384.000000.to.032768.000000', '0'],
    ['histogram.032768.000000.to.065536.000000', '0'],
    ['histogram.065536.000000.to.131072.000000', '0'],
    ['histogram.131072.000000.to.262144.000000', '0'],
    ['histogram.262144.000000.to.524288.000000', '0'],
    ['num.query.type.A', '170'],
    ['num.query.type.AAAA', '21'],
    ['num.query.type.SRV', '14'],
    ['num.query.class.IN', '205'],
    ['num.query.opcode.QUERY', '205'],
    ['num.query.tcp', '0'],
    ['num.query.tcpout', '0'],
    ['num.query.udpout', '29'],
    ['num.query.tls', '0'],
    ['num.query.tls.resume', '0'],
    ['num.query.ipv6', '0'],
    ['num.query.https', '0'],
    ['num.query.flags.QR', '0'],
    ['num.query.flags.AA', '0'],
    ['num.query.flags.TC', '0'],
    ['num.query.flags.RD', '205'],
    ['num.query.flags.RA', '0'],
    ['num.query.flags.Z', '0'],
    ['num.query.flags.AD', '0'],
    ['num.query.flags.CD', '0'],
    ['num.query.edns.present', '0'],
    ['num.query.edns.DO', '0'],
    ['num.answer.rcode.NOERROR', '25'],
    ['num.answer.rcode.FORMERR', '0'],
    ['num.answer.rcode.SERVFAIL', '0'],
    ['num.answer.rcode.NXDOMAIN', '93'],
    ['num.answer.rcode.NOTIMPL', '0'],
    ['num.answer.rcode.REFUSED', '87'],
    ['num.answer.rcode.nodata', '10'],
    ['num.query.ratelimited', '0'],
    ['num.answer.secure', '0'],
    ['num.answer.bogus', '0'],
    ['num.rrset.bogus', '0'],
    ['num.query.aggressive.NOERROR', '0'],
    ['num.query.aggressive.NXDOMAIN', '0'],
    ['unwanted.queries', '0'],
    ['unwanted.replies', '0'],
    ['msg.cache.count', '10'],
    ['rrset.cache.count', '8'],
    ['infra.cache.count', '1'],
    ['key.cache.count', '0'],
    ['msg.cache.max_collisions', '0'],
    ['rrset.cache.max_collisions', '0'],
    ['num.query.authzone.up', '0'],
    ['num.query.authzone.down', '0'],
    ['num.query.subnet', '0'],
    ['num.query.subnet_cache', '0'],
    ['num.query.cachedb', '0'],
]

EXAMPLE_SECTION = {
    'thread0.num.queries': 205,
    'thread0.num.queries_ip_ratelimited': 0,
    'thread0.num.queries_cookie_valid': 0,
    'thread0.num.queries_cookie_client': 0,
    'thread0.num.queries_cookie_invalid': 0,
    'thread0.num.cachehits': 171,
    'thread0.num.cachemiss': 34,
    'thread0.num.prefetch': 0,
    'thread0.num.queries_timed_out': 0,
    'thread0.query.queue_time_us.max': 0,
    'thread0.num.expired': 0,
    'thread0.num.recursivereplies': 34,
    'thread0.requestlist.avg': 0.294118,
    'thread0.requestlist.max': 2,
    'thread0.requestlist.overwritten': 0,
    'thread0.requestlist.exceeded': 0,
    'thread0.requestlist.current.all': 0,
    'thread0.requestlist.current.user': 0,
    'thread0.recursion.time.avg': 0.001525,
    'thread0.recursion.time.median': 0.001536,
    'thread0.tcpusage': 0,
    'total.num.queries': 205,
    'total.num.queries_ip_ratelimited': 0,
    'total.num.queries_cookie_valid': 0,
    'total.num.queries_cookie_client': 0,
    'total.num.queries_cookie_invalid': 0,
    'total.num.cachehits': 171,
    'total.num.cachemiss': 34,
    'total.num.prefetch': 0,
    'total.num.queries_timed_out': 0,
    'total.query.queue_time_us.max': 0,
    'total.num.expired': 0,
    'total.num.recursivereplies': 34,
    'total.requestlist.avg': 0.294118,
    'total.requestlist.max': 2,
    'total.requestlist.overwritten': 0,
    'total.requestlist.exceeded': 0,
    'total.requestlist.current.all': 0,
    'total.requestlist.current.user': 0,
    'total.recursion.time.avg': 0.001525,
    'total.recursion.time.median': 0.001536,
    'total.tcpusage': 0,
    'time.now': 1743744886.505331,
    'time.up': 1130.640860,
    'time.elapsed': 1130.640860,
    'mem.cache.rrset': 68548,
    'mem.cache.message': 68831,
    'mem.mod.iterator': 16748,
    'mem.mod.validator': 66384,
    'mem.mod.respip': 0,
    'mem.mod.subnet': 0,
    'mem.streamwait': 0,
    'mem.http.query_buffer': 0,
    'mem.http.response_buffer': 0,
    'histogram.000000.000000.to.000000.000001': 0,
    'histogram.000000.000001.to.000000.000002': 0,
    'histogram.000000.000002.to.000000.000004': 0,
    'histogram.000000.000004.to.000000.000008': 0,
    'histogram.000000.000008.to.000000.000016': 0,
    'histogram.000000.000016.to.000000.000032': 0,
    'histogram.000000.000032.to.000000.000064': 0,
    'histogram.000000.000064.to.000000.000128': 0,
    'histogram.000000.000128.to.000000.000256': 0,
    'histogram.000000.000256.to.000000.000512': 0,
    'histogram.000000.000512.to.000000.001024': 5,
    'histogram.000000.001024.to.000000.002048': 24,
    'histogram.000000.002048.to.000000.004096': 5,
    'histogram.000000.004096.to.000000.008192': 0,
    'histogram.000000.008192.to.000000.016384': 0,
    'histogram.000000.016384.to.000000.032768': 0,
    'histogram.000000.032768.to.000000.065536': 0,
    'histogram.000000.065536.to.000000.131072': 0,
    'histogram.000000.131072.to.000000.262144': 0,
    'histogram.000000.262144.to.000000.524288': 0,
    'histogram.000000.524288.to.000001.000000': 0,
    'histogram.000001.000000.to.000002.000000': 0,
    'histogram.000002.000000.to.000004.000000': 0,
    'histogram.000004.000000.to.000008.000000': 0,
    'histogram.000008.000000.to.000016.000000': 0,
    'histogram.000016.000000.to.000032.000000': 0,
    'histogram.000032.000000.to.000064.000000': 0,
    'histogram.000064.000000.to.000128.000000': 0,
    'histogram.000128.000000.to.000256.000000': 0,
    'histogram.000256.000000.to.000512.000000': 0,
    'histogram.000512.000000.to.001024.000000': 0,
    'histogram.001024.000000.to.002048.000000': 0,
    'histogram.002048.000000.to.004096.000000': 0,
    'histogram.004096.000000.to.008192.000000': 0,
    'histogram.008192.000000.to.016384.000000': 0,
    'histogram.016384.000000.to.032768.000000': 0,
    'histogram.032768.000000.to.065536.000000': 0,
    'histogram.065536.000000.to.131072.000000': 0,
    'histogram.131072.000000.to.262144.000000': 0,
    'histogram.262144.000000.to.524288.000000': 0,
    'num.query.type.A': 170,
    'num.query.type.AAAA': 21,
    'num.query.type.SRV': 14,
    'num.query.class.IN': 205,
    'num.query.opcode.QUERY': 205,
    'num.query.tcp': 0,
    'num.query.tcpout': 0,
    'num.query.udpout': 29,
    'num.query.tls': 0,
    'num.query.tls.resume': 0,
    'num.query.ipv6': 0,
    'num.query.https': 0,
    'num.query.flags.QR': 0,
    'num.query.flags.AA': 0,
    'num.query.flags.TC': 0,
    'num.query.flags.RD': 205,
    'num.query.flags.RA': 0,
    'num.query.flags.Z': 0,
    'num.query.flags.AD': 0,
    'num.query.flags.CD': 0,
    'num.query.edns.present': 0,
    'num.query.edns.DO': 0,
    'num.answer.rcode.NOERROR': 25,
    'num.answer.rcode.FORMERR': 0,
    'num.answer.rcode.SERVFAIL': 0,
    'num.answer.rcode.NXDOMAIN': 93,
    'num.answer.rcode.NOTIMPL': 0,
    'num.answer.rcode.REFUSED': 87,
    'num.answer.rcode.nodata': 10,
    'num.query.ratelimited': 0,
    'num.answer.secure': 0,
    'num.answer.bogus': 0,
    'num.rrset.bogus': 0,
    'num.query.aggressive.NOERROR': 0,
    'num.query.aggressive.NXDOMAIN': 0,
    'unwanted.queries': 0,
    'unwanted.replies': 0,
    'msg.cache.count': 10,
    'rrset.cache.count': 8,
    'infra.cache.count': 1,
    'key.cache.count': 0,
    'msg.cache.max_collisions': 0,
    'rrset.cache.max_collisions': 0,
    'num.query.authzone.up': 0,
    'num.query.authzone.down': 0,
    'num.query.subnet': 0,
    'num.query.subnet_cache': 0,
    'num.query.cachedb': 0,
}


def test_parse_unbound():
    assert unbound.parse_unbound(EXAMPLE_STRING_TABLE) == EXAMPLE_SECTION


@pytest.mark.parametrize('section, result', [
    (EXAMPLE_SECTION, [Service()]),
    ({}, []),
])
def test_discover_unbound_cache(section, result):
    assert list(unbound.discover_unbound_cache(section)) == result


@pytest.mark.parametrize('params, section, result', [
    (
        {},
        EXAMPLE_SECTION,
        [
            Result(state=State.OK, notice='Cache Misses: 34.00/s'),
            Metric('cache_misses_rate', 34.0),
            Result(state=State.OK, notice='Cache Hits: 171.00/s'),
            Metric('cache_hit_rate', 171.0),
            Result(state=State.OK, summary='Cache Hit Ratio: 83.41%'),
            Metric('cache_hit_ratio', 83.41463414634146),
        ]
    ),
    (
        {'cache_misses': ('fixed', (50, 60)), 'cache_hits': ('fixed', (75, 50))},
        EXAMPLE_SECTION,
        [
            Result(state=State.OK, notice='Cache Misses: 34.00/s'),
            Metric('cache_misses_rate', 34.0, levels=(50.0, 60.0)),
            Result(state=State.OK, notice='Cache Hits: 171.00/s'),
            Metric('cache_hit_rate', 171.0),
            Result(state=State.OK, summary='Cache Hit Ratio: 83.41%'),
            Metric('cache_hit_ratio', 83.41463414634146),
        ]
    ),
    (
        {'cache_misses': ('fixed', (20, 60)), 'cache_hits': ('fixed', (90, 50))},
        EXAMPLE_SECTION,
        [
            Result(state=State.WARN, notice='Cache Misses: 34.00/s (warn/crit at 20.00/s/60.00/s)'),
            Metric('cache_misses_rate', 34.0, levels=(20.0, 60.0)),
            Result(state=State.OK, notice='Cache Hits: 171.00/s'),
            Metric('cache_hit_rate', 171.0),
            Result(state=State.WARN, summary='Cache Hit Ratio: 83.41% (warn/crit below 90.00%/50.00%)'),
            Metric('cache_hit_ratio', 83.41463414634146),
        ]
    ),
    (
        {'cache_misses': ('fixed', (20, 30)), 'cache_hits': ('fixed', (90, 85))},
        EXAMPLE_SECTION,
        [
            Result(state=State.CRIT, notice='Cache Misses: 34.00/s (warn/crit at 20.00/s/30.00/s)'),
            Metric('cache_misses_rate', 34.0, levels=(20.0, 30.0)),
            Result(state=State.OK, notice='Cache Hits: 171.00/s'),
            Metric('cache_hit_rate', 171.0),
            Result(state=State.CRIT, summary='Cache Hit Ratio: 83.41% (warn/crit below 90.00%/85.00%)'),
            Metric('cache_hit_ratio', 83.41463414634146),
        ]
    ),
])
def test_check_ovpnlicense(monkeypatch, params, section, result):
    monkeypatch.setattr(unbound, 'get_value_store', lambda: {})
    monkeypatch.setattr(unbound, 'get_rate', lambda _v, _k, _t, v, raise_overflow=True: v)
    assert list(unbound.check_unbound_cache(params, section)) == result


@pytest.mark.parametrize('section, result', [
    (EXAMPLE_SECTION, [Service()]),
    ({}, []),
])
def test_discover_unbound_answers(section, result):
    assert list(unbound.discover_unbound_answers(section)) == result


@pytest.mark.parametrize('params, section, result', [
    (
        {},
        EXAMPLE_SECTION,
        [
            Result(state=State.OK, notice='NOERROR: 25.00/s'),
            Metric('unbound_answers_NOERROR', 25.0),
            Result(state=State.OK, notice='FORMERR: 0.00/s'),
            Metric('unbound_answers_FORMERR', 0.0),
            Result(state=State.OK, notice='SERVFAIL: 0.00/s'),
            Metric('unbound_answers_SERVFAIL', 0.0),
            Result(state=State.OK, notice='NXDOMAIN: 93.00/s'),
            Metric('unbound_answers_NXDOMAIN', 93.0),
            Result(state=State.OK, notice='NOTIMPL: 0.00/s'),
            Metric('unbound_answers_NOTIMPL', 0.0),
            Result(state=State.OK, notice='REFUSED: 87.00/s'),
            Metric('unbound_answers_REFUSED', 87.0),
            Result(state=State.OK, notice='nodata: 10.00/s'),
            Metric('unbound_answers_nodata', 10.0),
        ]
    ),
    (
        {'levels_upper_NOERROR': ('fixed', (30, 50))},
        EXAMPLE_SECTION,
        [
            Result(state=State.OK, summary='NOERROR: 25.00/s'),
            Metric('unbound_answers_NOERROR', 25.0, levels=(30.0, 50.0)),
            Result(state=State.OK, notice='FORMERR: 0.00/s'),
            Metric('unbound_answers_FORMERR', 0.0),
            Result(state=State.OK, notice='SERVFAIL: 0.00/s'),
            Metric('unbound_answers_SERVFAIL', 0.0),
            Result(state=State.OK, notice='NXDOMAIN: 93.00/s'),
            Metric('unbound_answers_NXDOMAIN', 93.0),
            Result(state=State.OK, notice='NOTIMPL: 0.00/s'),
            Metric('unbound_answers_NOTIMPL', 0.0),
            Result(state=State.OK, notice='REFUSED: 87.00/s'),
            Metric('unbound_answers_REFUSED', 87.0),
            Result(state=State.OK, notice='nodata: 10.00/s'),
            Metric('unbound_answers_nodata', 10.0),
        ]
    ),
    (
        {'levels_upper_NOERROR': ('fixed', (15, 50))},
        EXAMPLE_SECTION,
        [
            Result(state=State.WARN, summary='NOERROR: 25.00/s (warn/crit at 15.00/s/50.00/s)'),
            Metric('unbound_answers_NOERROR', 25.0, levels=(15.0, 50.0)),
            Result(state=State.OK, notice='FORMERR: 0.00/s'),
            Metric('unbound_answers_FORMERR', 0.0),
            Result(state=State.OK, notice='SERVFAIL: 0.00/s'),
            Metric('unbound_answers_SERVFAIL', 0.0),
            Result(state=State.OK, notice='NXDOMAIN: 93.00/s'),
            Metric('unbound_answers_NXDOMAIN', 93.0),
            Result(state=State.OK, notice='NOTIMPL: 0.00/s'),
            Metric('unbound_answers_NOTIMPL', 0.0),
            Result(state=State.OK, notice='REFUSED: 87.00/s'),
            Metric('unbound_answers_REFUSED', 87.0),
            Result(state=State.OK, notice='nodata: 10.00/s'),
            Metric('unbound_answers_nodata', 10.0),
        ]
    ),
    (
        {'levels_upper_NOERROR': ('fixed', (15, 20))},
        EXAMPLE_SECTION,
        [
            Result(state=State.CRIT, summary='NOERROR: 25.00/s (warn/crit at 15.00/s/20.00/s)'),
            Metric('unbound_answers_NOERROR', 25.0, levels=(15.0, 20.0)),
            Result(state=State.OK, notice='FORMERR: 0.00/s'),
            Metric('unbound_answers_FORMERR', 0.0),
            Result(state=State.OK, notice='SERVFAIL: 0.00/s'),
            Metric('unbound_answers_SERVFAIL', 0.0),
            Result(state=State.OK, notice='NXDOMAIN: 93.00/s'),
            Metric('unbound_answers_NXDOMAIN', 93.0),
            Result(state=State.OK, notice='NOTIMPL: 0.00/s'),
            Metric('unbound_answers_NOTIMPL', 0.0),
            Result(state=State.OK, notice='REFUSED: 87.00/s'),
            Metric('unbound_answers_REFUSED', 87.0),
            Result(state=State.OK, notice='nodata: 10.00/s'),
            Metric('unbound_answers_nodata', 10.0),
        ]
    ),
])
def test_check_unbound_answers(monkeypatch, params, section, result):
    monkeypatch.setattr(unbound, 'get_value_store', lambda: {})
    monkeypatch.setattr(unbound, 'get_rate', lambda _v, _k, _t, v, raise_overflow=True: v)
    assert list(unbound.check_unbound_answers(params, section)) == result


@pytest.mark.parametrize('section, result', [
    (EXAMPLE_SECTION, [Service()]),
    ({}, []),
])
def test_discover_unbound_unwanted_replies(section, result):
    assert list(unbound.discover_unbound_unwanted_replies(section)) == result


@pytest.mark.parametrize('section, result', [
    (
        EXAMPLE_SECTION,
        [
            Result(state=State.OK, summary='Unwanted Replies: 0.00/s'),
            Metric('unbound_unwanted_replies', 0.0, levels=(10.0, 100.0)),
        ]
    ),
    (
        {**EXAMPLE_SECTION, 'unwanted.replies': 15},
        [
            Result(state=State.WARN, summary='Unwanted Replies: 15.00/s (warn/crit at 10.00/s/100.00/s)'),
            Metric('unbound_unwanted_replies', 15.0, levels=(10.0, 100.0)),
        ]
    ),
    (
        {**EXAMPLE_SECTION, 'unwanted.replies': 150},
        [
            Result(state=State.CRIT, summary='Unwanted Replies: 150.00/s (warn/crit at 10.00/s/100.00/s)'),
            Metric('unbound_unwanted_replies', 150.0, levels=(10.0, 100.0)),
        ]
    ),
])
def test_check_unbound_unwanted_replies(monkeypatch, section, result):
    monkeypatch.setattr(unbound, 'get_value_store', lambda: {})
    monkeypatch.setattr(unbound, 'get_rate', lambda _v, _k, _t, v, raise_overflow=True: v)
    assert list(unbound.check_unbound_unwanted_replies(section)) == result
