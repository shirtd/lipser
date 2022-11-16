import numpy as np

# def format_float(f):
#     if f.is_integer():
#         return int(f)
#     e = 0
#     while not f.is_integer():
#         f *= 10
#         e -= 1
#     return '%de%d' % (int(f), e)

def format_float(f):
    return np.format_float_scientific(f, trim='-') # if int(f) != f else str(int(f))

# def format_float(f, buf=10000):
#     if int(f) == f:
#         return str(int(f))
#     elif int(buf*f) == buf*f:
#         return str(int(buf*f))
#     return np.format_float_scientific(f, trim='-')
#     # return if int(buf*f) != buf*f else str(int(f))
