# Související komunitní projekty

Další repa a reference, které pomohly tyto poznámky sestavit. Názvy jsou tak, jak jsou publikované na
GitHubu; cokoli si ověř, než to spustíš proti vlastnímu zařízení.

## API a reference
- **thezolon/tiiny-api-notes** — nejkompletnější komunitní reference API; také zdokumentoval funkční
  USB-C Ethernet adaptér ve druhém portu.
- **US4LKW/tiiny-ai-model-atlas** — katalog modelů s filtrem podle jazyka.
- **CooperativePenguinToby/tiiny-web** — open-source webový klient; zdroj řady `/api/services` a
  konektorových endpointů.

## Přístup a vnitřek
- **mjpcomp/tiiny-owner-ssh** — přidá vlastnický SSH klíč (SSH je na portu 3588). Viz
  [cli-and-ssh.md](cli-and-ssh.md) a jeho bezpečnostní poznámka.
- **maci0/tiinyos-linux** — poznámky k provozu TiinyOS na Linuxu.
- **webdevtodayjason/tiiny-unlock** — odemknutí `/data` po restartu jediným API voláním, když box vrací
  502.
- **teaguesterling/TTt** — pomocník `ttt` (`ttt doctor` aj.).

## Modely a inference
- **SJTU-IPADS / Tiiny-AI — PowerInfer** — inferenční engine boxu.
- **trentsuzuki/tiiny-custom-models** — spuštění vlastních GGUF modelů přes `llama.cpp` v kontejneru.
- **Titanium-Devops/tiiny-bench** — benchmarking.
- **webdevtodayjason/turnstile** — fronta požadavků (box dělá jednu inferenci naráz; souběžně → chyba
  `150004`).

## Ovládací panely a integrace
- **0xStian/tiiny-control-panel** a **TheS1ngularity/TiinyControlPanel-HA** — webový ovládací panel a
  add-on do Home Assistanta.
- **thezolon/tiiny-studio** — studio UI.

> Uvedeno jen pro referenci, ne jako doporučení. U minimálně jednoho komunitního repa byl pozorován
> omylem commitnutý API klíč — nikdy nepoužívej token, který najdeš v cizím repu, a necommituj vlastní.
