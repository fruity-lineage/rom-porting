"""Exercise bounded ELF extraction with synthetic images; no firmware changes."""
import hashlib
import importlib.util
import struct
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    'extract_trusty_apps', Path(__file__).with_name('extract-trusty-apps.py'))
EXTRACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXTRACT)


def elf(is64=True, endian='<', filesz=32, memsz=64):
    ident = b'\x7fELF' + bytes([2 if is64 else 1, 1 if endian == '<' else 2, 1]) + bytes(9)
    header_size = 64 if is64 else 52
    ph_size = 56 if is64 else 32
    payload_offset = header_size + ph_size
    header_fmt = endian + ('HHIQQQIHHHHHH' if is64 else 'HHIIIIIHHHHHH')
    header = struct.pack(header_fmt, 2, 183 if is64 else 40, 1, 0x1000,
                         header_size, 0, 0, header_size, ph_size, 1, 0, 0, 0)
    fields = (1, 5, payload_offset, 0x1000, 0, filesz, memsz, 0x1000) if is64 else (
        1, payload_offset, 0x1000, 0, filesz, memsz, 5, 0x1000)
    ph = struct.pack(endian + ('IIQQQQQQ' if is64 else 'IIIIIIII'), *fields)
    return ident + header + ph + b'x' * 32


class ExtractionTest(unittest.TestCase):
    def test_classes_and_endianness(self):
        for is64 in (False, True):
            for endian in ('<', '>'):
                with self.subTest(is64=is64, endian=endian):
                    data = elf(is64, endian)
                    result = EXTRACT.inspect(data, 0)
                    self.assertEqual(len(data), result['size'])
                    self.assertEqual(hashlib.sha256(data).hexdigest(), result['sha256'])
                    self.assertEqual(183 if is64 else 40, result['machine'])

    def test_embedded_image_offset_and_trailer(self):
        data = elf()
        result = EXTRACT.inspect(b'prefix' + data + b'trailer', 6)
        self.assertEqual(6, result['offset'])
        self.assertEqual(len(data), result['size'])
        self.assertEqual(hashlib.sha256(data).hexdigest(), result['sha256'])

    def test_all_truncated_prefixes_are_rejected(self):
        data = elf()
        for length in range(len(data)):
            self.assertIsNone(EXTRACT.inspect(data[:length], 0), length)

    def test_filesize_cannot_exceed_load_memory(self):
        self.assertIsNone(EXTRACT.inspect(elf(filesz=32, memsz=31), 0))

    def test_segment_cannot_extend_past_image(self):
        self.assertIsNone(EXTRACT.inspect(elf(filesz=33), 0))

    def test_program_table_cannot_extend_past_image(self):
        data = bytearray(elf())
        struct.pack_into('<Q', data, 32, len(data))
        self.assertIsNone(EXTRACT.inspect(data, 0))

    def test_requires_a_load_segment(self):
        data = bytearray(elf())
        struct.pack_into('<I', data, 64, 4)
        self.assertIsNone(EXTRACT.inspect(data, 0))

    def test_unsupported_architecture_is_rejected(self):
        data = bytearray(elf())
        struct.pack_into('<H', data, 18, 62)
        self.assertIsNone(EXTRACT.inspect(data, 0))


if __name__ == '__main__':
    unittest.main()
