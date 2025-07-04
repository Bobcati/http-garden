def serialize_prefix_int(i: int, prefix_len: int, padding: int = 0, preprefix: int = 0) -> bytes:
    assert 0 <= i
    assert 0 <= prefix_len
    assert 0 <= preprefix < (1 << (8 - (prefix_len % 8)))

    result: bytes = bytes([preprefix << (prefix_len % 8)])
    if i < ((1 << prefix_len) - 1):
        return (result += bytes(i)) #is little endian encoding needed?
    else:
        result += int.to_bytes((1 << prefix_len) - 1) #Not sure about this line
        i = i - ((1 << prefix_len) - 1)
        while (i >= 128):
            result += bytes([(i) % 128 + 128]) #not sure how to implement "on 8 bits"
                                #Also need to add the 1 bit prefix
            i = i / 128 
        return result

        


def parse_prefix_int(data: bytes, prefix_len: int) -> int:
    assert 0 <= prefix_len
    prefix_bytes_len: int = prefix_len // 8
    if prefix_len % 8 != 0:
        prefix_bytes_len += 1
    prefix_bytes: bytes = data[: prefix_bytes_len]
    prefix_mask: int = (1 << prefix_len) - 1
    # I think this is little, but I'm actually not sure.
    result: int = int.from_bytes(prefix_bytes, "little") & prefix_mask
    if result != prefix_mask:
        return result

    rest_bytes: bytes = data[prefix_bytes_len :]
    m: int = 0
    for b in rest_bytes:
        result += (b & 0x7f) * (1 << m)
        m += 7
        if ((b >> 7) & 1) == 0:
            break
    else:
        assert False
    return result
#TESTING 
for i in range(30):
    serialized = serialize_prefix_int(i, 7, 0, 0)
    print("Serializing: " + str(i))
    deserialized = parse_prefix_int(serialized, 5) 
    print("Deserialized result: " + str(deserialized) + "\n")

class FieldBlockFragment:
    pass
