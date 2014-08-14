height_map = {
    'STOP_CODE': 0,
    'POP_TOP' : -1,
    'ROT_TWO': 0,
    'ROT_THREE': 0,
    'DUP_TOP': 1,
    'ROT_FOUR': 0,

    'NOP': 0,
    'UNARY_POSITIVE': 0,
    'UNARY_NEGATIVE': 0,
    'UNARY_NOT': 0,
    'UNARY_CONVERT': 0,
    'UNARY_INVERT': 0,

    'BINARY_POWER': -1,
    'BINARY_MULTIPLY': -1,
    'BINARY_DIVIDE': -1,
    'BINARY_MODULO': -1,
    'BINARY_ADD': -1,
    'BINARY_SUBTRACT': -1,
    'BINARY_SUBSCR': -1,
    'BINARY_FLOOR_DIVIDE': -1,
    'BINARY_TRUE_DIVIDE': -1,
    'INPLACE_FLOOR_DIVIDE': -1,
    'INPLACE_TRUE_DIVIDE': -1,
    # 'SLICE+0':
    # 'SLICE+1':
    # 'SLICE+2':
    # 'SLICE+3':

    # 'STORE_SLICE+0':
    # 'STORE_SLICE+1':
    # 'STORE_SLICE+2':
    # 'STORE_SLICE+3':

    # 'DELETE_SLICE+0':
    # 'DELETE_SLICE+1':
    # 'DELETE_SLICE+2':
    # 'DELETE_SLICE+3':

    'STORE_MAP': -2,
    'INPLACE_ADD': -1,
    'INPLACE_SUBTRACT': -1,
    'INPLACE_MULTIPLY': -1,
    'INPLACE_DIVIDE': -1,
    'INPLACE_MODULO': -1,
    'STORE_SUBSCR': -3,
    'DELETE_SUBSCR': -2,
    'BINARY_LSHIFT': -1,
    'BINARY_RSHIFT': -1,
    'BINARY_AND': -1,
    'BINARY_XOR': -1,
    'BINARY_OR': -1,
    'INPLACE_POWER': -1,
    'GET_ITER': 0,

    'PRINT_EXPR': -1,
    'PRINT_ITEM': -1,
    'PRINT_NEWLINE': 0,
    'PRINT_ITEM_TO': -2,
    'PRINT_NEWLINE_TO': -1,
    'INPLACE_LSHIFT': -1,
    'INPLACE_RSHIFT': -1,
    'INPLACE_AND': -1,
    'INPLACE_XOR': -1,
    'INPLACE_OR': -1,
    'BREAK_LOOP': 0,
    'WITH_CLEANUP': 'bad', # cannot say, nondeterministic
    'LOAD_LOCALS': 1,
    'RETURN_VALUE': -1,
    'IMPORT_STAR': -1,
    'EXEC_STMT': -3,
    'YIELD_VALUE': -1,
    'POP_BLOCK': 0,
    'END_FINALLY': 'bad', # cannot say, nondeterministic
    'BUILD_CLASS': -3,
    'STORE_NAME': -1,
    'DELETE_NAME': 0,
    'UNPACK_SEQUENCE': 'bad', # argument - 1
    'FOR_ITER': 'bad', # either +1 during loop or -1 when loop is finished
    'LIST_APPEND': -1,
    'STORE_ATTR': -2,
    'DELETE_ATTR': -1,
    'STORE_GLOBAL': -1,
    'DELETE_GLOBAL': 0,
    'DUP_TOPX': 'bad', # +x
    'LOAD_CONST': +1,
    'LOAD_NAME': +1,
    'BUILD_TUPLE': 'bad', # argument -1
    'BUILD_LIST': 'bad', # argument -1
    'BUILD_SET': 'bad', # argument -1
    'BUILD_MAP': +1,
    'LOAD_ATTR': 0,
    'COMPARE_OP': -1,
    'IMPORT_NAME': -1,
    'IMPORT_FROM': +1,
    'JUMP_FORWARD': 0,
    'JUMP_IF_FALSE_OR_POP': -1,
    'JUMP_IF_TRUE_OR_POP': -1,
    'JUMP_ABSOLUTE': 0,
    'POP_JUMP_IF_FALSE': -1,
    'POP_JUMP_IF_TRUE': -1,

    'LOAD_GLOBAL': +1,

    'CONTINUE_LOOP': 0,
    'SETUP_LOOP': 0,
    'SETUP_EXCEPT': 0,
    'SETUP_FINALLY': 0,

    'LOAD_FAST': +1,
    'STORE_FAST': -1,
    'DELETE_FAST': 0,

    'RAISE_VARARGS': 'bad', #varargs!
    'CALL_FUNCTION': 'bad', # -(argument)
    'MAKE_FUNCTION': 'bad', # argument + 1
    # 'BUILD_SLICE':
    # 'MAKE_CLOSURE':
    # 'LOAD_CLOSURE':
    # 'LOAD_DEREF':
    # 'STORE_DEREF':

    # 'CALL_FUNCTION_VAR':
    # 'CALL_FUNCTION_KW':
    # 'CALL_FUNCTION_VAR_KW':

    # 'SETUP_WITH':

    # 'EXTENDED_ARG':
    # 'SET_ADD':
    # 'MAP_ADD':
    }
