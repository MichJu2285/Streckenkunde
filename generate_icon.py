import zlib, struct

S = 180

def in_rr(px, py, x0, y0, x1, y1, r):
    if px < x0 or px > x1 or py < y0 or py > y1:
        return False
    nx = max(x0 + r - px, 0, px - (x1 - r))
    ny = max(y0 + r - py, 0, py - (y1 - r))
    return nx * nx + ny * ny <= r * r

def col(px, py):
    t = max(0.0, min(1.0, py / (S - 1)))
    c = (round(250 + (208 - 250) * t), round(8 + (0 - 8) * t), round(36 + (16 - 36) * t))
    if in_rr(px, py, 32, 40, 148, 158, 36):
        c = (255, 255, 255)
        if in_rr(px, py, 48, 58, 132, 94, 14):
            wt = max(0.0, min(1.0, (py - 58) / 36))
            c = (round(51 + (15 - 51) * wt), round(65 + (23 - 65) * wt), round(85 + (42 - 85) * wt))
        elif in_rr(px, py, 40, 106, 140, 118, 6):
            c = (236, 0, 22)
        else:
            if (px - 60) ** 2 + (py - 132) ** 2 <= 49 or (px - 120) ** 2 + (py - 132) ** 2 <= 49:
                c = (30, 41, 59)
    return c

rows = bytearray()
for y in range(S):
    rows.append(0)
    for x in range(S):
        rs = gs = bs = 0
        for dx, dy in ((0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)):
            cc = col(x + dx, y + dy)
            rs += cc[0]; gs += cc[1]; bs += cc[2]
        rows += bytes((round(rs / 4), round(gs / 4), round(bs / 4), 255))

def chunk(t, d):
    return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)

png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", S, S, 8, 6, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
       + chunk(b"IEND", b""))

with open("icon.png", "wb") as f:
    f.write(png)
print("icon.png geschrieben:", len(png), "Bytes")