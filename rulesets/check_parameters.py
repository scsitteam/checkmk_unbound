#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import Dictionary, Float, Percentage, Tuple, Alternative


def _parameter_valuespec_unbound_cache():
    return Dictionary(
        title=_("Unbound: Cache"),
        elements=[
            (
                "cache_misses",
                Tuple(
                    title="Levels on cache misses per second",
                    elements=[
                        Float(
                            title="warn",
                        ),
                        Float(
                            title="crit",
                        ),
                    ],
                ),
            ),
            (
                "cache_hits",
                Tuple(
                    title="Lower levels for hits in %",
                    elements=[
                        Percentage(
                            title="warn",
                        ),
                        Percentage(
                            title="crit",
                        ),
                    ],
                ),
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="unbound_cache",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unbound_cache,
        title=lambda: _("Unbound Cache"),
    )
)


def _parameter_valuespec_unbound_answers():
    return Dictionary(
        elements=[
            (
                f"levels_upper_{answer}",
                Alternative(
                    title=f'Upper levels for {answer} answers',
                    show_alternative_title=True,
                    elements=[
                        Tuple(
                            elements=[
                                Float(title=_("Warning at"), unit=_("qps")),
                                Float(title=_("Critical at"), unit=_("qps")),
                            ],
                            title=f'Upper levels for rate of {answer} answers',
                        ),
                        Tuple(
                            elements=[
                                Percentage(title=_("Warning at")),
                                Percentage(title=_("Critical at")),
                                FixedValue(value="%", totext=""),
                            ],
                            title=f'Upper levels for ratio of {answer} answers',
                        ),
                    ]
                )
            )
            for answer in (
                'NOERROR',
                'FORMERR',
                'SERVFAIL',
                'NXDOMAIN',
                'NOTIMPL',
                'REFUSED',
                'nodata',
            )
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="unbound_answers",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unbound_answers,
        title=lambda: _("Unbound Answers"),
    )
)
