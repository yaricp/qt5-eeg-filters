
def str2tuple(value):
    return tuple(float(i) for i in value.split(","))


def str2float(value):
    return float(value) if value else 0.0


def str2int(value):
    return int(value) if value else 0


typing_value = {
    "tuple": str2tuple,
    "float": str2float,
    "int": str2int
}
