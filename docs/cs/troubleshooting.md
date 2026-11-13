# Řešení potíží

**nginx 502** — web server běží, ale vnitřní služba Tiiny ještě nenaběhla. Typické hned po zapnutí
(první boot je dlouhý) nebo během aktualizace. Počkat; případně spustit aplikaci TiinyOS, která
autorizuje backend.

**Agent store prázdný / `is_activated:false`** — nedokončená aktivace nebo probíhající aktualizace.
Dokončit přihlášení v aplikaci, nechat doběhnout update, restartovat aplikaci.

**0 modelů v `/v1/models`** — normální po vyp/zap; modely se donačtou, nebo některý spusť přes
`POST /api/v1/models/<id>/launch`.

**Model po každém zapnutí neběží** — box ne vždy sám znovu spustí poslední model. Po každém startu ho
spusť znovu (API nebo aplikace).

**Zaseklá OTA aktualizace** — OS updaty jsou velké `.raucb` obrazy řízené **aplikací koordinovaně s
Tiiny cloudem**; pro OS update neexistuje veřejné API ani CLI a box nemá shell. Zaseklý image pull
často vyřeší hardwarový restart (tlačítko napájení); OTA se po pauze sama často pozastaví. Aplikace
drží stav updatu lokálně (support adresář desktop aplikace, `update-state.json`).

**„PC Server package signature could not be verified“** — viděno na některých verzích desktop aplikace;
často neškodné. Obejít lze downgradem desktop aplikace.

**Sdílení internetu rozbíjí detekci** — sdílení internetu hostitele přes USB bridge může zabránit
desktopovému „PC Serveru“ v detekci boxu (`current_device_missing_from_pc_service_snapshot`). Na tom
rozhraní sdílení internetu vypni.

**Vypnutí z aplikace box nevypne** — může blokovat zaseklý proces. Alternativy:
`POST /api/v1/sys/shutdown/`, nebo podržet tlačítko napájení ~10 s.

**Nalezení boxu po změně DHCP** — dotázat `http://<ip>:39218/device.json`, nebo oskenovat podsíť na
port 80 a ověřit `GET /api/v1/sys/device_info` (`device_model_name` začíná na `Tiiny`).
