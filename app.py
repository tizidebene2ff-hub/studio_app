import math
import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- FORMULARIO ENCICLOPEDICO ---
FORMULARIO = {
    "Matematica": [
        ("Algebra", "Equazione 1° grado", "ax + b = 0  =>  x = -b / a (con a ≠ 0)"),
        ("Algebra", "Equazione 2° grado", "ax² + bx + c = 0  =>  Δ = b² - 4ac ;  x = (-b ± √Δ) / (2a)"),
        ("Algebra", "Prodotti notevoli", "(a±b)² = a² ± 2ab + b²  |  a² - b² = (a-b)(a+b)"),
        ("Algebra", "Proprietà potenze", "aᵐ · aⁿ = aᵐ⁺ⁿ  |  aᵐ / aⁿ = aᵐ⁻ⁿ  |  (aᵐ)ⁿ = aᵐ·ⁿ"),
        ("Algebra", "Logaritmi", "logₐ(b) = c ⇔ aᶜ = b  |  log(xy) = log x + log y"),
        ("Geometria Piana", "Triangolo", "Area = (b · h) / 2  |  Erone: A = √[p(p-a)(p-b)(p-c)]"),
        ("Geometria Piana", "Teorema di Pitagora", "c = √(a² + b²)  (in un triangolo rettangolo)"),
        ("Geometria Piana", "Cerchio", "Circonferenza = 2πr  |  Area = πr²"),
        ("Geometria Solida", "Sfera e Cilindro", "V_sfera = (4/3)πr³ , A = 4πr²  |  V_cilindro = πr²h"),
        ("Trigonometria", "Identità fondamentale", "sin²(α) + cos²(α) = 1  |  tan(α) = sin(α)/cos(α)"),
        ("Trigonometria", "Teorema dei seni e coseni", "a/sin α = b/sin β = c/sin γ  |  c² = a² + b² - 2ab·cos γ"),
        ("Analisi", "Derivate fondamentali", "D[xⁿ] = n·xⁿ⁻¹  |  D[eˣ] = eˣ  |  D[ln x] = 1/x  |  D[sin x] = cos x"),
        ("Analisi", "Integrali fondamentali", "∫ xⁿ dx = xⁿ⁺¹/(n+1) + C  |  ∫ 1/x dx = ln|x| + C"),
    ],
    "Fisica": [
        ("Cinematica", "Moto Rettilineo Uniforme (MRU)", "s = s₀ + v · t  |  v = Δs / Δt"),
        ("Cinematica", "Moto Uniformemente Accelerato", "v = v₀ + a · t  |  s = s₀ + v₀t + ½at²  |  v² = v₀² + 2aΔs"),
        ("Cinematica", "Moto Circolare Uniforme", "v = 2πr / T = ω · r  |  a_c = v² / r = ω²r"),
        ("Dinamica", "Leggi di Newton", "F = m · a  |  P = m · g (g ≈ 9,81 m/s²)"),
        ("Dinamica", "Attrito e Legge di Hooke", "F_attr = μ · N  |  F_elastica = -k · Δx"),
        ("Lavoro ed Energia", "Lavoro e Potenza", "L = F · s · cos(θ)  |  P = L / Δt = F · v"),
        ("Lavoro ed Energia", "Energia Cinetica e Potenziale", "K = ½mv²  |  U_g = m·g·h  |  U_el = ½k·x²"),
        ("Fluidi", "Pressione e Stevino", "P = F / A  |  P = P₀ + ρ · g · h  |  Spinta Archimede: F_A = ρ_fluido · V_imm · g"),
        ("Termodinamica", "Calore e Gas Perfetti", "Q = m · c · ΔT  |  P · V = n · R · T (R = 8,314 J/mol·K)"),
        ("Termodinamica", "Primo Principio", "ΔU = Q - L  (variazione energia interna = calore assorbito - lavoro compiuto)"),
        ("Elettromagnetismo", "Legge di Coulomb e Campo E", "F = k₀ · |q₁·q₂| / r² (k₀ ≈ 8,99·10⁹ N·m²/C²)  |  E = F / q"),
        ("Elettromagnetismo", "Legge di Ohm e Potenza", "V = R · I  |  P = V · I = R · I²  |  R_serie = ΣRᵢ  |  1/R_par = Σ(1/Rᵢ)"),
        ("Onde e Ottica", "Onde e Rifrazione", "v = λ · f  |  Legge di Snell: n₁ · sin(θ₁) = n₂ · sin(θ₂)"),
    ],
    "Scienze": [
        ("Chimica", "Densità e Concentrazione", "d = m / V  |  Molarità M = n_moli / V_litri"),
        ("Chimica", "Moli e Massa Molare", "n = m / MM  |  N_particelle = n · N_A (N_A = 6,022 · 10²³ mol⁻¹)"),
        ("Chimica", "pH e Soluzioni", "pH = -log₁₀[H₃O⁺]  |  pOH = -log₁₀[OH⁻]  |  pH + pOH = 14 (a 25°C)"),
        ("Chimica", "Diluizione", "C₁ · V₁ = C₂ · V₂"),
        ("Biologia", "Fotosintesi Clorofilliana", "6 CO₂ + 6 H₂O + luce → C₆H₁₂O₆ + 6 O₂"),
        ("Biologia", "Respirazione Cellulare", "C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + ~30-32 ATP"),
        ("Biologia", "Dogma Centrale e Genetica", "DNA → (Trascrizione) → RNA → (Traduzione) → Proteine | A-T (o U), C-G"),
        ("Biologia", "Leggi di Mendel", "1ª Dominanza | 2ª Segregazione (3:1 in F₂) | 3ª Assortimento indipendente (9:3:3:1)"),
        ("Scienze della Terra", "Terremoti e Struttura Terra", "Magnitudo Richter (scala logaritmica) vs Intensità Mercalli | Crosta, Mantello, Nucleo"),
        ("Astronomia", "Leggi di Keplero e Gravitazione", "T² ∝ a³  |  F = G · (m₁ · m₂) / r²  (G = 6,674 · 10⁻¹¹ N·m²/kg²)"),
    ],
}

# --- BANCA QUIZ ---
DOMANDE_QUIZ = [
    {"materia": "Matematica", "domanda": "Qual è il discriminante Δ di x² - 5x + 6 = 0?", "risposta": "1", "spiegazione": "Δ = b² - 4ac = (-5)² - 4(1)(6) = 25 - 24 = 1."},
    {"materia": "Matematica", "domanda": "Quanto vale log₂(32)?", "risposta": "5", "spiegazione": "Perché 2⁵ = 32."},
    {"materia": "Matematica", "domanda": "Un triangolo rettangolo ha cateti 3 e 4. Quanto vale l'ipotenusa?", "risposta": "5", "spiegazione": "Teorema di Pitagora: √(3² + 4²) = √(9 + 16) = √25 = 5."},
    {"materia": "Fisica", "domanda": "Una forza di 20 N sposta un corpo di 4 kg. Qual è l'accelerazione in m/s²?", "risposta": "5", "spiegazione": "Seconda legge di Newton: a = F / m = 20 / 4 = 5 m/s²."},
    {"materia": "Fisica", "domanda": "Calcola l'energia cinetica (in J) di una massa di 2 kg che viaggia a 3 m/s.", "risposta": "9", "spiegazione": "K = ½ · m · v² = 0,5 · 2 · 3² = 9 J."},
    {"materia": "Fisica", "domanda": "Qual è la resistenza (in Ω) se una tensione di 12 V produce una corrente di 3 A?", "risposta": "4", "spiegazione": "Prima legge di Ohm: R = V / I = 12 / 3 = 4 Ω."},
    {"materia": "Scienze", "domanda": "Quante moli ci sono in 36 g di acqua (H₂O, massa molare = 18 g/mol)?", "risposta": "2", "spiegazione": "n = m / MM = 36 / 18 = 2 moli."},
    {"materia": "Scienze", "domanda": "Qual è il pH di una soluzione con concentrazione [H₃O⁺] = 10⁻³ M?", "risposta": "3", "spiegazione": "pH = -log₁₀(10⁻³) = 3."},
    {"materia": "Scienze", "domanda": "Un corpo ha massa 50 g e volume 25 cm³. Qual è la sua densità in g/cm³?", "risposta": "2", "spiegazione": "d = m / V = 50 / 25 = 2 g/cm³."},
]

HTML_TEMPLATE = """
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hub Studio Completo: Matematica, Fisica, Scienze</title>
  <style>
    :root { --primary: #2563eb; --bg: #f1f5f9; --card: #ffffff; --text: #0f172a; --muted: #475569; }
    body { font-family: system-ui, -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 16px; background: var(--bg); color: var(--text); }
    header { text-align: center; padding: 12px 0 20px; }
    h1 { margin: 0; font-size: 1.7rem; }
    .sub { color: var(--muted); margin: 4px 0 0; }
    .tabs { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
    .tab-btn { flex: 1; min-width: 110px; padding: 12px; border: none; border-radius: 10px; background: #cbd5e1; font-weight: bold; cursor: pointer; font-size: 0.95rem; }
    .tab-btn.active { background: var(--primary); color: #fff; }
    .section { display: none; }
    .section.active { display: block; }
    .card { background: var(--card); border-radius: 14px; padding: 18px; margin-bottom: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    label { display: block; margin-top: 10px; font-weight: 600; font-size: 0.92rem; }
    input, select, button.action { margin-top: 6px; padding: 10px 12px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 1rem; width: 100%; box-sizing: border-box; }
    button.action { background: var(--primary); color: #fff; border: none; font-weight: bold; cursor: pointer; margin-top: 14px; }
    button.action:hover { background: #1d4ed8; }
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
    .risultato { margin-top: 14px; padding: 14px; border-radius: 10px; background: #eff6ff; border-left: 4px solid var(--primary); white-space: pre-line; line-height: 1.5; }
    .ok { background: #ecfdf5; border-left-color: #10b981; }
    .err { background: #fef2f2; border-left-color: #ef4444; }
    .formula-item { border-bottom: 1px solid #e2e8f0; padding: 10px 0; }
    .formula-item:last-child { border-bottom: none; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 0.78rem; font-weight: bold; background: #e2e8f0; color: #334155; margin-right: 6px; }
    .formula-code { font-family: Consolas, monospace; background: #f8fafc; padding: 6px 10px; border-radius: 6px; display: block; margin-top: 5px; border: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <header>
    <h1>Laboratorio Studio Completo</h1>
    <p class="sub">Calcolatori guidati, formulario generale e quiz per Matematica, Fisica e Scienze</p>
  </header>

  <div class="tabs">
    <button class="tab-btn {{ 'active' if tab == 'calcolatori' else '' }}" onclick="openTab('calcolatori', this)">1. Calcolatori</button>
    <button class="tab-btn {{ 'active' if tab == 'formulario' else '' }}" onclick="openTab('formulario', this)">2. Formulario</button>
    <button class="tab-btn {{ 'active' if tab == 'quiz' else '' }}" onclick="openTab('quiz', this)">3. Quiz</button>
  </div>

  <!-- SEZIONE 1: CALCOLATORI -->
  <div id="calcolatori" class="section {{ 'active' if tab == 'calcolatori' else '' }}">
    <div class="card">
      <h2>Risolutore con passaggi</h2>
      <form method="post">
        <input type="hidden" name="azione" value="calcola">
        <input type="hidden" name="tab" value="calcolatori">

        <label for="strumento">Scegli argomento / formula</label>
        <select id="strumento" name="strumento" onchange="aggiornaEtichette()">
          <optgroup label="Matematica">
            <option value="eq2" {% if strumento == 'eq2' %}selected{% endif %}>Equazione 2° grado (ax² + bx + c = 0)</option>
            <option value="pitagora" {% if strumento == 'pitagora' %}selected{% endif %}>Teorema di Pitagora (cateti a, b)</option>
            <option value="cerchio" {% if strumento == 'cerchio' %}selected{% endif %}>Cerchio (raggio r → circonferenza e area)</option>
            <option value="log" {% if strumento == 'log' %}selected{% endif %}>Logaritmo in base b di x: log_b(x)</option>
          </optgroup>
          <optgroup label="Fisica">
            <option value="mrua" {% if strumento == 'mrua' %}selected{% endif %}>Moto Accelerato: s = v₀·t + ½·a·t²</option>
            <option value="newton" {% if strumento == 'newton' %}selected{% endif %}>2ª Legge di Newton: F = m · a</option>
            <option value="cinetica" {% if strumento == 'cinetica' %}selected{% endif %}>Energia Cinetica: K = ½ · m · v²</option>
            <option value="ohm" {% if strumento == 'ohm' %}selected{% endif %}>Legge di Ohm e Potenza (V, R)</option>
            <option value="gas" {% if strumento == 'gas' %}selected{% endif %}>Gas Perfetti: P = (n · R · T) / V</option>
          </optgroup>
          <optgroup label="Scienze / Chimica">
            <option value="densita" {% if strumento == 'densita' %}selected{% endif %}>Densità: d = m / V</option>
            <option value="moli" {% if strumento == 'moli' %}selected{% endif %}>Numero di moli: n = m / MM</option>
            <option value="ph" {% if strumento == 'ph' %}selected{% endif %}>Calcolo pH da [H₃O⁺] (in mol/L)</option>
          </optgroup>
        </select>

        <div class="grid-3">
          <div>
            <label id="lbl1" for="val1">Valore 1 (a)</label>
            <input id="val1" name="val1" type="number" step="any" value="{{ val1 }}" required>
          </div>
          <div id="box2">
            <label id="lbl2" for="val2">Valore 2 (b)</label>
            <input id="val2" name="val2" type="number" step="any" value="{{ val2 }}">
          </div>
          <div id="box3">
            <label id="lbl3" for="val3">Valore 3 (c)</label>
            <input id="val3" name="val3" type="number" step="any" value="{{ val3 }}">
          </div>
        </div>

        <button class="action" type="submit">Calcola e mostra passaggi</button>
      </form>

      {% if esito_calcolo %}
        <div class="risultato">{{ esito_calcolo }}</div>
      {% endif %}
    </div>
  </div>

  <!-- SEZIONE 2: FORMULARIO -->
  <div id="formulario" class="section {{ 'active' if tab == 'formulario' else '' }}">
    <div class="card">
      <h2>Formulario completo</h2>
      <input type="text" id="cercaFormula" onkeyup="filtraFormule()" placeholder="Cerca formula o argomento (es. Newton, logaritmi, pH, derivata, Ohm)...">
    </div>

    {% for materia, lista in formulario.items() %}
      <div class="card gruppo-materia">
        <h3>{{ materia }}</h3>
        {% for area, titolo, testo in lista %}
          <div class="formula-item">
            <span class="badge">{{ area }}</span> <strong>{{ titolo }}</strong>
            <span class="formula-code">{{ testo }}</span>
          </div>
        {% endfor %}
      </div>
    {% endfor %}
  </div>

  <!-- SEZIONE 3: QUIZ -->
  <div id="quiz" class="section {{ 'active' if tab == 'quiz' else '' }}">
    <div class="card">
      <h2>Allenamento a Quiz</h2>
      <p><span class="badge">{{ domanda.materia }}</span> <strong>{{ domanda.domanda }}</strong></p>
      <form method="post">
        <input type="hidden" name="azione" value="quiz">
        <input type="hidden" name="tab" value="quiz">
        <input type="hidden" name="idx_domanda" value="{{ idx_domanda }}">
        <label for="risposta_utente">Inserisci il risultato numerico</label>
        <input id="risposta_utente" name="risposta_utente" type="text" placeholder="Es. 5" required>
        <button class="action" type="submit">Verifica risposta</button>
      </form>

      {% if esito_quiz %}
        <div class="risultato {{ 'ok' if quiz_corretto else 'err' }}">{{ esito_quiz }}</div>
      {% endif %}
    </div>
  </div>

  <script>
    const CONFIG_CAMPI = {
      eq2:      ["Coefficiente a", "Coefficiente b", "Termine noto c"],
      pitagora: ["Cateto a", "Cateto b", null],
      cerchio:  ["Raggio r", null, null],
      log:      ["Argomento x (> 0)", "Base b (> 0, ≠ 1)", null],
      mrua:     ["Velocità iniziale v₀ (m/s)", "Accelerazione a (m/s²)", "Tempo t (s)"],
      newton:   ["Massa m (kg)", "Accelerazione a (m/s²)", null],
      cinetica: ["Massa m (kg)", "Velocità v (m/s)", null],
      ohm:      ["Tensione V (Volt)", "Resistenza R (Ohm)", null],
      gas:      ["Moli n (mol)", "Temperatura T (Kelvin)", "Volume V (m³)"],
      densita:  ["Massa m (g o kg)", "Volume V (cm³ o m³)", null],
      moli:     ["Massa campione m (g)", "Massa molare MM (g/mol)", null],
      ph:       ["Concentrazione [H₃O⁺] (mol/L, es. 0.001)", null, null]
    };

    function aggiornaEtichette() {
      const s = document.getElementById("strumento").value;
      const cfg = CONFIG_CAMPI[s];
      document.getElementById("lbl1").innerText = cfg[0];

      const box2 = document.getElementById("box2");
      const inp2 = document.getElementById("val2");
      if (cfg[1]) { box2.style.display = "block"; document.getElementById("lbl2").innerText = cfg[1]; inp2.required = true; }
      else { box2.style.display = "none"; inp2.required = false; }

      const box3 = document.getElementById("box3");
      const inp3 = document.getElementById("val3");
      if (cfg[2]) { box3.style.display = "block"; document.getElementById("lbl3").innerText = cfg[2]; inp3.required = true; }
      else { box3.style.display = "none"; inp3.required = false; }
    }

    function openTab(tabName, btn) {
      document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.getElementById(tabName).classList.add("active");
      btn.classList.add("active");
    }

    function filtraFormule() {
      const q = document.getElementById("cercaFormula").value.toLowerCase();
      document.querySelectorAll(".formula-item").forEach(item => {
        item.style.display = item.innerText.toLowerCase().includes(q) ? "block" : "none";
      });
    }

    aggiornaEtichette();
  </script>
</body>
</html>
"""


def calcola_formula(strumento, v1, v2, v3):
    if strumento == "eq2":
        if v1 == 0:
            return "Con a = 0 non è di 2° grado." if v2 == 0 else f"Equazione 1° grado: x = {-v3/v2:g}"
        delta = v2**2 - 4 * v1 * v3
        testo = f"Equazione: {v1:g}x² + ({v2:g})x + ({v3:g}) = 0\nΔ = b² - 4ac = {delta:g}\n"
        if delta > 0:
            x1 = (-v2 - math.sqrt(delta)) / (2 * v1)
            x2 = (-v2 + math.sqrt(delta)) / (2 * v1)
            return testo + f"Due soluzioni reali: x₁ = {x1:g},  x₂ = {x2:g}"
        elif delta == 0:
            x = -v2 / (2 * v1)
            return testo + f"Una soluzione reale doppia: x = {x:g}"
        return testo + "Nessuna soluzione reale (Δ < 0)."

    if strumento == "pitagora":
        c = math.hypot(v1, v2)
        return f"c = √({v1:g}² + {v2:g}²) = √({v1**2 + v2**2:g}) = {c:g}"

    if strumento == "cerchio":
        if v1 < 0:
            return "Il raggio non può essere negativo."
        return f"Raggio r = {v1:g}\nCirconferenza = 2πr = {2 * math.pi * v1:g}\nArea = πr² = {math.pi * v1**2:g}"

    if strumento == "log":
        if v1 <= 0 or v2 <= 0 or v2 == 1:
            return "Servono x > 0, base b > 0 e b ≠ 1."
        res = math.log(v1, v2)
        return f"log_{v2:g}({v1:g}) = {res:g}  (infatti {v2:g}^{res:g} ≈ {v1:g})"

    if strumento == "mrua":
        s = v1 * v3 + 0.5 * v2 * (v3**2)
        vf = v1 + v2 * v3
        return f"Spazio percorso s = {v1:g}·{v3:g} + ½·{v2:g}·{v3:g}² = {s:g} m\nVelocità finale v = {vf:g} m/s"

    if strumento == "newton":
        return f"Forza risultante F = m · a = {v1:g} · {v2:g} = {v1 * v2:g} N"

    if strumento == "cinetica":
        return f"Energia cinetica K = ½ · m · v² = 0,5 · {v1:g} · {v2:g}² = {0.5 * v1 * (v2**2):g} J"

    if strumento == "ohm":
        if v2 == 0:
            return "La resistenza R non può essere 0."
        i = v1 / v2
        p = v1 * i
        return f"Corrente I = V / R = {v1:g} / {v2:g} = {i:g} A\nPotenza P = V · I = {p:g} W"

    if strumento == "gas":
        if v3 == 0:
            return "Il volume V non può essere 0."
        r_gas = 8.314
        p = (v1 * r_gas * v2) / v3
        return f"Pressione P = (n·R·T)/V = ({v1:g} · 8,314 · {v2:g}) / {v3:g} = {p:g} Pa"

    if strumento == "densita":
        if v2 == 0:
            return "Il volume non può essere 0."
        return f"Densità d = m / V = {v1:g} / {v2:g} = {v1 / v2:g}"

    if strumento == "moli":
        if v2 <= 0:
            return "La massa molare deve essere maggiore di 0."
        n = v1 / v2
        particelle = n * 6.022e23
        return f"Moli n = {v1:g} / {v2:g} = {n:g} mol\nNumero di particelle ≈ {particelle:.3e}"

    if strumento == "ph":
        if v1 <= 0:
            return "La concentrazione [H₃O⁺] deve essere > 0."
        ph = -math.log10(v1)
        natura = "acida" if ph < 7 else ("neutra" if math.isclose(ph, 7, abs_tol=1e-6) else "basica")
        return f"pH = -log₁₀({v1:g}) = {ph:.2f}  (soluzione {natura}, pOH = {14 - ph:.2f})"

    return "Strumento non riconosciuto."


@app.route("/", methods=["GET", "POST"])
def home():
    tab = "calcolatori"
    strumento = "eq2"
    val1, val2, val3 = "", "", ""
    esito_calcolo = None
    esito_quiz = None
    quiz_corretto = False
    idx_domanda = random.randrange(len(DOMANDE_QUIZ))

    if request.method == "POST":
        azione = request.form.get("azione")
        tab = request.form.get("tab", "calcolatori")

        if azione == "calcola":
            strumento = request.form.get("strumento", "eq2")
            val1 = request.form.get("val1", "")
            val2 = request.form.get("val2", "")
            val3 = request.form.get("val3", "")
            try:
                v1 = float(val1)
                v2 = float(val2) if val2 != "" else 0.0
                v3 = float(val3) if val3 != "" else 0.0
                esito_calcolo = calcola_formula(strumento, v1, v2, v3)
            except ValueError:
                esito_calcolo = "Inserisci valori numerici validi."

        elif azione == "quiz":
            idx_domanda = int(request.form.get("idx_domanda", 0)) % len(DOMANDE_QUIZ)
            risposta_utente = request.form.get("risposta_utente", "").strip().replace(",", ".")
            corretta = DOMANDE_QUIZ[idx_domanda]["risposta"]
            spiegazione = DOMANDE_QUIZ[idx_domanda]["spiegazione"]
            if risposta_utente == corretta:
                quiz_corretto = True
                esito_quiz = f"Corretto! {spiegazione}"
            else:
                quiz_corretto = False
                esito_quiz = f"Risposta errata (quella corretta era {corretta}). {spiegazione}"
            idx_domanda = (idx_domanda + 1) % len(DOMANDE_QUIZ)

    return render_template_string(
        HTML_TEMPLATE,
        tab=tab,
        strumento=strumento,
        val1=val1,
        val2=val2,
        val3=val3,
        esito_calcolo=esito_calcolo,
        formulario=FORMULARIO,
        domanda=DOMANDE_QUIZ[idx_domanda],
        idx_domanda=idx_domanda,
        esito_quiz=esito_quiz,
        quiz_corretto=quiz_corretto,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)