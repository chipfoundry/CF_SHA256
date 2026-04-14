"""SHA256 interrupt sequence — exercises IRQ sources (valid, ready) and IM/IC."""

from seq_lib.sha256_base_seq import sha256_base_seq


ABC_BLOCK = 0x61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018


class sha256_interrupt_seq(sha256_base_seq):
    async def body(self):
        await self._init()

        await self._w("im_all", "IM", 0x3)

        await self._hash(ABC_BLOCK, mode=1, is_first=True)

        await self._r("ris_valid", "RIS")
        await self._r("mis_valid", "MIS")

        await self._w("ic_valid", "IC", 0x1)
        await self._r("ris_after_clr", "RIS")

        await self._w("ic_ready", "IC", 0x2)
        await self._r("ris_final", "RIS")

        await self._w("ic_all", "IC", 0x3)
        await self._r("ris_zero", "RIS")

        for bit in range(2):
            await self._w(f"im_bit{bit}", "IM", 1 << bit)
            await self._r(f"im_rd{bit}", "IM")

        await self._w("im_restore", "IM", 0x3)
