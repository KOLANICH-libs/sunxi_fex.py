sunxi_fex.py
============
~~[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/sunxi_fex.py/workflows/CI/master/sunxi_fex-0.CI-py3-none-any.whl)~~
~~[![GitHub Actions](https://github.com/KOLANICH-libs/sunxi_fex.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/sunxi_fex.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/sunxi_fex.py.svg)](https://libraries.io/github/KOLANICH-libs/sunxi_fex.py)
[<img alt="GPL-3.0-or-later" src="https://www.gnu.org/graphics/gplv3-or-later.svg" width="101"/>](./COPYING.md)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

A library for parsing [sunxi FEX format](https://linux-sunxi.org/Fex_Guide). Implemented via Kaitai Struct spec.
And a CLI tool for reserializing the contents of fex files in a human-readable and human-editable format.

License
=======

Unlike my other libs, this one [is licensed](./COPYING.md) under GNU GPL v3 <img alt="GPL-3.0-or-later" src="https://www.gnu.org/graphics/gplv3-or-later.svg" width="101"/> or any later version. **This is only to satisfy https://github.com/linux-sunxi/sunxi-tools [GPL-2.0-or-later license ![license badge](https://img.shields.io/github/license/linux-sunxi/sunxi-tools)](https://github.com/linux-sunxi/sunxi-tools/blob/master/LICENSE.md)**, because the knowledge required to specify this format was reverse-engineered from source code (see doc-ref of the Kaitai Struct spec) of that free and open source tool. Also from that tool some principles of conversion back to `fex` were taken, namely the idea that `0xFFFFFFFF` must be `default` and the principle of generating names for ports.

I am OK with relicensing my original contributions that are within this repo under [`Unlicense`](https://unlicense.org/), but I am not sure that the authors of [sunxi-tools](https://github.com/linux-sunxi/sunxi-tools) ([Alejandro Mery aka @amery](https://github.com/amery) and [@n1tehawk](https://github.com/n1tehawk)) are OK. They have chosen GPL, and the purpose of GPL is to be as viral as possible.
