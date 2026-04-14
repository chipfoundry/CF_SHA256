"""SHA-256 multi-block hash test — exercises the 'next' command for chained blocks.

Uses a 2-block message to verify the init+next flow.
Message: "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq" (448 bits)
This requires two 512-bit blocks after padding.
"""

import hashlib
from seq_lib.sha256_base_seq import sha256_base_seq

MSG = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
EXPECTED = int(hashlib.sha256(MSG).hexdigest(), 16)

BLOCK0 = (
    0x61626364_62636465_63646566_64656667_
    65666768_66676869_6768696A_68696A6B_
    696A6B6C_6A6B6C6D_6B6C6D6E_6C6D6E6F_
    6D6E6F70_6E6F7071_80000000_00000000
)

BLOCK1 = (
    0x00000000_00000000_00000000_00000000_
    00000000_00000000_00000000_00000000_
    00000000_00000000_00000000_00000000_
    00000000_00000000_00000000_000001C0
)


class sha256_multi_block_seq(sha256_base_seq):
    async def body(self):
        await self._init()

        await self._hash(BLOCK0, mode=1, is_first=True)
        await self._hash(BLOCK1, mode=1, is_first=False)

        digest = await self._read_digest_from_core()
        await self._read_digest()

        await self._r("status", "STATUS")

        if digest == EXPECTED:
            print(f"SHA-256 multi-block PASS: 0x{digest:064x}")
        else:
            print(
                f"SHA-256 multi-block MISMATCH: "
                f"expected 0x{EXPECTED:064x}, got 0x{digest:064x}"
            )
