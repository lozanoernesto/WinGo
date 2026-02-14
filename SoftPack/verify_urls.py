#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica que todas las URLs del catálogo respondan y entreguen un instalador (no HTML)."""
import ssl
import urllib.request
import urllib.error
from config import SOFTWARE_CATALOG

TIMEOUT = 15
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
}

def check_url(software_id, url):
    """Devuelve (ok: bool, mensaje: str)."""
    if not url or not url.strip():
        return False, "URL vacía"
    extra_headers = dict(HEADERS)
    if software_id == 'teams':
        extra_headers['Referer'] = 'https://teams.microsoft.com/'
        extra_headers['Origin'] = 'https://teams.microsoft.com'
    elif software_id == 'battlenet':
        extra_headers['Referer'] = 'https://www.blizzard.com/'
        extra_headers['Origin'] = 'https://www.blizzard.com'
    elif software_id == 'crystaldisk':
        extra_headers['Referer'] = 'https://sourceforge.net/'
    req = urllib.request.Request(url, headers=extra_headers)
    ctx = ssl.create_default_context()
    opener = urllib.request.build_opener(
        urllib.request.HTTPRedirectHandler(),
        urllib.request.HTTPSHandler(context=ctx),
    )
    opener.addheaders = [(k, v) for k, v in extra_headers.items()]
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            code = getattr(resp, 'status', None) or (resp.getcode() if hasattr(resp, 'getcode') else 200)
            if code != 200:
                return False, f"HTTP {code}"
            final_url = resp.geturl()
            ct = (resp.getheader('Content-Type') or '').lower()
            # Leer solo los primeros bytes para ver si es binario
            chunk = resp.read(1024)
            if not chunk:
                return False, "Respuesta vacía"
            # Si Content-Type es HTML y la URL no termina en .exe/.msi/.zip, probablemente es página
            if 'text/html' in ct and not any(final_url.lower().endswith(ext) for ext in ('.exe', '.msi', '.zip')):
                return False, "Respuesta HTML (no instalador)"
            return True, f"OK (Content-Type: {ct[:50] if ct else 'N/A'})"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, str(e)[:80]

def main():
    print("Verificando URLs del catálogo...\n")
    ok_list = []
    fail_list = []
    for sid, data in SOFTWARE_CATALOG.items():
        name = data.get('name', sid)
        url = data.get('download_url', '')
        ok, msg = check_url(sid, url)
        if ok:
            ok_list.append((sid, name))
            print(f"  OK   {name}")
        else:
            fail_list.append((sid, name, url, msg))
            print(f"  FAIL {name}: {msg}")
    print("\n" + "=" * 60)
    print(f"Correctas: {len(ok_list)} | Fallidas: {len(fail_list)}")
    if fail_list:
        print("\nURLs que fallaron (revisar en config.py):")
        for sid, name, url, msg in fail_list:
            print(f"  - {name} ({sid})")
            print(f"    {url[:70]}...")
            print(f"    -> {msg}")

if __name__ == "__main__":
    main()
