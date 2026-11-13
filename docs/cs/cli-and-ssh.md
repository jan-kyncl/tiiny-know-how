# CLI a SSH

## Oficiální CLI (`tiiny`)

Výrobce dodává oficiální CLI SDK (v době psaní v0.0.7, z dev.tiiny.ai). Je to obal nad stejným HTTP API
— shell na boxu **nedává**.

Instalace (příklad macOS):

```bash
curl -fsSL http://tiiny-cli.tiiny.cloud/install-darwin.sh | bash
```

Binárka v `~/.local/tiiny/bin/tiiny`, konfigurace v `~/.local/tiiny/config.json` (obsahuje
`account.authKey` — tvůj token).

Skupiny příkazů:

```
auth / login / logout / status      scan / connect / wifi / upgrade
ls / info / top / load / unload     run / bench / interrupt
import / download / rm              connector
backup / restore / restart / shutdown / tasks      vault
```

Typický postup: `tiiny scan` → `tiiny connect <ip>` → `tiiny login` → `tiiny ls` / `tiiny run`.

## SSH

**Oficiální shell neexistuje**, ale SSH server poslouchá na **portu 3588** (port 22 je zavřený),
**jen klíč** (bez hesla). Ve výchozím stavu nemáš žádný autorizovaný klíč, takže se nepřihlásíš.

### Přidání vlastního klíče

Komunitní projekt **`mjpcomp/tiiny-owner-ssh`** přidá vlastnický klíč. Jak to funguje (dobré vědět,
než to spustíš):

1. Přes connector API (`connector.api.tiiny` → `/v1/mcp/servers`) vytvoří dočasný MCP konektor, pak
   přes services API (`agent-services.api.tiiny` → `/api/services`) spustí **dočasný Docker kontejner**,
   který připojí hostitelský filesystem (`/:/host`) jako **root**.
2. Uvnitř kontejneru zapíše tři soubory a pošle sshd SIGHUP:
   - `/etc/ssh/owner_authorized_keys/` (adresář, `700`)
   - `/etc/ssh/owner_authorized_keys/root` (tvůj veřejný klíč, `600`)
   - `/etc/ssh/sshd_config.d/00-owner-access.conf`
     (`PermitRootLogin prohibit-password` + `AuthorizedKeysFile` ukazující na adresář výše)
3. Kontejner se po ~180 s sám odstraní. Nástroj také dělá baseline zálohu, verifikaci a umí
   auto-rollback.

Windows-only části repa jsou jen launcher a čtení tokenu; jádro je platformně nezávislý Python.

> **🔒 Bezpečnostní důsledek.** Výše uvedený mechanismus znamená, že **kdokoli s tokenem zařízení má
> fakticky root na boxu**, přes ten kontejnerový primitiv — nezávisle na SSH. Podle toho s tokenem
> zacházej: mimo repa, logy a sdílené konfigurace, a box zafirewalluj od nedůvěryhodných sítí.

### Praktický bloker (0.1.39)

Spuštění kontejneru `tiiny-owner-ssh` potřebuje na boxu **přítomný čistý `python3` Docker obraz**. Na
firmwaru 0.1.39 self-contained objevení obrazu (interní port 5555, `/api/web/compose/current`) vrací
prázdno a jediné předinstalované obrazy jsou n8n stack (node, ne python). Instalace služby, která
nacachuje python obraz (např. **Odysseus**, který balí SearXNG), jeden dodá; poté funguje
„kompatibilní cesta“, která službu posílá z hostitele přes `agent-services.api.tiiny`.
