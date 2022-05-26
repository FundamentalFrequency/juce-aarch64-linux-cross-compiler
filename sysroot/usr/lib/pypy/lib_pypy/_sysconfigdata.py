import imp
import sys

build_time_vars = {
    "SO": [s[0] for s in imp.get_suffixes() if s[2] == imp.C_EXTENSION][0]
}
if hasattr(sys, '_multiarch'):
    build_time_vars.update({
        'MULTIARCH': sys._multiarch,
    })
