# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import datetime

def update_dispatch(dispatch):

    @dispatch.multi(datetime.datetime)
    def normalizer(self, o):
        return self.serialize_function(
            self.serialize_symbol(b"DateObject"), (
                self.serialize_iterable((
                    self.serialize_integer(o.year),
                    self.serialize_integer(o.month),
                    self.serialize_integer(o.day),
                    self.serialize_integer(o.hour),
                    self.serialize_integer(o.minute),
                    self.serialize_float(o.second + o.microsecond / 1000000.)
                )),
                self.serialize_string("Instant"),
                self.serialize_string("Gregorian"),
                self.serialize_tzinfo(o)
            )
        )

    @dispatch.multi(datetime.date)
    def normalizer(self, o):
        return self.serialize_function(
            self.serialize_symbol(b"DateObject"), (
                self.serialize_iterable((
                    self.serialize_integer(o.year),
                    self.serialize_integer(o.month),
                    self.serialize_integer(o.day),
                )),
            )
        )

    @dispatch.multi(datetime.time)
    def normalizer(self, o):
        return self.serialize_function(
            self.serialize_symbol(b"TimeObject"), (
                self.serialize_iterable((
                    self.serialize_integer(o.hour),
                    self.serialize_integer(o.minute),
                    self.serialize_float(o.second + o.microsecond / 1000000.)
                )),
                self.serialize_rule(
                    self.serialize_symbol(b"TimeZone"),
                    self.serialize_tzinfo(o)
                )
            )
        )