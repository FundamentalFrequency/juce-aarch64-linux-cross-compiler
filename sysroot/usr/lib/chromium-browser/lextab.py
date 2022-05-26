# lextab.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('ANY', 'ASYNC', 'ATTRIBUTE', 'BOOLEAN', 'BYTE', 'BYTESTRING', 'CALLBACK', 'CONST', 'CONSTRUCTOR', 'DELETER', 'DICTIONARY', 'DOMSTRING', 'DOUBLE', 'ELLIPSIS', 'ENUM', 'FALSE', 'FLOAT', 'FROZENARRAY', 'GETTER', 'INCLUDES', 'INFINITY', 'INHERIT', 'INTERFACE', 'ITERABLE', 'LONG', 'MAPLIKE', 'MIXIN', 'NAMESPACE', 'NAN', 'NULL', 'OBJECT', 'OBSERVABLEARRAY', 'OCTET', 'OPTIONAL', 'OR', 'PARTIAL', 'PROMISE', 'READONLY', 'RECORD', 'REQUIRED', 'SEQUENCE', 'SETLIKE', 'SETTER', 'SHORT', 'SPECIAL_COMMENT', 'STATIC', 'STRINGIFIER', 'TRUE', 'TYPEDEF', 'UNRESTRICTED', 'UNSIGNED', 'USVSTRING', 'VOID', 'float', 'identifier', 'integer', 'string'))
_lexreflags   = 64
_lexliterals  = '"*.(){}[],;:=+-/~|&^?<>'
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_ELLIPSIS>\\.\\.\\.)|(?P<t_float>-?(([0-9]+\\.[0-9]*|[0-9]*\\.[0-9]+)([Ee][+-]?[0-9]+)?|[0-9]+[Ee][+-]?[0-9]+))|(?P<t_integer>-?([1-9][0-9]*|0[Xx][0-9A-Fa-f]+|0[0-7]*))|(?P<t_LINE_END>\\n+)|(?P<t_string>"[^"]*")|(?P<t_SPECIAL_COMMENT>/\\*\\*(.|\\n)+?\\*/)|(?P<t_COMMENT>(/\\*(.|\\n)*?\\*/)|(//.*(\\n[ \\t]*//.*)*))|(?P<t_KEYWORD_OR_SYMBOL>[_-]?[A-Za-z][A-Za-z_0-9-]*)', [None, ('t_ELLIPSIS', 'ELLIPSIS'), ('t_float', 'float'), None, None, None, ('t_integer', 'integer'), None, ('t_LINE_END', 'LINE_END'), ('t_string', 'string'), ('t_SPECIAL_COMMENT', 'SPECIAL_COMMENT'), None, ('t_COMMENT', 'COMMENT'), None, None, None, None, ('t_KEYWORD_OR_SYMBOL', 'KEYWORD_OR_SYMBOL')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_ANY_error'}
_lexstateeoff = {}
