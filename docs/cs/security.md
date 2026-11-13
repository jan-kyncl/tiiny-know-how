# Bezpečnost — pozorování a otevřené obavy

> **Přečti si nejdřív tohle.** Tahle stránka shromažďuje **bezpečnostní obavy** majitele boxu, napsané
> jako **možné, spekulativní závěry** z běžného používání a z veřejných komunitních projektů — **ne**
> bezpečnostní audit, **ne** potvrzené zranitelnosti a **ne** zodpovědně nahlášené nálezy. Něco z toho
> může být chybné, zastaralé nebo založené na nepochopení, jak zařízení funguje. Nic zde není obvinění
> vůči Tiiny AI. Ber každou „obavu“ níže jako hypotézu k ověření, ne jako fakt. Ověřeno proti firmwaru
> 0.1.39.

Vzor níže je záměrný: **Pozorování** = něco reálně viděného na zařízení nebo ve veřejném kódu;
**Spekulativní obava** = starost, kterou to *může* znamenat a která nebyla potvrzena.

## 1. Token zařízení vypadá jako ekvivalent rootu

- **Pozorování.** Komunitní nástroj (`mjpcomp/tiiny-owner-ssh`) používá dokumentované services/connector
  API k vytvoření dočasného Docker kontejneru, který připojí hostitelský filesystem (`/:/host`) jako
  root. Vytvoření toho kontejneru vyžaduje jen běžný **API token** zařízení.
- **Spekulativní obava.** Pokud je ten primitiv obecně dostupný, pak **držení API tokenu může být
  ekvivalentní rootu na boxu** — bez ohledu na to, že „neexistuje shell“. Uniklý token by pak nebyl jen
  problém zneužití API, ale problém úplné kompromitace zařízení. Viz [cli-and-ssh.md](cli-and-ssh.md).
- **Pokud je to pravda, mitigace.** Ber token jako rootovské heslo: nikdy v repech/lozích/sdílených
  konfiguracích, při úniku rotovat a box držet mimo nedůvěryhodné sítě.

## 2. LAN služby možná bez autentizace

- **Pozorování.** Podle komunitní analýzy (`tiiny-web`) a kontrol na zařízení se nainstalované aplikace
  servírují na LAN přes port 80 na `<app>.agent.tiiny.local` bez zjevné autentizace před nimi.
- **Spekulativní obava.** Kdokoli, kdo na box dosáhne v LAN, **by možná mohl** ty aplikace používat — a
  podle aplikace i data či akce, které vystavují — bez přihlašovacích údajů.
- **Pokud je to pravda, mitigace.** Dej box do izolované VLAN/segmentu; zafirewalluj ho od guest a IoT
  sítí; neportforwarduj ho.

## 3. Discovery bez autentizace

- **Pozorování.** `http://<ip>:39218/device.json` vrací jméno zařízení, **sériové číslo** a všechny
  adresy rozhraní bez autentizace.
- **Spekulativní obava.** Na sdílené síti to prozrazuje identifikační/inventární informace a dělá box
  triviálně dohledatelným a otiskovatelným. Nízká závažnost, ale dobré vědět.

## 4. Závislost na cloudu a „phone-home“

- **Pozorování.** Aktivace, model store a OS (OTA) updaty jsou **koordinované s Tiiny cloudem**;
  desktopová aplikace komunikuje se službami výrobce.
- **Spekulativní obava.** Zařízení prodávané jako „soukromé/offline“ přesto **zřejmě závisí na cloudu
  výrobce** při nastavení, stahování modelů a updatech, což implikuje nějakou telemetrii/konektivitu a
  závislost důvěry i dostupnosti na výrobci. *Inference* běží lokálně; *životní cyklus* nemusí být plně
  offline. Co přesně se odesílá, zde nebylo zkoumáno.
- **Pokud ti na tom záleží.** Sleduj si odchozí provoz boxu sám (např. na routeru), než uvěříš tvrzení
  „plně offline“, a zvaž síťové omezení egressu.

## 5. Šifrované úložiště, ale automaticky odemykané při startu

- **Pozorování.** `/data` je šifrovaný LUKS, ale odemyká se automaticky při startu (bez dotazu na heslo
  majitele).
- **Spekulativní obava.** To chrání **ukradený disk / vypnuté zařízení**, ale pravděpodobně **ne běžící
  nebo nabootovaný box**, protože odemykací klíč musí být zařízení dostupný. Kde ten klíč je a jak je
  chráněný, zde nebylo zkoumáno.

## 6. Uzavřený firmware se těžko ověřuje

- **Pozorování.** Neexistuje oficiální shell a firmware je uzavřený; všechno řídíš přes API.
- **Spekulativní obava.** To dělá **nezávislé ověření** toho, co na zařízení běží, co odesílá a jestli
  daný update změnil bezpečnostně relevantní chování, obtížné. Jde o omezení transparentnosti, ne o
  konkrétní chybu.

## 7. Nestandardní SSH port není ochrana

- **Pozorování.** SSH poslouchá na portu **3588**, jen klíč.
- **Spekulativní obava.** Nestandardní port je **bezpečnost skrze nejasnost**; skutečná kontrola je
  autentizace jen klíčem. Nespoléhej na číslo portu.

## 8. Hygiena ekosystému

- **Pozorování.** U minimálně jednoho veřejného komunitního repa byl viděn **omylem commitnutý API
  token**.
- **Spekulativní obava.** Ve spojení s obavou č. 1 (token ≈ root) by nedbalé zacházení s tokeny v
  komunitě mohlo vystavit jednotlivé boxy. Nikdy nepoužívej token nalezený v cizím repu; nikdy
  necommituj vlastní.

---

## Shrnutí (spekulativní)

Pokud obavy č. 1 a č. 2 platí, je praktický bezpečnostní model zhruba: **kdokoli se síťovým dosahem na
box nebo s kopií jeho tokenu ho může plně ovládnout.** To je zvládnutelné na důvěryhodné, izolované
domácí síti a rizikové na sdílené/vystavené. **Nic z toho není potvrzené** — ověř si to na vlastním
zařízení, než na to budeš spoléhat, a reálné problémy hlas výrobci, místo abys tuhle stránku bral jako
hlášení.
