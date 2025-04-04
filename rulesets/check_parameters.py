#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    InputHint,
    SimpleLevels,
    LevelDirection,
    Percentage,
    LevelsType,
    Integer,
    migrate_to_float_simple_levels,
    migrate_to_lower_float_levels,
)
from cmk.rulesets.v1.rule_specs import Topic, CheckParameters, HostCondition


def _parameter_form_unbound_cache():
    return Dictionary(
        elements={
            'cache_misses': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Levels on cache misses per second'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=InputHint(value=(100, 200)),
                    migrate=migrate_to_float_simple_levels,
                ),
                required=False,
            ),
            'cache_hits': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Lower levels for hits in %'),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=InputHint(value=(75, 50)),
                    migrate=migrate_to_lower_float_levels,
                ),
                required=False,
            ),
        },
    )


rule_spec_unbound_cache = CheckParameters(
    name='unbound_cache',
    title=Title('Unbound Cache'),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_unbound_cache,
    condition=HostCondition(),
)


def _parameter_form_unbound_answers():
    return Dictionary(
        elements={
            f"levels_upper_{answer}": DictElement(
                parameter_form=SimpleLevels(
                    title=Title(f'Upper levels for {answer} answers'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(unit_symbol='q/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=InputHint(value=(100, 1000)),
                    migrate=migrate_to_float_simple_levels,
                ),
                required=False,
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
        },
    )


rule_spec_unbound_answers = CheckParameters(
    name='unbound_answers',
    title=Title('Unbound Answers'),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_unbound_answers,
    condition=HostCondition(),
)
