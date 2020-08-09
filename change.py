#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020  <@QCMTA1408289>
#
# Distributed under terms of the MIT license.
"""

"""
import pandas as pd

df = pd.read_excel("mainfile.xlsx")
df = df.sample(frac=1).reset_index(drop=True)
df.to_excel("for500CAD.xlsx")
