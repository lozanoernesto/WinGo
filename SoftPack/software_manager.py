#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de descarga e instalación de software
"""

import os
import ssl
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
import shutil
import contextlib
from contextlib import redirect_stdout, redirect_stderr, nullcontext
import glob
from config import SOFTWARE_CATALOG, APP_CONFIG
import time
import webbrowser


class SoftwareManager:
    """Clase para gestionar descarga e instalación de software"""
    
    def __init__(self):
        self.download_dir = Path(APP_CONFIG['download_dir'])
        self.temp_dir = Path(APP_CONFIG['temp_dir'])
        # Mapear descargas exitosas: software_id -> software_id_real (para fallbacks)
        self._download_map = {}
        # Archivo de auditoría para instalaciones silenciosas
        self._install_log = self.temp_dir / 'install_log.txt'

        # Crear directorios si no existen
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        # Asegurar que exista el archivo de log
        try:
            self._install_log.parent.mkdir(parents=True, exist_ok=True)
            self._install_log.touch(exist_ok=True)
        except Exception:
            pass
        
    def download(self, software_id):
        """
        Descargar software
        
        Args:
            software_id: ID del software en el catálogo
            
        Returns:
            bool: True si la descarga fue exitosa
        """
        if software_id not in SOFTWARE_CATALOG:
            print(f"Error: Software '{software_id}' no encontrado en el catálogo")
            return False
        
        software = SOFTWARE_CATALOG[software_id]
        download_url = software['download_url']
        installer_name = software['installer_name']
        
        destination = self.download_dir / installer_name
        
        # Si ya existe, preguntar si reemplazar
        if destination.exists():
            print(f"El archivo {installer_name} ya existe")
            # Por ahora, usar el existente
            return True
        
        # ¿Modo silencioso para este software?
        silent = software.get('silent', False)
        cm = self._suppress_output() if silent else nullcontext()
        destination = None  # por si falla antes de asignar

        try:
            if not silent:
                print(f"Descargando {software['name']}...")
                print(f"URL: {download_url}")

            # Configurar headers para evitar bloqueos
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9'
            }

            # Añadir Referer/Origin para fuentes que lo requieran
            if software_id == 'riot':
                headers['Referer'] = 'https://launcher.riotgames.com/'
                headers['Origin'] = 'https://launcher.riotgames.com'
            elif software_id == 'battlenet':
                # Battle.net puede requerir Referer/Origin para descargas directas
                headers['Referer'] = 'https://www.blizzard.com/'
                headers['Origin'] = 'https://www.blizzard.com'
            elif software_id == 'teams':
                # CDN de Microsoft Teams puede validar origen
                headers['Referer'] = 'https://teams.microsoft.com/'
                headers['Origin'] = 'https://teams.microsoft.com'
            elif software_id == 'discord':
                # Endpoints de Discord pueden validar origen en algunos entornos
                headers['Referer'] = 'https://discord.com/'
                headers['Origin'] = 'https://discord.com'
            elif software_id == 'crystaldisk':
                # SourceForge a veces requiere Referer para permitir descarga
                headers['Referer'] = 'https://sourceforge.net/'

            request = urllib.request.Request(download_url, headers=headers)
            # Opener que sigue redirecciones y usa SSL por defecto (evita errores de certificado en Windows)
            ssl_ctx = ssl.create_default_context()
            opener = urllib.request.build_opener(
                urllib.request.HTTPRedirectHandler(),
                urllib.request.HTTPSHandler(context=ssl_ctx),
            )
            opener.addheaders = [(k, v) for k, v in headers.items()]

            # No usar HEAD: muchos servidores devuelven 403/405; GET con redirects es más fiable
            with cm:
                with opener.open(request, timeout=APP_CONFIG['timeout']) as response:
                    # Resolver nombre final del archivo usando Content-Disposition o la URL final
                    final_url = response.geturl()
                    content_disp = response.getheader('Content-Disposition') or ''
                    content_type = (response.getheader('Content-Type') or '').lower()

                    # Si la respuesta es HTML, solo rechazar si tampoco es descarga por Content-Disposition ni URL directa
                    final_url = response.geturl()
                    url_looks_like_installer = final_url.lower().endswith(('.exe', '.msi', '.zip'))
                    disp_attachment = 'attachment' in content_disp.lower() and any(
                        ext in content_disp.lower() for ext in ('.exe', '.msi', '.zip'))
                    is_binary = ('application/octet-stream' in content_type or
                                 'application/x-msdownload' in content_type or
                                 'application/x-msi' in content_type)
                    if 'text/html' in content_type and not is_binary and not url_looks_like_installer and not disp_attachment:
                        if not silent:
                            print(f"Error: No se obtuvo un instalador (Content-Type: {content_type}, URL final: {final_url}).")
                            print("Se usará la URL directa del catálogo; si falla, descarga manualmente desde la web oficial.")
                        try:
                            if self._try_fallbacks(software_id):
                                return True
                        except Exception:
                            pass
                        return False

                    # Siempre guardar con el nombre del catálogo (installer_name) para tener un solo archivo
                    destination = self.download_dir / installer_name

                    # Descargar por chunks para poder mostrar progreso si existe Content-Length
                    total_size = response.getheader('Content-Length')
                    try:
                        total_size = int(total_size) if total_size else None
                    except Exception:
                        total_size = None

                    chunk_size = 8192
                    downloaded = 0
                    with open(destination, 'wb') as out_file:
                        while True:
                            chunk = response.read(chunk_size)
                            if not chunk:
                                break
                            out_file.write(chunk)
                            downloaded += len(chunk)
                            if total_size:
                                percent = downloaded * 100 / total_size
                                print(f"\r{percent:.1f}% ({downloaded / 1024 / 1024:.1f} MB / {total_size / 1024 / 1024:.1f} MB)", end='')
                if total_size:
                    # cuando no es silencioso, imprimimos un salto de línea final
                    if not silent:
                        print()

            if not silent:
                print(f"Descarga completada: {destination}")
            # Registrar que la descarga del software_id original se completó
            self._download_map[software_id] = software_id

            # Si es un ZIP, extraer y localizar un .exe para usar como instalador
            try:
                import zipfile
                if zipfile.is_zipfile(destination):
                    extract_dir = self.temp_dir / f"extracted_{software_id}"
                    if extract_dir.exists():
                        shutil.rmtree(extract_dir)
                    extract_dir.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(destination, 'r') as zf:
                        zf.extractall(extract_dir)

                    exe_candidates = list(extract_dir.rglob('*.exe'))
                    if exe_candidates:
                        exe_path = exe_candidates[0]
                        # Guardar como stem.exe (ej. crystaldisk_installer.exe) para no sobrescribir el .zip
                        target = self.download_dir / (Path(installer_name).stem + '.exe')
                        shutil.copy2(exe_path, target)
                        if not silent:
                            print(f"Extraído y preparado instalador: {target}")
            except Exception as e:
                if not silent:
                    print(f"Advertencia: no se pudo procesar archivo comprimido: {e}")

            return True

        except urllib.error.URLError as e:
            if not silent:
                print(f"Error de URL al descargar: {e}")
            # Intentar fallbacks configurados para este software (si existen)
            # Si es Battle.net, abrir la página oficial para descarga manual y esperar el instalador
            if software_id == 'battlenet':
                try:
                    if self._prompt_manual_download_and_wait(software_id):
                        return True
                except Exception as e2:
                    if not silent:
                        print(f"Error al esperar instalador manual: {e2}")

            try:
                if self._try_fallbacks(software_id):
                    return True
            except Exception:
                pass
            return False
        except Exception as e:
                print(f"Error al descargar {software['name']}: {e}")
                try:
                    if destination and destination.exists():
                        destination.unlink()
                except Exception:
                    pass
                # Intentar fallbacks configurados para este software (si existen)
                try:
                    if self._try_fallbacks(software_id):
                        return True
                except Exception:
                    pass
                return False
    def _prompt_manual_download_and_wait(self, software_id, wait_time=None):
        """Abrir la página de descarga en el navegador y esperar a que el instalador aparezca.

        Busca en la carpeta de descargas configurada y en la carpeta Downloads del usuario
        por un ejecutable cuyo nombre contenga 'battle' o 'battlenet' durante un tiempo.
        """
        software = SOFTWARE_CATALOG.get(software_id, {})
        url = software.get('download_url')
        installer_name = software.get('installer_name')
        silent = software.get('silent', False)

        # Abrir navegador en la página de descarga
        try:
            if not silent:
                print(f"Abriendo navegador para descargar manualmente: {url}")
            webbrowser.open(url)
        except Exception as e:
            if not silent:
                print(f"Advertencia: no se pudo abrir el navegador automáticamente: {e}")

        timeout = wait_time if wait_time is not None else APP_CONFIG.get('timeout', 300)
        poll_interval = 3
        end_time = time.time() + timeout

        # Carpetas a vigilar
        download_paths = [self.download_dir, Path.home() / 'Downloads']

        def find_installer():
            for d in download_paths:
                if not d.exists():
                    continue
                for p in d.iterdir():
                    if p.is_file() and p.suffix.lower() in ('.exe', '.msi'):
                        name = p.name.lower()
                        if 'battle' in name or 'battlenet' in name or 'blizzard' in name or 'bnet' in name:
                            return p
            return None

        if not silent:
            print(f"Esperando instalador hasta {timeout} segundos... (revisa tu carpeta de descargas)")
        while time.time() < end_time:
            found = find_installer()
            if found:
                if not silent:
                    print(f"Instalador encontrado: {found}")
                # Copiar al nombre esperado si hace falta
                target = self.download_dir / installer_name
                try:
                    if not self.download_dir.exists():
                        self.download_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(found, target)
                    # Registrar que está disponible
                    self._download_map[software_id] = software_id
                    if not silent:
                        print(f"Copiado instalador a: {target}")
                    return True
                except Exception as e:
                    if not silent:
                        print(f"Error al copiar instalador: {e}")
                    return False
            time.sleep(poll_interval)

        if not silent:
            print("Tiempo de espera agotado esperando descarga manual del instalador.")
        return False
    def install(self, software_id):
        """
        Instalar software descargado
        
        Args:
            software_id: ID del software en el catálogo
            
        Returns:
            bool: True si la instalación fue exitosa
        """
        if software_id not in SOFTWARE_CATALOG:
            print(f"Error: Software '{software_id}' no encontrado en el catálogo")
            return False
        
        software = SOFTWARE_CATALOG[software_id]
        installer_name = software['installer_name']
        install_args = software['install_args']

        # Si hubo un fallback exitoso durante la descarga, usar el software real descargado
        effective_id = self._download_map.get(software_id, software_id)
        if effective_id != software_id:
            fb = SOFTWARE_CATALOG.get(effective_id, {})
            fb_installer = fb.get('installer_name')
            if fb_installer:
                installer_name = fb_installer
                software = fb

        # Intentar localizar el instalador: primero el nombre esperado, si no, buscar alternativas
        installer_path = self.download_dir / installer_name
        if not installer_path.exists():
            # Buscar instalador correspondiente al software efectivo
            alt = self._find_installer(effective_id)
            if alt:
                print(f"Nota: instalador esperado '{installer_name}' no encontrado. Usando '{alt.name}'")
                installer_path = alt
            else:
                print(f"Error: Instalador no encontrado en {installer_path}")
                print("Por favor, descarga el software primero")
                return False
        
        # Verificar modo silencioso
        silent = software.get('silent', False)
        cm = self._suppress_output() if silent else nullcontext()
        try:
            with cm:
                print(f"Instalando {software['name']}...")
                print(f"Ejecutando: {installer_path} {install_args}")
                
                # Ejecutar instalador
                if installer_name.endswith('.msi'):
                    # Para instaladores MSI
                    cmd = f'msiexec.exe /i "{installer_path}" {install_args}'
                else:
                    # Para instaladores EXE
                    cmd = f'"{installer_path}" {install_args}'

                # Discord (y otros Squirrel) necesitan tratamiento especial:
                # - No capturar output (bloquea el proceso)
                # - Usar Popen en vez de run (el instalador lanza Discord y no termina)
                is_squirrel = software_id in ('discord', 'teams', 'spotify')
                
                if is_squirrel:
                    print(f"  (Instalador tipo Squirrel: ejecución sin captura de salida)")
                    try:
                        popen_kwargs = {
                            'shell': True,
                            'cwd': str(self.download_dir),
                            'stdout': subprocess.DEVNULL,
                            'stderr': subprocess.DEVNULL,
                        }
                        if os.name == 'nt':
                            try:
                                popen_kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
                            except Exception:
                                pass
                        proc = subprocess.Popen(cmd, **popen_kwargs)
                        # Esperar máximo 120s a que el proceso principal termine
                        try:
                            proc.wait(timeout=120)
                        except subprocess.TimeoutExpired:
                            # Es normal: Squirrel lanza la app y el proceso padre queda
                            print(f"  El instalador sigue ejecutándose (normal para {software['name']})")
                    except Exception as e:
                        print(f"  Error al lanzar instalador: {e}")

                    # Verificar instalación con espera (Squirrel tarda en colocar archivos)
                    verify_timeout = int(software.get('install_verify_timeout', 120))
                    print(f"  Verificando instalación durante {verify_timeout}s...")
                    success = self._wait_for_installed(software_id, timeout=verify_timeout)
                    if success:
                        print(f"{software['name']} instalado correctamente (verificado)")
                    else:
                        print(f"No se pudo verificar la instalación de {software['name']}")
                else:
                    # Flujo normal para instaladores estándar
                    run_kwargs = {
                        'shell': True,
                        'capture_output': True,
                        'text': True,
                        'timeout': 600,  # 10 minutos timeout
                        'cwd': str(self.download_dir),
                    }

                    # Si estamos en modo silencioso en Windows, ocultar ventana
                    if silent and os.name == 'nt':
                        try:
                            run_kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
                        except Exception:
                            try:
                                si = subprocess.STARTUPINFO()
                                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                                run_kwargs['startupinfo'] = si
                            except Exception:
                                pass

                    result = subprocess.run(cmd, **run_kwargs)
                    
                    success = False
                    if result.returncode == 0:
                        if not silent:
                            print(f"{software['name']} instalado correctamente")
                        success = True
                    else:
                        if not silent:
                            print(f"Advertencia: El instalador retornó código {result.returncode}")
                        # Algunos instaladores retornan códigos no-cero incluso cuando tienen éxito
                        if self.check_installed(software_id):
                            if not silent:
                                print(f"{software['name']} instalado correctamente (verificado)")
                            success = True
                        else:
                            if not silent:
                                print(f"Error durante la instalación")
                                if result.stderr:
                                    print(f"Error: {result.stderr}")
                            success = False

                    # Verificación con espera si el software lo requiere
                    verify_after_install = software.get('verify_after_install', False)
                    if verify_after_install and not success:
                        verify_timeout = int(software.get('install_verify_timeout', 120))
                        if not silent:
                            print(f"Verificando instalación de {software['name']} durante {verify_timeout}s...")
                        success = self._wait_for_installed(software_id, timeout=verify_timeout)
                        if not silent:
                            if success:
                                print(f"{software['name']} instalado correctamente (verificado con espera)")
                            else:
                                print(f"No se pudo verificar la instalación de {software['name']} tras la espera")

                # Registrar instalación en log si fue silenciosa
                try:
                    if silent:
                        from datetime import datetime
                        with open(self._install_log, 'a', encoding='utf-8') as lf:
                            lf.write(f"{datetime.utcnow().isoformat()}Z\t{software_id}\t{software['name']}\t{'OK' if success else 'FAIL'}\n")
                except Exception:
                    pass

                return success
        except subprocess.TimeoutExpired:
            print(f"Error: Tiempo de espera agotado al instalar {software['name']}")
            return False
        except Exception as e:
            print(f"Error al instalar {software['name']}: {e}")
            return False
    
    def check_installed(self, software_id):
        """
        Verificar si un software está instalado
        
        Args:
            software_id: ID del software en el catálogo
            
        Returns:
            bool: True si el software está instalado
        """
        if software_id not in SOFTWARE_CATALOG:
            return False
        
        software = SOFTWARE_CATALOG[software_id]
        check_paths = software.get('check_paths')
        if not check_paths:
            check_paths = [software['check_path']]

        username = os.getenv('USERNAME', 'User')
        for check_path in check_paths:
            resolved = check_path.replace('{username}', username)
            if '*' in resolved:
                matches = glob.glob(resolved)
                if len(matches) > 0:
                    return True
            else:
                if Path(resolved).exists():
                    return True

        return False

    def _wait_for_installed(self, software_id, timeout=120, poll_interval=2):
        """Esperar a que el software aparezca como instalado."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                if self.check_installed(software_id):
                    return True
            except Exception:
                pass
            time.sleep(poll_interval)
        return self.check_installed(software_id)

    def _find_installer(self, software_id):
        """Buscar un instalador en el directorio de descargas como alternativa.

        Heurística:
        - Si existe el nombre configurado, lo devuelve.
        - Busca archivos cuyo nombre contenga el `software_id` o palabras del nombre.
        - Si no hay coincidencias, devuelve el .exe/.msi más reciente si existe.
        """
        software = SOFTWARE_CATALOG.get(software_id, {})
        installer_name = software.get('installer_name', '')
        name = software.get('name', '').lower()

        # Comprobar nombre exacto
        exact = self.download_dir / installer_name
        if exact.exists():
            return exact

        candidates = [p for p in self.download_dir.iterdir() if p.is_file()]

        # Buscar por software_id o palabras del nombre
        words = [w for w in name.split() if len(w) > 2]
        for p in candidates:
            fn = p.name.lower()
            if software_id.lower() in fn:
                return p
            for w in words:
                if w in fn:
                    return p

        # Fallback: el .exe/.msi más reciente
        exe_msi = [p for p in candidates if p.suffix.lower() in ('.exe', '.msi')]
        if exe_msi:
            exe_msi.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return exe_msi[0]

        return None
    
    def _try_fallback_urls(self, software_id):
        """Intentar URLs alternativas (fallback_urls) para descargar el mismo software.

        Recorre la lista de 'fallback_urls' del catálogo y prueba descargar desde cada
        una hasta que alguna funcione. Como último recurso, si tiene 'manual_download_url',
        abre el navegador para descarga manual.
        Devuelve True si alguna descarga fue exitosa.
        """
        software = SOFTWARE_CATALOG.get(software_id, {})
        fallback_urls = software.get('fallback_urls', [])
        silent = software.get('silent', False)
        installer_name = software.get('installer_name', '')

        for url in fallback_urls:
            if not silent:
                print(f"Intentando URL alternativa: {url}")
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': '*/*',
                }
                request = urllib.request.Request(url, headers=headers)
                ssl_ctx = ssl.create_default_context()
                opener = urllib.request.build_opener(
                    urllib.request.HTTPRedirectHandler(),
                    urllib.request.HTTPSHandler(context=ssl_ctx),
                )
                destination = self.download_dir / installer_name
                with opener.open(request, timeout=APP_CONFIG['timeout']) as response:
                    content_type = (response.getheader('Content-Type') or '').lower()
                    if 'text/html' in content_type:
                        if not silent:
                            print(f"  URL devolvió HTML, saltando...")
                        continue
                    total_size = response.getheader('Content-Length')
                    try:
                        total_size = int(total_size) if total_size else None
                    except Exception:
                        total_size = None
                    downloaded = 0
                    with open(destination, 'wb') as out_file:
                        while True:
                            chunk = response.read(8192)
                            if not chunk:
                                break
                            out_file.write(chunk)
                            downloaded += len(chunk)
                            if total_size and not silent:
                                percent = downloaded * 100 / total_size
                                print(f"\r  {percent:.1f}% ({downloaded / 1024 / 1024:.1f} MB)", end='')
                    if not silent and total_size:
                        print()
                if destination.exists() and destination.stat().st_size > 1000:
                    if not silent:
                        print(f"Descarga exitosa desde URL alternativa: {destination}")
                    self._download_map[software_id] = software_id
                    return True
                else:
                    if destination.exists():
                        destination.unlink()
            except Exception as e:
                if not silent:
                    print(f"  Falló URL alternativa: {e}")

        # Último recurso: abrir navegador para descarga manual
        manual_url = software.get('manual_download_url')
        if manual_url:
            if not silent:
                print(f"Abriendo navegador para descarga manual: {manual_url}")
            try:
                webbrowser.open(manual_url)
                # Esperar a que el archivo aparezca en la carpeta de descargas
                if self._prompt_manual_download_and_wait(software_id):
                    return True
            except Exception as e:
                if not silent:
                    print(f"Error al abrir navegador: {e}")

        return False

    def _try_fallbacks(self, software_id):
        """Intentar descargar alternativas (fallbacks) configuradas para un software.

        Primero intenta fallback_urls (URLs alternativas para el mismo software).
        Si el software tiene la clave 'fallbacks' en el catálogo, intenta descargar
        cada alternativa en orden hasta que una de ellas se descargue correctamente.
        Devuelve True si alguna descarga de fallback fue exitosa.
        """
        # Primero intentar URLs alternativas del mismo software
        if self._try_fallback_urls(software_id):
            return True

        software = SOFTWARE_CATALOG.get(software_id, {})
        fallbacks = software.get('fallbacks', [])
        silent = software.get('silent', False)
        if not fallbacks:
            return False

        for fb in fallbacks:
            if fb == software_id:
                continue
            if not silent:
                print(f"Intentando fallback: reemplazar '{software_id}' por '{fb}'...")
            if fb not in SOFTWARE_CATALOG:
                if not silent:
                    print(f"Advertencia: fallback '{fb}' no encontrado en el catálogo.")
                continue
            try:
                if self.download(fb):
                    # Registrar que el fallback fue el que se descargó para este software
                    self._download_map[software_id] = fb
                    if not silent:
                        print(f"Fallback exitoso con '{fb}'")
                    return True
                else:
                    if not silent:
                        print(f"Falló la descarga del fallback '{fb}'.")
            except Exception as e:
                if not silent:
                    print(f"Falló el fallback '{fb}': {e}")
        return False

    def install_all(self, software_list=None, force_silent=False):
        """Instala todos los items del catálogo (o los provistos en software_list).

        Args:
            software_list: lista opcional de IDs a instalar (si None, instala todo el catálogo)
            force_silent: si True forzará modo silencioso para todas las instalaciones

        Returns:
            dict: mapping software_id -> bool (True si instalado correctamente)
        """
        ids = software_list if software_list is not None else list(SOFTWARE_CATALOG.keys())
        results = {}
        for sid in ids:
            if sid not in SOFTWARE_CATALOG:
                results[sid] = False
                continue
            software = SOFTWARE_CATALOG[sid]
            # Forzar silent si se pidió
            original_silent = software.get('silent', False)
            if force_silent:
                software['silent'] = True

            try:
                dl_ok = self.download(sid)
                if not dl_ok:
                    results[sid] = False
                    continue
                inst_ok = self.install(sid)
                results[sid] = inst_ok
            except Exception:
                results[sid] = False
            finally:
                # Restaurar el valor original de silent si lo modificamos
                if force_silent:
                    software['silent'] = original_silent
        return results

    from contextlib import contextmanager

    @contextmanager
    def _suppress_output(self):
        """Context manager que redirige stdout/stderr a devnull."""
        try:
            with open(os.devnull, 'w') as devnull:
                with redirect_stdout(devnull), redirect_stderr(devnull):
                    yield
        except Exception:
            # Si falla la supresión, no propagar la excepción
            yield
    
    def uninstall(self, software_id):
        """
        Desinstalar software (funcionalidad básica)
        
        Args:
            software_id: ID del software en el catálogo
            
        Returns:
            bool: True si la desinstalación fue exitosa
        """
        # Esta función requeriría acceso al registro de Windows
        # o a los uninstallers de cada programa
        # Por ahora, solo es un placeholder
        print("Funcionalidad de desinstalación no implementada aún")
        return False
    
    def cleanup_downloads(self):
        """Limpiar archivos descargados"""
        try:
            if self.download_dir.exists():
                shutil.rmtree(self.download_dir)
                self.download_dir.mkdir(parents=True, exist_ok=True)
            print("Directorio de descargas limpiado")
            return True
        except Exception as e:
            print(f"Error al limpiar descargas: {e}")
            return False

    def cleanup_temp(self):
        """
        Limpiar archivos temporales sin tocar las descargas.
        Se usa al cerrar la app en modo ultra portable.
        """
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            # Recrear log para próximas ejecuciones
            try:
                self._install_log = self.temp_dir / 'install_log.txt'
                self._install_log.touch(exist_ok=True)
            except Exception:
                pass
            print("Directorio temporal limpiado")
            return True
        except Exception as e:
            print(f"Error al limpiar temporales: {e}")
            return False
    
    def get_download_size(self):
        """Obtener tamaño total de descargas"""
        total_size = 0
        if self.download_dir.exists():
            for file in self.download_dir.iterdir():
                if file.is_file():
                    total_size += file.stat().st_size
        return total_size
    
    def list_downloaded(self):
        """Listar software descargado"""
        downloaded = []
        if self.download_dir.exists():
            for file in self.download_dir.iterdir():
                if file.is_file():
                    downloaded.append({
                        'name': file.name,
                        'size': file.stat().st_size,
                        'path': str(file)
                    })
        return downloaded

