"""Cria o banco SQLite (signos.db) com os 12 signos do zodíaco.

Uso:  python database/init_db.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("signos.db")

SCHEMA = """
DROP TABLE IF EXISTS signos;
CREATE TABLE signos (
    id            INTEGER PRIMARY KEY,
    nome          TEXT NOT NULL UNIQUE,
    simbolo       TEXT NOT NULL,
    inicio_md     INTEGER NOT NULL,   -- mês*100 + dia (ex.: 21/03 -> 321)
    fim_md        INTEGER NOT NULL,
    periodo       TEXT NOT NULL,
    elemento      TEXT NOT NULL,
    modalidade    TEXT NOT NULL,
    regente       TEXT NOT NULL,
    cor           TEXT NOT NULL,
    cor_hex       TEXT NOT NULL,
    pedra         TEXT NOT NULL,
    dia_semana    TEXT NOT NULL,
    numeros       TEXT NOT NULL,
    compatibilidade TEXT NOT NULL,
    descricao     TEXT NOT NULL,
    qualidades    TEXT NOT NULL,
    desafios      TEXT NOT NULL
);
CREATE INDEX idx_signos_periodo ON signos (inicio_md, fim_md);

-- Registro das consultas (não é apagado ao recriar os signos)
CREATE TABLE IF NOT EXISTS consultas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    data_nascimento TEXT NOT NULL,
    signo_id        INTEGER NOT NULL REFERENCES signos(id),
    consultado_em   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
    ip              TEXT
);
"""

SIGNOS = [
 ("Áries","♈",321,419,"21 de março a 19 de abril","Fogo","Cardinal","Marte","Vermelho","#E5594F","Diamante","Terça-feira","1, 9, 17","Leão, Sagitário, Gêmeos",
  "O primeiro signo do zodíaco é movido por iniciativa e coragem. Arianos gostam de começar coisas novas, enfrentar desafios de frente e liderar pelo exemplo.",
  "Coragem, determinação, entusiasmo, honestidade","Impaciência, impulsividade, dificuldade em ouvir"),
 ("Touro","♉",420,520,"20 de abril a 20 de maio","Terra","Fixo","Vênus","Verde","#6FA86B","Esmeralda","Sexta-feira","2, 6, 15","Virgem, Capricórnio, Câncer",
  "Taurinos valorizam estabilidade, conforto e prazeres simples. São persistentes, leais e constroem a vida com paciência, um passo de cada vez.",
  "Lealdade, paciência, praticidade, sensualidade","Teimosia, apego excessivo, resistência a mudanças"),
 ("Gêmeos","♊",521,620,"21 de maio a 20 de junho","Ar","Mutável","Mercúrio","Amarelo","#E3C94F","Ágata","Quarta-feira","3, 5, 14","Libra, Aquário, Áries",
  "Curiosos e comunicativos, geminianos vivem de ideias, conversas e novidades. Adaptam-se com facilidade e transitam bem entre grupos diferentes.",
  "Curiosidade, adaptabilidade, bom humor, comunicação","Dispersão, inconstância, ansiedade"),
 ("Câncer","♋",621,722,"21 de junho a 22 de julho","Água","Cardinal","Lua","Prata","#B8C4D6","Pérola","Segunda-feira","2, 7, 11","Escorpião, Peixes, Touro",
  "Cancerianos têm forte ligação com a família, a casa e as memórias. São protetores, intuitivos e percebem o que os outros sentem antes de qualquer palavra.",
  "Empatia, cuidado, intuição, memória afetiva","Sensibilidade excessiva, apego ao passado, tendência a se retrair"),
 ("Leão","♌",723,822,"23 de julho a 22 de agosto","Fogo","Fixo","Sol","Dourado","#E8A33D","Rubi","Domingo","1, 4, 19","Áries, Sagitário, Libra",
  "Leoninos têm presença marcante e gostam de brilhar. São generosos, criativos e protegem quem amam com uma lealdade quase teatral.",
  "Generosidade, carisma, criatividade, confiança","Vaidade, orgulho, necessidade de reconhecimento"),
 ("Virgem","♍",823,922,"23 de agosto a 22 de setembro","Terra","Mutável","Mercúrio","Verde-oliva","#9AA56A","Safira","Quarta-feira","5, 14, 23","Touro, Capricórnio, Câncer",
  "Virginianos observam os detalhes e gostam de tornar as coisas melhores. São organizados, analíticos e mostram afeto ajudando de forma concreta.",
  "Organização, senso crítico, dedicação, prestatividade","Perfeccionismo, autocrítica, preocupação em excesso"),
 ("Libra","♎",923,1022,"23 de setembro a 22 de outubro","Ar","Cardinal","Vênus","Rosa","#D98CA8","Opala","Sexta-feira","6, 15, 24","Gêmeos, Aquário, Leão",
  "Librianos buscam equilíbrio, beleza e justiça. Gostam de conviver, sabem mediar conflitos e dão importância à harmonia nas relações.",
  "Diplomacia, senso estético, justiça, sociabilidade","Indecisão, evitar conflitos, dependência da aprovação alheia"),
 ("Escorpião","♏",1023,1121,"23 de outubro a 21 de novembro","Água","Fixo","Plutão e Marte","Vinho","#C2425F","Topázio","Terça-feira","8, 11, 18","Câncer, Peixes, Virgem",
  "Escorpianos vivem as emoções com intensidade e vão fundo em tudo o que fazem. São reservados, estratégicos e muito fiéis a quem conquista sua confiança.",
  "Intensidade, foco, lealdade, resiliência","Ciúme, desconfiança, dificuldade em perdoar"),
 ("Sagitário","♐",1122,1221,"22 de novembro a 21 de dezembro","Fogo","Mutável","Júpiter","Roxo","#9C7BD6","Turquesa","Quinta-feira","3, 7, 9","Áries, Leão, Aquário",
  "Sagitarianos são exploradores de espírito. Amam viajar, aprender e discutir ideias grandes, e encaram a vida com otimismo e franqueza.",
  "Otimismo, liberdade, sinceridade, sede de aprender","Falta de tato, inquietação, dificuldade com compromissos"),
 ("Capricórnio","♑",1222,119,"22 de dezembro a 19 de janeiro","Terra","Cardinal","Saturno","Marrom","#A68A6A","Granada","Sábado","4, 8, 13","Touro, Virgem, Escorpião",
  "Capricornianos trabalham com disciplina para alcançar metas de longo prazo. São responsáveis, ambiciosos e têm um humor seco que surpreende.",
  "Disciplina, responsabilidade, ambição, resistência","Rigidez, pessimismo, dificuldade em relaxar"),
 ("Aquário","♒",120,218,"20 de janeiro a 18 de fevereiro","Ar","Fixo","Urano e Saturno","Azul-elétrico","#4FA3E3","Ametista","Sábado","4, 7, 11","Gêmeos, Libra, Sagitário",
  "Aquarianos pensam à frente do seu tempo. São independentes, originais e se importam com causas coletivas, mesmo quando parecem distantes.",
  "Originalidade, independência, visão de futuro, humanitarismo","Distanciamento emocional, teimosia nas ideias, rebeldia por impulso"),
 ("Peixes","♓",219,320,"19 de fevereiro a 20 de março","Água","Mutável","Netuno e Júpiter","Verde-água","#5FB8B0","Água-marinha","Quinta-feira","3, 9, 12","Câncer, Escorpião, Capricórnio",
  "Piscianos são sonhadores, sensíveis e muito criativos. Absorvem o clima ao redor, têm compaixão natural e uma imaginação que raramente descansa.",
  "Compaixão, imaginação, intuição, generosidade","Fuga da realidade, indecisão, deixar-se influenciar"),
]

def main():
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)
    con.executemany(
        """INSERT INTO signos (nome, simbolo, inicio_md, fim_md, periodo, elemento, modalidade,
           regente, cor, cor_hex, pedra, dia_semana, numeros, compatibilidade, descricao,
           qualidades, desafios) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        SIGNOS,
    )
    con.commit()
    con.close()
    print(f"Banco criado em {DB_PATH} com {len(SIGNOS)} signos.")

if __name__ == "__main__":
    main()
