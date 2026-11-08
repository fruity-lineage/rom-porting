#!/usr/bin/env python3
"""Inventory/extract bounded ELF payloads from Trusty images without changing them."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct


def inspect(data, base):
    ident = data[base:base + 16]
    if len(ident) < 16 or ident[4] not in (1, 2) or ident[5] not in (1, 2) or ident[6] != 1:
        return None
    is64 = ident[4] == 2
    endian = '<' if ident[5] == 1 else '>'
    fmt = endian + ('HHIQQQIHHHHHH' if is64 else 'HHIIIIIHHHHHH')
    header_size = 16 + struct.calcsize(fmt)
    remaining = len(data) - base
    if remaining < header_size:
        return None
    kind, machine, version, entry, phoff, shoff, flags, ehsize, phentsize, phnum, shentsize, shnum, shstrndx = struct.unpack_from(fmt, data, base + 16)
    if kind not in (2, 3) or machine not in (40, 183) or version != 1 or ehsize != header_size:
        return None
    phfmt = endian + ('IIQQQQQQ' if is64 else 'IIIIIIII')
    shfmt = endian + ('IIQQQQIIQQ' if is64 else 'IIIIIIIIII')
    if not 0 < phnum <= 1024 or phentsize != struct.calcsize(phfmt) or phoff + phnum * phentsize > remaining:
        return None
    if shnum > 1024 or (shnum and (shentsize != struct.calcsize(shfmt) or shoff + shnum * shentsize > remaining)):
        return None
    size = max(header_size, phoff + phnum * phentsize, shoff + shnum * shentsize if shnum else 0)
    loads = []
    for i in range(phnum):
        ph = struct.unpack_from(phfmt, data, base + phoff + i * phentsize)
        if is64:
            ptype, pflags, off, va, pa, filesz, memsz, align = ph
        else:
            ptype, off, va, pa, filesz, memsz, pflags, align = ph
        if off + filesz > remaining or (ptype == 1 and filesz > memsz):
            return None
        size = max(size, off + filesz)
        if ptype == 1:
            loads.append({'file_offset':off, 'vaddr':va, 'filesz':filesz, 'memsz':memsz, 'flags':pflags})
    if not loads:
        return None
    for i in range(shnum):
        sh = struct.unpack_from(shfmt, data, base + shoff + i * shentsize)
        if sh[1] != 8:  # SHT_NOBITS has no image bytes.
            if sh[4] + sh[5] > remaining:
                return None
            size = max(size, sh[4] + sh[5])
    payload = data[base:base + size]
    # Service names identify investigation leads, not runtime capability.
    hints = [{'file_offset':m.start(), 'text':m.group().decode()} for m in
             re.finditer(rb'com\.android\.trusty\.[a-zA-Z0-9._-]+', payload)]
    return {'offset':base, 'size':size, 'class':ident[4], 'machine':machine, 'entry':entry,
            'sha256':hashlib.sha256(payload).hexdigest(), 'loads':loads, 'identity_hints':hints}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--extract-dir', type=Path, help='New directory; existing destination is refused')
    args = parser.parse_args()
    data = args.image.read_bytes()
    if args.extract_dir:
        args.extract_dir.mkdir(parents=True, exist_ok=False)
    report = {'image':str(args.image.resolve()), 'size':len(data), 'sha256':hashlib.sha256(data).hexdigest(),
              'payloads':[], 'rejected_magic_offsets':[]}
    start = 0
    while True:
        start = data.find(b'\x7fELF', start)
        if start < 0:
            break
        payload = inspect(data, start)
        if payload:
            if args.extract_dir:
                path = args.extract_dir / f'elf-{start:08x}.elf'
                path.write_bytes(data[start:start + payload['size']])
                payload['extracted_path'] = str(path.resolve())
            report['payloads'].append(payload)
            hints = [h['text'] for h in payload['identity_hints']]
            print(f"0x{start:x} {payload['size']} bytes EM_{payload['machine']} {', '.join(hints[:3])}")
        else:
            report['rejected_magic_offsets'].append(start)
        start += 4
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(f"Validated {len(report['payloads'])} ELF payloads; report: {args.report}")


if __name__ == '__main__':
    main()
