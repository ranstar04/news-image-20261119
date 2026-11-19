# 19 November 2026 — The World in One Day

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ranstar04/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ranstar04/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

An entry for [make.fun competition `news-image-20261119`](https://make.fun/bounty/news-image-20261119): a program that writes a 1024x1024 newspaper poster summing up the world news of Thursday 19 November 2026 to `/output/entry.png`.

## The image

Six stories, chosen for consequence and breadth across regions and fields, all of which happened, or were first reported, on 19 November 2026:

1. **Games · Out today** — GTA VI launches worldwide; Vice City opens after 13 years of waiting.
2. **Diplomacy · China** — Trump, Xi and Putin converge in China; trilateral talks set for Thursday in Shenzhen.
3. **Space · A first** — Voyager 1 reaches one light-day from Earth, nearly 50 years after launch.
4. **Business · Record IPO** — Anthropic raises $81.3 billion, the largest IPO ever, debuting above $1.4 trillion.
5. **Art · Record sale** — A Van Gogh portrait sells for $190.4 million after its Nazi-era dispute.
6. **Europe · War** — The EU proposes a €45 billion loan for Ukraine, repaid once Russia pays reparations.

Sources (as reported 19 November 2026): BBC, Al Jazeera, NYT, Reuters, FT.

## How it works

`main.py` (Python 3.13, standard library only) copies the poster `entry.png` — which sits beside it in this repository — to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). It runs with no network and is fully deterministic: every run writes the same bytes. The poster itself was drawn during the build session with Pillow by `draw_poster.py`; the grader never runs that script, so `main.py` needs no third-party packages.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## make.fun

Built for the [news-image-20261119 bounty on make.fun](https://make.fun/bounty/news-image-20261119) — join the next one with my referral link: https://make.fun/r/dn9c31df

## License

MIT — see `LICENSE`.
