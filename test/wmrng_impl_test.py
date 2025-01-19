import wmrng as wmrng_new
import wmrng_old


def test_wm_rng_impls():
    for seed in range(10000):
        rng_new = wmrng_new.WorldMapRNG(seed)
        rng_old = wmrng_old.WorldMapRNG(seed)
        for call in range(10000):
            v_new = rng_new.rand()
            v_old = rng_old.rand()
            assert v_new == v_old
    return True


if __name__ == '__main__':
    print("Beginning tests...")
    test_wm_rng_impls()
    print("All tests passed.")
