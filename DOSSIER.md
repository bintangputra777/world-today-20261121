# Dossier — make.fun bounty "Sum up 21 November's world news in one image"

## Bounty (verified 22 Nov 2026, ~07:55 WIB)

- Bounty: **Sum up 21 November's world news in one image** — https://make.fun/bounty/news-image-20261121
- Slug: `news-image-20261121` · Prize: **$100, 50 places paid** (1st $20, 2nd $12, 3rd $6, 4th–10th $2 each, 11th–50th $1.20 each), USDC on Solana, escrow funded 2026-11-21. (Note: this edition's prize is $100, down from $250 on the 19–20 Nov editions.)
- Deadline: **Monday 23 Nov 2026, 07:00 WIB** (2026-11-23T00:00:00Z).
- Judging: an AI judge that can see images compares entries two at a time; the image itself must show the day's news (the judge has no news feed).
- Same format as the accepted 19 and 20 Nov entries (world-today-20261119, world-today-20261120); this build reuses their verified render pipeline.

## The image — five stories (checked 22 Nov against OneTurn, Majik Morning Brief, AP/Reuters via TFI, Kilambi, all dated 21 Nov 2026)

1. **UKRAINE — Russian missile hits Zelenskyy's hometown.** A ballistic strike on Kryvyi Rih kills two (a boy of 7, a woman of 20) and wounds 60 in a double-tap attack.
2. **MEXICO — Mexico captures cartel boss "El Chapo Isidro".** FBI most-wanted Fausto Isidro Meza Flores seized in Guasave, Sinaloa, with US intelligence help; cartel gunmen retaliate.
3. **CLIMATE — COP31 climate talks run into overtime.** The Antalya summit overruns its Friday deadline with no deal yet; fossil fuels missing from the draft text.
4. **MARKETS — AI sell-off drags world markets down.** S&P 500 falls 3.7% and Nasdaq erases its 2026 gains; Nikkei drops 5.06%.
5. **GULF — Iran says it struck US bases in Bahrain.** Bahrain reports an Iranian attack set a civilian industrial site ablaze, no injuries; Tehran claims the strike.

Design: same newspaper front-page style as the 19/20 Nov entries — navy masthead "THE WORLD TODAY / SATURDAY · 21 NOVEMBER 2026", five numbered colour-tagged rows, footer citing major news outlets. Rendered in code with Python/PIL (`scripts/render.py`) — no AI image generator.

## Program

`main.ts` copies `assets/entry.png` to `/output/entry.png` — deterministic, no network. Verified locally: two runs byte-identical and equal to the source asset.
