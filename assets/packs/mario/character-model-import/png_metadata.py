"""Remove volatile render text metadata without decoding/recompressing PNG pixels."""
import struct


def stable_png(path):
    source = path.read_bytes()
    assert source[:8] == b'\x89PNG\r\n\x1a\n'
    chunks, image_data = [], []
    offset = 8
    while offset < len(source):
        length = struct.unpack('>I', source[offset:offset + 4])[0]
        kind = source[offset + 4:offset + 8]
        chunk = source[offset:offset + 12 + length]
        assert len(chunk) == 12 + length
        if kind == b'IDAT':
            image_data.append(chunk)
        if kind not in (b'tEXt', b'zTXt', b'iTXt'):
            chunks.append(chunk)
        offset += 12 + length
    result = source[:8] + b''.join(chunks)
    assert all(chunk in result for chunk in image_data), 'PNG image data must be byte-identical'
    path.write_bytes(result)
