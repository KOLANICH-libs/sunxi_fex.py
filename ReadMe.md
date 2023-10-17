sunxi_fex.py
============
~~[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/sunxi_fex.py/workflows/CI/master/sunxi_fex-0.CI-py3-none-any.whl)~~
~~[![GitHub Actions](https://github.com/KOLANICH-libs/sunxi_fex.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/sunxi_fex.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/sunxi_fex.py.svg)](https://libraries.io/github/KOLANICH-libs/sunxi_fex.py)
[<img alt="GPL-3.0-or-later" src="https://www.gnu.org/graphics/gplv3-or-later.svg" width="101"/>](./COPYING.md)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

**We have moved to https://codeberg.org/KFmts/sunxi_fex.py (the namespace has changed to `KFmts`, which groups packages related to parsing or serialization), grab new versions there.**

Under the disguise of "better security" Micro$oft-owned GitHub has [discriminated users of 1FA passwords](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/) while having commercial interest in success and wide adoption of [FIDO 1FA specifications](https://fidoalliance.org/specifications/download/) and [Windows Hello implementation](https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422) which [it promotes as a replacement for passwords](https://github.blog/2023-07-12-introducing-passwordless-authentication-on-github-com/). It will result in dire consequencies and is competely inacceptable, [read why](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

If you don't want to participate in harming yourself, it is recommended to follow the lead and migrate somewhere away of GitHub and Micro$oft. Here is [the list of alternatives and rationales to do it](https://github.com/orgs/community/discussions/49869). If they delete the discussion, there are certain well-known places where you can get a copy of it. [Read why you should also leave GitHub](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

---

A library for parsing [sunxi FEX format](https://linux-sunxi.org/Fex_Guide). Implemented via Kaitai Struct spec.
And a CLI tool for reserializing the contents of fex files in a human-readable and human-editable format.

License
=======

Unlike my other libs, this one [is licensed](./COPYING.md) under GNU GPL v3 <img alt="GPL-3.0-or-later" src="https://www.gnu.org/graphics/gplv3-or-later.svg" width="101"/> or any later version. **This is only to satisfy https://github.com/linux-sunxi/sunxi-tools [GPL-2.0-or-later license ![license badge](https://img.shields.io/github/license/linux-sunxi/sunxi-tools)](https://github.com/linux-sunxi/sunxi-tools/blob/master/LICENSE.md)**, because the knowledge required to specify this format was reverse-engineered from source code (see doc-ref of the Kaitai Struct spec) of that free and open source tool. Also from that tool some principles of conversion back to `fex` were taken, namely the idea that `0xFFFFFFFF` must be `default` and the principle of generating names for ports.

I am OK with relicensing my original contributions that are within this repo under [`Unlicense`](https://unlicense.org/), but I am not sure that the authors of [sunxi-tools](https://github.com/linux-sunxi/sunxi-tools) ([Alejandro Mery aka @amery](https://github.com/amery) and [@n1tehawk](https://github.com/n1tehawk)) are OK. They have chosen GPL, and the purpose of GPL is to be as viral as possible.
