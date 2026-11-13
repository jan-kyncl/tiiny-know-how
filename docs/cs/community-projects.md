# Související komunitní projekty a credits

Tyhle poznámky stojí na ramenou širší Tiiny komunity. Repa níže jsou to, co citujeme nebo čím jsme se
inspirovali — díky jejich autorům. Názvy a odkazy jsou tak, jak jsou publikované na GitHubu; cokoli si
ověř, než to spustíš proti vlastnímu zařízení.

## API a reference
- [thezolon/tiiny-api-notes](https://github.com/thezolon/tiiny-api-notes) — nejkompletnější komunitní
  reference API; také zdokumentoval funkční USB-C Ethernet adaptér ve druhém portu.
- [US4LKW/tiiny-ai-model-atlas](https://github.com/US4LKW/tiiny-ai-model-atlas) — katalog modelů s
  filtrem podle jazyka.
- [CooperativePenguinToby/tiiny-web](https://github.com/CooperativePenguinToby/tiiny-web) — open-source
  webový klient; zdroj řady `/api/services` a konektorových endpointů.

## Přístup a vnitřek
- [mjpcomp/tiiny-owner-ssh](https://github.com/mjpcomp/tiiny-owner-ssh) — přidá vlastnický SSH klíč
  (SSH je na portu 3588). Viz [cli-and-ssh.md](cli-and-ssh.md) a jeho bezpečnostní poznámka.
- [maci0/tiinyos-linux](https://github.com/maci0/tiinyos-linux) — poznámky k provozu TiinyOS na Linuxu.
- [webdevtodayjason/tiiny-unlock](https://github.com/webdevtodayjason/tiiny-unlock) — odemknutí `/data`
  po restartu jediným API voláním, když box vrací 502.
- [teaguesterling/TTt](https://github.com/teaguesterling/TTt) — pomocník `ttt` (`ttt doctor` aj.).

## Modely a inference
- [SJTU-IPADS/PowerInfer](https://github.com/SJTU-IPADS/PowerInfer) — inferenční engine, na kterém box
  staví (Tiiny dodává fork).
- [trentsuzuki/tiiny-custom-models](https://github.com/trentsuzuki/tiiny-custom-models) — spuštění
  vlastních GGUF modelů přes `llama.cpp` v kontejneru.
- [Titanium-Devops/tiiny-bench](https://github.com/Titanium-Devops/tiiny-bench) — benchmarking.
- [webdevtodayjason/turnstile](https://github.com/webdevtodayjason/turnstile) — fronta požadavků (box
  dělá jednu inferenci naráz; souběžně → chyba `150004`).

## Ovládací panely a integrace
- [0xStian/tiiny-control-panel](https://github.com/0xStian/tiiny-control-panel) — webový ovládací panel.
- [TheS1ngularity/TiinyControlPanel-HA](https://github.com/TheS1ngularity/TiinyControlPanel-HA) —
  add-on do Home Assistanta.
- [thezolon/tiiny-studio](https://github.com/thezolon/tiiny-studio) — studio UI.

---

> Uvedeno pro referenci a jako poděkování, ne jako doporučení. U minimálně jednoho komunitního repa byl
> pozorován omylem commitnutý API klíč — nikdy nepoužívej token, který najdeš v cizím repu, a necommituj
> vlastní.
