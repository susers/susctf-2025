#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include "gen_data.h"

// Symbols from objcopy -I binary
extern const unsigned char _binary_blob_bin_start[];
extern const unsigned char _binary_blob_bin_end[];

static inline uint64_t fnv1a_mix_u8(uint64_t h, uint8_t v) {
    h ^= v;
    return h * 1099511628211ULL;
}

static inline uint64_t xs64s_next(uint64_t x) {
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    return x * 2685821657736338717ULL;
}

int main(void) {
    const unsigned char *p = _binary_blob_bin_start;
    size_t n = (size_t)(_binary_blob_bin_end - _binary_blob_bin_start);

    if ((uint64_t)n != blob_expected_size) {
        fprintf(stderr, "Blob size mismatch: got %zu, expected %" PRIu64 "\n", n, blob_expected_size);
        return 1;
    }

    // Derive seed from selected positions
    uint64_t h = 1469598103934665603ULL;
    for (size_t i = 0; i < NUM_IDXS; i++) {
        uint32_t idx = idxs[i];
        if ((size_t)idx >= n) {
            fprintf(stderr, "Index out of range: %u\n", idx);
            return 1;
        }
        uint8_t b = p[idx];
        uint64_t t = idx;
        for (int k = 0; k < 8; k++) {
            h = fnv1a_mix_u8(h, (uint8_t)(t & 0xFF));
            t >>= 8;
        }
        h = fnv1a_mix_u8(h, b);
    }
    if (h == 0) h = 0x9E3779B97F4A7C15ULL;

    // Decrypt ciphertext
    unsigned char flag[CT_LEN + 1];
    uint64_t s = h;
    for (size_t i = 0; i < CT_LEN; i++) {
        s = xs64s_next(s);
        uint8_t ks = (uint8_t)(s >> 56);
        flag[i] = (unsigned char)(ct[i] ^ ks);
    }
    flag[CT_LEN] = '\0';

    puts((char*)flag);
    return 0;
}
