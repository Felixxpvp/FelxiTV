# Kennzahlen

> Automatisch aus der Datenbank erzeugt. Letztes Update: 2026-06-22
> Quelle: `data/data.db` | Neu erzeugen: `python scripts/generate_metrics.py`

## Warenbestand
**Fleisch:**
| Produkt | Bestand | Einheit | Preis |
|---------|---------|---------|-------|
| Reh (Frischfleisch) ! | 0 | kg | - |
| Reh (Vakuum) ! | 0 | Paket | - |
| Wildschwein (Frischfleisch) ! | 0 | kg | - |
| Wildschwein (Vakuum) ! | 0 | Paket | - |

**Gemüse:**
| Produkt | Bestand | Einheit | Preis |
|---------|---------|---------|-------|
| Gemüsekorb gemischt ! | 0 | Korb | - |
| Paprika ! | 0 | kg | - |
| Salat ! | 0 | Stück | - |
| Tomaten ! | 0 | kg | - |
| Zucchini ! | 0 | kg | - |

**Met:**
| Produkt | Bestand | Einheit | Preis |
|---------|---------|---------|-------|
| Met 0.5L | 40 | Flasche | EUR 9.50 |
| Met 0.75L ! | 0 | Flasche | - |

**Saft:**
| Produkt | Bestand | Einheit | Preis |
|---------|---------|---------|-------|
| Apfelsaft 0.5L ! | 0 | Flasche | - |
| Birnensaft 0.5L ! | 0 | Flasche | - |
| Gemischter Fruchtsaft 0.5L ! | 0 | Flasche | - |

## Lager
✅ Alle Artikel über Mindestbestand.

## Kassenbuch
| | Betrag |
|---|---|
| Einnahmen gesamt | €31 |
| Ausgaben gesamt | €106 |
| **Saldo** | **€-74** |

**Diesen Monat:** Einnahmen €31 | Ausgaben €106 | Saldo €-74

**Letzte Buchungen:**
| Datum | Typ | Kategorie | Betrag |
|-------|-----|-----------|--------|
| 2026-06-20 | Einnahme | Fleisch-Verkauf | €12.00 |
| 2026-06-15 | Ausgabe | Jagd | €32.00 |
| 2026-06-10 | Einnahme | Met-Verkauf | €19.00 |
| 2026-06-05 | Ausgabe | Imkerei | €28.50 |
| 2026-06-01 | Ausgabe | Saatgut | €45.00 |

## Verkäufe
**Gesamt:** 2 Verkäufe | Umsatz: €31

**Diesen Monat:** 2 Verkäufe | €31

**Letzte Verkäufe:**
| Datum | Produkt | Preis | Kanal |
|-------|---------|-------|-------|
| 2026-06-22 | Wildschweinfleisch | €12.00 | Direktverkauf |
| 2026-06-22 | Met 0.5L | €19.00 | Direktverkauf |

## Wechselkurse
| Währung | Kurs (von USD) | Stand |
|---------|----------------|-------|
| AUD | 1.4257 | 2026-06-19 |
| CAD | 1.4152 | 2026-06-19 |
| CHF | 0.8065 | 2026-06-19 |
| EUR | 0.8721 | 2026-06-19 |
| GBP | 0.7557 | 2026-06-19 |
| JPY | 161.2300 | 2026-06-19 |

## Datenfrische
| Quelle | Letzter Datensatz | Status |
|--------|-------------------|--------|
| buchhaltung | 2026-06-20 | verbunden |
| fx_rates | 2026-06-19 | verbunden |
| lager | - | keine Datums-Spalte |
| verkauf | 2026-06-22 | verbunden |
| waren | - | keine Datums-Spalte |
