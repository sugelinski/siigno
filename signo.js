/* Página de resultado: busca o signo no servidor (SQLite) e preenche a tela */

const MESES = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
const TEXTO = "\uFE0E";
const $ = (id) => document.getElementById(id);

function dataPorExtenso(iso) {
  const [a, m, d] = iso.split("-").map(Number);
  return `Nascimento: ${d} de ${MESES[m - 1]} de ${a}`;
}

function preencherLista(id, texto) {
  const ul = $(id);
  texto.split(",").map(t => t.trim()).filter(Boolean).forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    ul.appendChild(li);
  });
}

function falhar(msg) {
  const estado = $("estado");
  estado.textContent = msg;
  estado.classList.add("erro-estado");
}

async function carregar() {
  const data = new URLSearchParams(window.location.search).get("data");
  if (!data) return falhar("Nenhuma data informada. Volte e preencha sua data de nascimento.");

  try {
    const resp = await fetch(`/api/signo?data=${encodeURIComponent(data)}`);
    const s = await resp.json();
    if (!resp.ok) return falhar(s.erro || "Não foi possível consultar o signo.");

    document.title = `${s.nome} — Seu signo`;
    document.documentElement.style.setProperty("--accent", s.cor_hex);

    $("simbolo").textContent = s.simbolo + TEXTO;
    $("nascimento").textContent = dataPorExtenso(data);
    $("nome").textContent = s.nome;
    $("periodo").textContent = s.periodo;
    $("descricao").textContent = s.descricao;
    $("elemento").textContent = s.elemento;
    $("modalidade").textContent = s.modalidade;
    $("regente").textContent = s.regente;
    $("cor").textContent = s.cor;
    $("amostra").style.background = s.cor_hex;
    $("pedra").textContent = s.pedra;
    $("dia").textContent = s.dia_semana;
    $("numeros").textContent = s.numeros;
    preencherLista("qualidades", s.qualidades);
    preencherLista("desafios", s.desafios);
    preencherLista("compatibilidade", s.compatibilidade);

    $("estado").hidden = true;
    $("signo").hidden = false;
  } catch {
    falhar("Não foi possível conectar ao servidor. Inicie-o com: python server.py");
  }
}

carregar();
