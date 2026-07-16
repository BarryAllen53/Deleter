# Deleter

[English documentation](README.md) · [Türkçe Dokumentation](README.tr.md)

Deleter ist eine barrierearme Windows-Desktopanwendung zur Analyse von Speicherplatz und zur sicheren Prüfung möglicher Bereinigungen. Große Dateien und installierte Programme werden angezeigt, während kritische Windows-Pfade technisch geschützt bleiben.

## Status

Version 0.1.0 ist eine frühe öffentliche Version mit Schwerpunkt auf sicherem Scannen, Schutzstatus, Barrierefreiheit und Simulation. Löschen und Deinstallieren sind noch nicht als destruktive Aktionen aktiviert.

## Funktionen

- Registerkarten „Programme“ und „Dateien“ mit inkrementeller Hintergrundanalyse.
- Mehrfachauswahl mit gesperrten und nicht zugänglichen Elementen.
- Größenfilter ab 500 MB.
- Pausieren, Fortsetzen und Abbrechen.
- Englisch, Deutsch und Türkisch.
- Native Qt-Tastaturbedienung und Accessible-Output-2-Ankündigungen.
- ACL-bewusste Windows-Fehlerbehandlung und UAC-Unterstützung.
- Simulationsvorschau vor zukünftigen destruktiven Vorgängen.

## Sicherheit

Große Dateien gelten niemals automatisch als unnötig. Windows-, Boot-, Treiber-, Wiederherstellungs-, Sicherheits-, Paket-, Programm-, Reparse-Point- und unklare ACL-Bereiche bleiben gesperrt oder nicht zugänglich. Die Anwendung übernimmt keinen Besitz und verändert keine ACLs.

## Barrierefreiheit und Sprachen

Native Qt-Rollen, Namen, Fokusreihenfolge und Kontrollzustände werden verwendet. Wichtige Scan- und Warnereignisse werden, sofern verfügbar, über Accessible Output 2 angekündigt. Unterstützt werden Englisch, Deutsch und Türkisch.

## Anforderungen und Start

Windows 10 oder Windows 11 und Python 3.14.5 werden für den Quellcode benötigt. Für normale Nutzer ist ein fertiges Release vorgesehen. Aus dem Quellcode startet `run.bat` die virtuelle Umgebung, installiert Abhängigkeiten und führt `python -m app` aus. Entwickler können `requirements-dev.txt` installieren.

## Verwendung

Beim Start beginnt automatisch eine Systemanalyse. Dateien werden nach Mindestgröße gefiltert und schrittweise angezeigt. Programme stammen aus unterstützten Windows-Deinstallationsregistrierungen. Ausgewählte Elemente können geprüft und simuliert werden; gesperrte Kontrollkästchen lassen sich nicht aktivieren.

## Datenschutz, Einschränkungen und Beiträge

Dateilisten, Pfade, Programminformationen und Nutzungsdaten verlassen das Gerät nicht. Destruktive Bereinigung, vollständige Deinstallationsanbieter, Exporte und ein signiertes portables Release sind in 0.1.0 noch nicht aktiviert. Siehe [ROADMAP.md](ROADMAP.md). Fehler und Beiträge sind in [CONTRIBUTING.md](CONTRIBUTING.md) beschrieben; Sicherheitsprobleme gehören in GitHub Security Advisories gemäß [SECURITY.md](SECURITY.md).

## Lizenz

Deleter steht unter der [MIT-Lizenz](LICENSE).
