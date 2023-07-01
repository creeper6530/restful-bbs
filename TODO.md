# TODOs

- [x] Přesuň TODO do zvláštního souboru, abys nemusel pořád dělat bordel v commitech
- [x] Pořeš, když je token potřeba, ale není dán (je vhodné použít error kód 499 nebo 401)
- [x] Odstraňuj to "=" na konci tokenů
- [x] Zkus programovat z RPi přes SSH, aby jsi mohl využít výhody Linuxu
- [x] Příklady pro login/logout
- [x] ~~Odeslat jen seznam Boardů při `GET /boards`~~ Odeslat počet příspěvků na boardu při `GET /boards` místo jejich listu
- [x] Přidej `register()`, `underister()`, `chpasswd()` a integruj do endpointu (zatím je to prováděné člověkem)
- [x] Rozděl `/auth` endpoint na jednotlivé `/auth/<action>`
- [ ] Sepiš dokumentaci
- [ ] Pořeš, když chybí i jiná políčka než token
- [ ] Logování akcí i s uživatelem (zjistíš dle tokenu) a IP
- [ ] Implementuj oprávnění (zatím lze bez loginu GETovat a s loginem POSTovat i DELETEovat vše)
- [ ] Klient
- [ ] Pořeš načítání celé BBS do paměti (optimalizuj paměť) (možná by to šlo pořešit migrací na SQL)