Exit code: 0
Wall time: 0.6 seconds
Output:
# Deleter

[English documentation](README.md) · [Türkçe Dokumentation](README.tr.md)

Deleter ist eine barrierearme Windows-Desktopanwendung zur Analyse von Speicherplatz und zur sicheren Prüfung möglicher Bereinigungen. Große Dateien und installierte Programme werden angezeigt, während kritische Windows-Pfade technisch geschützt bleiben.

## Status

Version 0.2.0 ist die erste funktionale öffentliche Version. Sie umfasst geschütztes systemweites Scannen, geprüfte Bereinigung über den Windows-Papierkorb, unterstützte Deinstallation, Exporte, Barrierefreiheit und Simulation.

## Funktionen

- Registerkarten „Programme“ und „Dateien“ mit inkrementeller Hintergrundanalyse.
- Mehrfachauswahl mit gesperrten und nicht zugänglichen Elementen.
- Größenfilter ab 500 MB.
- Pausieren, Fortsetzen und Abbrechen.
- Englisch, Deutsch und Türkisch.
- Native Qt-Tastaturbedienung und Accessible-Output-2-Ankündigungen.
- ACL-bewusste Windows-Fehlerbehandlung und UAC-Unterstützung.
- Geprüfte Bereinigung verschiebt berechtigte Dateien nach Bestätigung in den Windows-Papierkorb; der Simulationsmodus bleibt verfügbar.
- Deinstallationsanbieter für Registrierung und Microsoft Store/AppX mit validierter Befehlsplanung und isolierter Ausführung.
- JSON- und CSV-Exporte der Scanergebnisse.

## Sicherheit

Große Dateien gelten niemals automatisch als unnötig. Windows-, Boot-, Treiber-, Wiederherstellungs-, Sicherheits-, Paket-, Programm-, Reparse-Point- und unklare ACL-Bereiche bleiben gesperrt oder nicht zugänglich. Die Anwendung übernimmt keinen Besitz und verändert keine ACLs.

## Barrierefreiheit und Sprachen

Native Qt-Rollen, Namen, Fokusreihenfolge und Kontrollzustände werden verwendet. Wichtige Scan- und Warnereignisse werden, sofern verfügbar, über Accessible Output 2 angekündigt. Unterstützt werden Englisch, Deutsch und Türkisch.

## Anforderungen und Start

Windows 10 oder Windows 11 und Python 3.14.5 werden für den Quellcode benötigt. Für normale Nutzer steht ein portables ZIP im Release-Bereich bereit. Aus dem Quellcode startet `run.bat` die virtuelle Umgebung, installiert Abhängigkeiten und führt `python -m app` aus. Entwickler können `requirements-dev.txt` installieren.

## Verwendung

Beim Start beginnt automatisch eine Systemanalyse. Dateien werden nach Mindestgröße gefiltert und schrittweise angezeigt. Programme stammen aus unterstützten Windows-Deinstallationsregistrierungen. Ausgewählte Elemente können geprüft und simuliert werden; gesperrte Kontrollkästchen lassen sich nicht aktivieren.

## Datenschutz, Einschränkungen und Beiträge

Dateilisten, Pfade, Programminformationen und Nutzungsdaten verlassen das Gerät nicht. Permanente Löschung ist absichtlich nicht verfügbar; Bereinigung ist auf geprüfte, bestätigte Verschiebungen in den Papierkorb beschränkt. Die Signatur wird vom Release-Workflow aktiviert, sobald die Zertifikats-Secrets hinterlegt sind. Siehe [ROADMAP.md](ROADMAP.md). Fehler und Beiträge sind in [CONTRIBUTING.md](CONTRIBUTING.md) beschrieben; Sicherheitsprobleme gehören in GitHub Security Advisories gemäß [SECURITY.md](SECURITY.md).

## Lizenz

Deleter steht unter der [MIT-Lizenz](LICENSE).

