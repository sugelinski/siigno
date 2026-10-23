# Descubra seu signo

Página web em que o usuário informa a data de nascimento e é levado a uma página com as principais informações do seu signo.

## Estrutura

```
descubra-seu-signo/
├── index.html          # formulário (página inicial)
├── signo.html          # resultado
├── css/style.css
├── js/index.js         # validação, roda animada e redirecionamento
├── js/signo.js         # consulta a API e preenche a página
├── database/
│   ├── init_db.py      # cria o banco com os 12 signos
│   └── signos.db       # banco SQLite (já gerado)
└── server.py           # servidor + API  GET /api/signo?data=AAAA-MM-DD
```

## Como rodar

Requer Python 3.8+ (nenhuma biblioteca externa).

```bash
python server.py
```

Abra http://localhost:8000

Para recriar o banco do zero: `python database/init_db.py`
