# OTA upgrade — terénní průvodce

Oficiální quick start líčí update jako jedno tlačítko. V praxi je OS (firmware) upgrade
**vícefázový proces koordinovaný s cloudem**, který se umí zaseknout na několika místech. Tahle
stránka je to, co quick start vynechává — na základě protažení boxu ze staršího firmwaru až na
**0.1.39**.

## Jak to doopravdy funguje

- OS updaty jsou velké **`.raucb` obrazy** (desítky minut na stažení a aplikaci), řízené
  **aplikací koordinovaně s Tiiny cloudem**. Pro OS update **neexistuje veřejné API ani CLI** a box
  **nemá shell** — řídíš to z desktopové aplikace.
- Stoupá po **krocích**, ne jedním skokem: např. `0.1.33 → 0.1.35 → … → 0.1.39`. Každý krok stáhne,
  aplikuje a restartuje; počítej s několika restarty.
- Po každém OS kroku si box často znovu stáhne **nové verze modelů**, což přidá další čas.

## Kde je stav (hostitel, cesty macOS)

| Co | Cesta |
|---|---|
| Stavový automat updatu | `~/Library/Application Support/tiiny-ai/update-state.json` |
| Logy desktop aplikace | `~/Library/Application Support/TiinyOS/logs` |
| Log requestů PC Serveru | `/etc/pcsvr/logs/requests.jsonl` |

`update-state.json` drží aktuální `phase` a `upgrade_process.os_download_progress`. Když se něco pokazí,
uvidíš tu hodnoty jako `paused`, `cancelInProgress` nebo `Cancellation failed`.

## Řízení OS updatu přes API PC Serveru

Dokud běží desktopová aplikace („PC Server“), je koordinátor OS upgradu dostupný na hostiteli na
`http://hardware-upgrade.api.tiiny` (routuje se přes PC Server, **ne** přes běžnou LAN IP):

```
GET  /api/upgrade/status
POST /api/upgrade/resume_prepare
POST /api/upgrade/pause_prepare
```

Pomocí nich lze prohlédnout a popostrčit běh, ve kterém se UI zamotalo.

## Poruchy, na které jsme reálně narazili (a jak je spravit)

**„PC Server package signature could not be verified“ (appka 1.0.3)**
Novější desktop aplikace tohle vyhodila a následně update/feedback volání failovala. Ruční `codesign -R`
přitom projde, takže to vypadá na bug aplikace. **Obejití:** downgrade desktop aplikace na ověřenou
verzi (u nás 0.9.6; instalační pkg leží na připojeném Tiiny volume), provést upgrade, pak se vrátit.
Varování o podpisu může na 1.0.3 kosmeticky přetrvávat, i když vše funguje.

**Služba `hardware-upgrade` visí (timeouty / 502)**
Upgrade služba na boxu se zasekla a vracela 502. **Fix:** restart boxu **tlačítkem napájení**.

**Zaseklý image pull („获取镜像 manifest…“)**
Box visí při stahování kontejnerového obrazu během přípravy. **Fix:** restart boxu tlačítkem. Pozor, OTA
se po pauze často **sama pozastaví** — znovu pošli `resume_prepare` nebo krok restartuj.

**Sdílení internetu rozbíjí detekci**
Pokud Mac sdílí internet přes USB bridge (`bridge100`), PC Server přestane box vidět
(`current_device_missing_from_pc_service_snapshot`) a update nemůže pokračovat. **Fix:** na tom rozhraní
vypnout sdílení internetu.

**Update zaseklý v `paused` / `cancelInProgress` / „Cancellation failed“**
Nejčistší reset: **Cmd+Q aplikace TiinyOS**, pak — se zavřenou aplikací — zazálohovat a **smazat
`update-state.json`** a začít znovu. OS update je nepovinný; klidně můžeš box nechat na firmwaru, na
kterém je.

## Praktické tipy

- Dej tomu čas a napájení: první boot po kroku je pomalý a 502 hned po restartu obvykle jen znamená, že
  vnitřní služba ještě nenaběhla — než na něco saháš, počkej.
- Po celou dobu nech box na **stejné Wi-Fi** a na vlastním napájení (ne jen přes USB).
- Když se vše usadí, model se nemusí **sám spustit** — spusť ho znovu přes aplikaci nebo
  `POST /api/v1/models/<id>/launch`.
