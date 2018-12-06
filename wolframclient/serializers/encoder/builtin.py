# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import math

from wolframclient.serializers.utils import safe_len
from wolframclient.utils import six
from wolframclient.utils.encoding import force_bytes, force_text
from wolframclient.utils.functional import identity, force_tuple
from wolframclient.serializers.encoder import wolfram_encoder
if six.PY2:
    #in py2 if you construct use dict(a=2) then "a" is binary
    #since using bytes as keys is a legit operation we are only fixing py2 here

    def safe_key(key):
        if isinstance(key, six.binary_type):
            return force_text(key)
        return key
else:
    safe_key = identity



@wolfram_encoder.register(bool, six.none_type)
def encode_none(serializer, o):
    return serializer.serialize_symbol(force_bytes(o))

@wolfram_encoder.register(*set([bytearray, six.binary_type, *six.buffer_types]))
def encode_bytes(serializer, o):
    return serializer.serialize_bytes(o)

@wolfram_encoder.register(six.text_type)
def encode_text(serializer, o):
    return serializer.serialize_string(o)

@wolfram_encoder.register(dict)
def encode_dict(serializer, o):
    return serializer.serialize_mapping(
        ((serializer.encode(safe_key(key)), serializer.encode(value))
            for key, value in o.items()),
        length=safe_len(o))

@wolfram_encoder.register(*six.integer_types)
def encode_int(serializer, o):
    return serializer.serialize_int(o)

@wolfram_encoder.register(float)
def encode_float(serializer, o):

    if math.isinf(o):
        return serializer.serialize_function(
            serializer.serialize_symbol(b"DirectedInfinity"),
            (serializer.serialize_int(o < 0 and -1 or 1), ))

    if math.isnan(o):
        return serializer.serialize_symbol(b"Indeterminate")

    return serializer.serialize_float(o)

@wolfram_encoder.register(complex)
def encode_complex(serializer, o):
    return serializer.serialize_complex(o)

@wolfram_encoder.register(*six.iterable_types)
def encode_iter(serializer, o):
    return serializer.serialize_iterable((serializer.encode(value) for value in o),
                                    length=safe_len(o))
