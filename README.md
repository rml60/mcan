# MCAN

**MicroPython - Modul fuer das Märklin can-Protokoll**

Es soll ein Modul zum Umgang mit Märklin can-Nachrichten
entstehen, dass im esp32 Umfeld genutzt werden kann.
Es ist noch viel zu tun, aber der grundsätzliche Umgang
mit Märklin can-Nachrichten ist realisiert.

Die Struktur einer Märklin can-Nachricht ist in der
Klasse McanMsgArray abgebildet.

Die Klassen McanCommand und McanDecode erben McanMsgArray.
McanDecode ist noch nicht in der Lage alle Nachrichten zu
dekodieren.

Es sind mit Sicherheit noch Fehler vorhanden und auch die Dokumentation der
einzelnen Komponenten fehlt noch. 
