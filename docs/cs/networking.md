# Síť a přístup

Box provozuje **nginx na portu 80** před backendem FastAPI. Žádné HTTPS a žádná admin webová stránka —
vše je HTTP API. Na port 80 se dostaneš třemi způsoby.

## 1. Wi-Fi (běžný klient LAN)

Box se připojí k domácí Wi-Fi a dostane DHCP adresu. Takto se obvykle používá bezhlavě.

```
http://<ip>/...        hlavička Host vybírá službu, Bearer token autentizuje
```

Protože je to DHCP, adresa se může měnit; chceš-li ji pevnou, nastav na routeru rezervaci (podle Wi-Fi
MAC boxu).

## 2. USB-C gadget (do hostitelského počítače)

Zapojení boxu do USB-C portu počítače vystaví **RNDIS / USB-Ethernet gadget** (rozhraní `usb0`). Box
dostane pevnou malou podsíť (přesný `/30` se liší kus od kusu, např. `172.20.204.136/30` s
zařízením `.137` a hostitelem `.138`). Nižší latence než Wi-Fi, ale jen po dobu připojení a tuto cestu
používá i desktopová aplikace („PC Server“).

## 3. USB-C Ethernet adaptér (box do LAN kabelem) ✅

Zapoj **USB-C → Ethernet adaptér do _druhého_ USB-C portu** (toho, který *není* „to PC“ gadget port).
Box zvedne běžné `eth0` s **normální LAN DHCP adresou** a plné API je přes něj dostupné úplně stejně
jako přes Wi-Fi — jen po stabilní a rychlejší kabelové lince.

- 2,5GbE adaptér funguje.
- I takto jsou vystavené jen HTTP API (port 80) a SSH (3588) — interní porty jednotlivých modelů se na
  `eth0` **neotevřou**, takže adaptér přináší stabilitu a rychlost, ne „víc portů“.
- Dřívější komunitní tvrzení, že „adaptér bez prostředníka nic nedělá“, bylo chybné.

## Discovery

Každé rozhraní odpovídá na discovery endpoint:

```
http://<ip>:39218/device.json
```

Vrátí jméno zařízení, sériové číslo a **všechny aktuální adresy rozhraní** (`eth0`, `wlan0`, `usb0`)
plus IPv6 link-local. Spolehlivý způsob, jak zjistit aktuální adresy po změně DHCP. (Odpovídající UDP
discovery poslouchá na 39217.)

## Otevřené porty (pozorováno)

| Port | Služba |
|---|---|
| 80 | HTTP API (nginx → FastAPI; hlavička `Host` routuje na služby) |
| 3588 | SSH (jen klíč; viz [cli-and-ssh.md](cli-and-ssh.md)) |
| 39217 / 39218 | discovery (UDP / HTTP `device.json`) |

Běžně očekávané, ale **zavřené** z LAN: 22 (SSH je místo toho na 3588), 443, 11434 (Ollama se
servíruje na 80 přes Host hlavičku, ne na nativním portu) a interní porty služeb/modelů (např. 8880,
5555) — ty jsou v zařízení jen na loopbacku.

## Autentizace

Každý API požadavek nese:

```
Authorization: Bearer <TOKEN>
```

`<TOKEN>` je API klíč z aplikace TiinyOS → *Settings → API access* (uložen lokálně v konfiguraci
aplikace, klíč `account.authKey`). Ber ho jako přihlašovací údaj rovný rootu — viz
[cli-and-ssh.md](cli-and-ssh.md).
