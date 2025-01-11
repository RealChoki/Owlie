## Aufgabe 1: Datentypen und Ausdrücke (3 Punkte)

### a) Variableninitialisierung 
Deklarieren Sie eine Variable mit dem Variablennamen `zaehler` vom Datentyp `int` und initialisieren Sie die Variable mit dem Wert `5`.

### b) Variablendeklaration    
Deklarieren Sie eine Variable mit dem Variablennamen `vorname` vom Datentyp `String`.

### c) Operatoren und Ausdrücke
Zu welchem Datentyp und Wert werten die folgenden Ausdrücke aus?

| Ausdruck   | Datentyp  | Wert   |
|------------|-----------|--------|
| `3 % 5`    |           |        |
| `8.2 * 1.5`|           |        |
| `"Ana" + "nas"` |      |        |
| `8 / 5`    |           |        |

---

## Aufgabe 2: Fehleranalyse und Codekorrektur (4 Punkte)

Die Methode `textAusgabe` soll den String im Eingabeparameter `text` so oft auf der Konsole ausgeben, wie der Wert des Eingabeparameters `num`.

```java
public static void textAusgabe(String text, int num) {

    int i = 0;

    while (i < 5) {

        System.out.println("Ein String");
        i++;
    }
}
```

### 1. 
Die Methode setzt die gewünschte Funktionalität nicht um. Warum?

### 2. 
Wie müsste die Methode angepasst werden, so dass die gewünschte Funktionalität umgesetzt wird? Geben Sie den Programmcode und die Zeile(n) an, in welcher/welchen dieser eingefügt werden müsste.

---

## Aufgabe 3: Syntax und Programmstruktur (4 Punkte)

Die Methode `sum` soll drei ganze Zahlen als Eingabeparameter nehmen, sie miteinander multiplizieren und das Ergebnis zurückgeben.

```java
public static int sum(int a, int b, int c) {
    { int erg = 1;
    erg = erg * a * b * c
    return erg;
}
```

Das Programm kompiliert nicht. Beschreiben Sie, um welche(n) Fehler es sich handelt und markieren Sie diesen im Code.

---

## Aufgabe 4: Boolesche Logik und Wahrheitstabellen (4 Punkte)

Gegeben sei der folgende Ausdruck:

```java
boolean erg = (!x && !y) || (z ^ x);
```

Vervollständigen Sie die nachfolgende Tabelle für den gegebenen Ausdruck:

| `x`    | `y`    | `z`    | `erg`  |
|--------|--------|--------|--------|
| `true` | `true` | `true` |        |
| `true` | `true` | `false`|        |
| `true` | `false`| `true` |        |
| `true` | `false`| `false`|        |
| `false`| `true` | `true` |        |
| `false`| `true` | `false`|        |
| `false`| `false`| `true` |        |
| `false`| `false`| `false`|        |

---

## Aufgabe 5: Methodenverhalten und Testen (3 Punkte)

Welche Aussage(n) trifft/treffen auf die folgende Methode zu?

```java
public static int compute(int k) {
    int erg = 1;
    for (int i = 0; i < k; i++) {
        erg = erg * 3;
    }
    return erg;
}
```

1. Für `k=0` liefert die Methode den Wert `1`.  
2. Für `k=3` liefert die Methode den Wert `6`.  
3. Für `k<0` liefert die Methode den Wert `1`.  
4. Für `k<0` kann die Methode nicht ausgeführt werden.

---

## Aufgabe 6: Programmierung einfacher Funktionen (6 Punkte)

### a) 
Schreiben Sie eine Methode `countTrueBooleans`, die für ein als Parameter übergebenes Array die Anzahl an booleschen Werten mit dem Wert `true` zurückgibt.

**Beispiel:**

Für ein Array `{ true, false, false, true, true }` liefert die Methode `countTrueBooleans` den Wert `3`.

### b) 
Versehen Sie Ihre Methode mit einem entsprechenden Dokumentationskommentar (Javadoc). *(Tipp: Lassen Sie oberhalb der Methodendefinition Platz für Javadoc).*

---

## Aufgabe 7: Programmierung einfacher Funktionen (6 Punkte)

### a) 
Schreiben Sie eine Methode `calculateSquares`, die für eine gegebene Array von nicht-negativen ganzen Zahlen die Quadrate dieser Zahlen berechnet und sie auf der Konsole ausgibt.

**Beispiel:**

**Eingabe:** `[2, 3, 5, 7]`  
**Ausgabe auf der Konsole:**

```
4
9
25
49
```

### b) 
Versehen Sie Ihre Methode mit einem entsprechenden Dokumentationskommentar (Javadoc). *(Tipp: Lassen Sie oberhalb der Methodendefinition Platz für Javadoc).*

---

## Aufgabe 8: Objektorientierte Programmierung (10 Punkte)

Erstellen Sie eine Klasse `Spacecraft` (Raumfahrzeug). Ein Raumfahrzeug soll folgende Eigenschaften (Objektvariablen) besitzen:

- **Name des Raumfahrzeugs** (`name`)  
- **Typ des Raumfahrzeugs** (`type`, z.B. Raumschiff, Satellit)  
- **Baujahr des Raumfahrzeugs** (`year`)  
- **Aktuelle Geschwindigkeit in km/s** (`velocity`)  

### Anforderungen an die Klasse:

1. **Konstruktor:**  
   Der Konstruktor soll allen Objektvariablen beim Erstellen eines neuen Objekts Werte zuweisen. Die aktuelle Geschwindigkeit wird beim Erstellen auf `0` gesetzt.

2. **Methoden:**  
   - `accelerate(double acceleration)`: Erhöht die Geschwindigkeit des Raumfahrzeugs um den angegebenen Beschleunigungswert `acceleration` in km/s.  
   - `decelerate(double deceleration)`: Verringert die Geschwindigkeit des Raumfahrzeugs um den angegebenen Verzögerungswert `deceleration` in km/s. *Stellen Sie sicher, dass die Geschwindigkeit nicht negativ wird.*  
   - `printSpacecraftDetails()`: Gibt alle Informationen über das Raumfahrzeug auf der Konsole aus, einschließlich des Namens, des Typs, des Baujahrs und der aktuellen Geschwindigkeit.  
   - `launch()`: Gibt eine Meldung aus, dass das Raumfahrzeug gestartet wurde.  

3. **Getter und Setter:**  
   - Getter für den Namen und die aktuelle Geschwindigkeit.  
   - Setter für die aktuelle Geschwindigkeit.
