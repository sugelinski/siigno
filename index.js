/* Página inicial: valida a data, anima a roda e redireciona para signo.html */

// Usado apenas para a pré-visualização na roda. A consulta oficial é feita no banco (SQLite).
const SIGNOS = [
  { nome: "Áries",       simbolo: "♈", ini: 321,  fim: 419 },
  { nome: "Touro",       simbolo: "♉", ini: 420,  fim: 520 },
  { nome: "Gêmeos",      simbolo: "♊", ini: 521,  fim: 620 },
  { nome: "Câncer",      simbolo: "♋", ini: 621,  fim: 722 },
  { nome: "Leão",        simbolo: "♌", ini: 723,  fim: 822 },
  { nome: "Virgem",      simbolo: "♍", ini: 823,  fim: 922 },
  { nome: "Libra",       simbolo: "♎", ini: 923,  fim: 1022 },
  { nome: "Escorpião",   simbolo: "♏", ini: 1023, fim: 1121 },
  { nome: "Sagitário",   simbolo: "♐", ini: 1122, fim: 1221 },
  { nome: "Capricórnio", simbolo: "♑", ini: 1222, fim: 119 },
  { nome: "Aquário",     simbolo: "♒", ini: 120,  fim: 218 },
  { nome: "Peixes",      simbolo: "♓", ini: 219,  fim: 320 },
];
const TEXTO = "\uFE0E"; // força o símbolo em modo texto (não emoji)

const form   = document.getElementById("form-signo");
const campo  = document.getElementById("data");
const erro   = document.getElementById("erro");
const roda   = document.getElementById("roda");
const anel   = document.getElementById("roda-anel");
const centroSimbolo = document.getElementById("centro-simbolo");
const centroNome    = document.getElementById("centro-nome");

// Data máxima = hoje (no fuso local)
const hoje = new Date();
const hojeISO = `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, "0")}-${String(hoje.getDate()).padStart(2, "0")}`;
campo.max = hojeISO;

// Monta os 12 símbolos ao redor da roda
SIGNOS.forEach((s, i) => {
  const g = document.createElement("div");
  g.className = "glifo";
  g.style.setProperty("--a", `${i * 30}deg`);
  g.title = s.nome;
  const span = document.createElement("span");
  span.textContent = s.simbolo + TEXTO;
  g.appendChild(span);
  anel.appendChild(g);
});

function indiceDoSigno(dataISO) {
  const [, m, d] = dataISO.split("-").map(Number);
  const md = m * 100 + d;
  return SIGNOS.findIndex(s =>
    s.ini <= s.fim ? md >= s.ini && md <= s.fim : md >= s.ini || md <= s.fim
  );
}

function dataValida(valor) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(valor)) return "Informe sua data de nascimento.";
  const [a, m, d] = valor.split("-").map(Number);
  const dt = new Date(a, m - 1, d);
  if (dt.getFullYear() !== a || dt.getMonth() !== m - 1 || dt.getDate() !== d) return "Essa data não existe. Confira o dia e o mês.";
  if (a < 1900) return "Use uma data a partir de 1900.";
  if (valor > hojeISO) return "A data de nascimento não pode estar no futuro.";
  return "";
}

function mostrarErro(msg) {
  erro.textContent = msg;
  campo.setAttribute("aria-invalid", msg ? "true" : "false");
}

// Ao escolher a data, a roda gira até o signo correspondente
campo.addEventListener("input", () => {
  if (dataValida(campo.value)) return;
  mostrarErro("");
  const i = indiceDoSigno(campo.value);
  roda.style.setProperty("--rot", `${-i * 30}deg`);
  anel.style.setProperty("--rot", `${-i * 30}deg`);
  anel.querySelectorAll(".glifo").forEach((g, idx) => {
    g.classList.toggle("ativo", idx === i);
    g.firstChild.style.setProperty("--rot", `${-i * 30}deg`);
  });
  centroSimbolo.textContent = SIGNOS[i].simbolo + TEXTO;
  centroNome.textContent = SIGNOS[i].nome;
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const msg = dataValida(campo.value);
  if (msg) {
    mostrarErro(msg);
    campo.focus();
    return;
  }
  window.location.href = `signo.html?data=${encodeURIComponent(campo.value)}`;
});
