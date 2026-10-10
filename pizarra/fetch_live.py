"""Resultados casi en vivo desde el marcador público de ESPN (sin clave).
Descarga todos los partidos de la temporada actual de 8 ligas y guarda
pizarra/data/live/<DIV>.csv con: Date,Time,HomeTeam,AwayTeam,FTHG,FTAG,Status
Status: FT (terminado), LIVE (en juego), NS (no empezado).
"""
import csv, json, os, sys, time, urllib.request, urllib.error
from datetime import date, datetime, timedelta, timezone

LEAGUES = {"E0": "eng.1", "E1": "eng.2", "SP1": "esp.1", "I1": "ita.1",
           "D1": "ger.1", "F1": "fra.1", "P1": "por.1", "N1": "ned.1"}
OUT = os.path.join(os.path.dirname(__file__), "data", "live")
API = "https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={a}-{b}&limit=1000"

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

def get(url):
    for i in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 pizarra-datos", "Accept": "application/json"})
            return json.loads(urllib.request.urlopen(req, timeout=30).read())
        except urllib.error.HTTPError as e:
            log("  HTTP", e.code, url, e.read()[:200])
        except Exception as e:
            log("  fallo", url, repr(e)[:200])
        time.sleep(2)
    return None

today = date.today()
start = date(today.year if today.month >= 7 else today.year - 1, 7, 15)
end = today + timedelta(days=7)
os.makedirs(OUT, exist_ok=True)
ok = 0
for div, lg in LEAGUES.items():
    rows = []
    # en tramos de 30 días para no pedir demasiado de golpe
    a = start
    while a <= end:
        b = min(a + timedelta(days=29), end)
        js = get(API.format(lg=lg, a=a.strftime("%Y%m%d"), b=b.strftime("%Y%m%d")))
        for ev in (js or {}).get("events", []):
            try:
                comp = ev["competitions"][0]
                h = next(c for c in comp["competitors"] if c["homeAway"] == "home")
                w = next(c for c in comp["competitors"] if c["homeAway"] == "away")
                dt = datetime.fromisoformat(ev["date"].replace("Z", "+00:00")).astimezone(timezone(timedelta(hours=2)))
                st = comp["status"]["type"]
                status = "FT" if st.get("completed") else ("LIVE" if st.get("state") == "in" else "NS")
                rows.append(dict(Date=dt.strftime("%d/%m/%Y"), Time=dt.strftime("%H:%M"),
                                 HomeTeam=h["team"]["displayName"], AwayTeam=w["team"]["displayName"],
                                 FTHG=h.get("score", "") if status != "NS" else "",
                                 FTAG=w.get("score", "") if status != "NS" else "", Status=status))
            except (KeyError, StopIteration, ValueError) as e:
                log("  evento ignorado:", repr(e)[:120])
        a = b + timedelta(days=1)
    if rows:
        uniq = {(r["Date"], r["HomeTeam"], r["AwayTeam"]): r for r in rows}
        with open(os.path.join(OUT, f"{div}.csv"), "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(uniq.values())
        ok += 1
        log(div, len(uniq), "partidos,", sum(r["Status"] == "FT" for r in uniq.values()), "terminados")
    else:
        log(div, "sin partidos")
log("ligas guardadas:", ok, "| hora UTC", datetime.now(timezone.utc).isoformat(timespec="minutes"))
open(os.path.join(OUT, "_registro.txt"), "w").write("\n".join(LOG[-200:]) + "\n")
