# Gerador de Agenda Telefónica a partir de Exportações .xls/.xlsx

Script em Python que consolida centenas/milhares de ficheiros
`.xls`/`.xlsx` (exportações de encomendas) numa única agenda
telefónica em Excel, com Nome, Morada e Contacto.

## O que faz

1. Percorre uma pasta (e opcionalmente subpastas) à procura de
   ficheiros `.xls`/`.xlsx`.
2. Lê cada ficheiro e extrai as colunas relevantes (destinatário,
   morada e telefone).
3. Junta tudo numa única tabela.
4. Remove linhas sem nome e contactos duplicados.
5. Ordena por nome e grava o resultado num único `.xlsx` final.

## Requisitos

- Python 3.9+
- [pandas](https://pandas.pydata.org/)
- Um engine de leitura Excel: `openpyxl` (para `.xlsx`) e/ou `xlrd`
  (para `.xls` antigos)

Instalação:

```bash
pip install pandas openpyxl xlrd
```

## Estrutura esperada

```
.
├── gerar_agenda.py
└── arquivos_xls/              # pasta de entrada (configurável)
    ├── encomenda_001.xlsx
    ├── encomenda_002.xls
    └── ...
```

## Configuração

Todas as opções ficam no topo do script, sem precisar mexer no resto
do código:

```python
PASTA_ENTRADA = "./arquivos_xls"    # onde estão os ficheiros de origem
SAIDA = "agenda_telefonica.xlsx"    # nome do ficheiro final
BUSCAR_SUBPASTAS = True             # True = também procura dentro de subpastas
```

### Mapeamento de colunas

O script espera que os ficheiros de origem tenham estas colunas
(ajuste os nomes conforme o seu ficheiro real):

```python
COL_NOME = "Destinatário"
COL_MORADA_PARTES = ["Direcção destino", "Localidade destino", "CP destinatário"]
COL_CONTACTO = "Telefone destinatário"
```

- `COL_NOME`: coluna usada como nome do contacto (**obrigatória** —
  ficheiros sem essa coluna são ignorados com aviso).
- `COL_MORADA_PARTES`: lista de colunas que são concatenadas para
  formar a morada completa (só entram as partes que existirem e não
  estiverem vazias).
- `COL_CONTACTO`: coluna do telefone (opcional — se não existir, fica
  em branco).

## Como usar

```bash
python gerar_agenda.py
```

Saída no terminal:

```
Encontrados 1342 arquivos em 'arquivos_xls'.
Processados 100/1342...
Processados 200/1342...
...
Removidos 87 duplicados (mesmo Nome + Contacto).
Agenda telefónica salva em: agenda_telefonica.xlsx (1189 contactos)
```

## Regras de limpeza aplicadas

- **Ficheiros inválidos ou ilegíveis**: são ignorados com aviso no
  terminal (`[AVISO] Falhou ao ler ...`), o script não para.
- **Ficheiros sem a coluna de nome**: ignorados com aviso.
- **Linhas sem nome** (vazio ou `"nan"`): removidas da agenda final.
- **Duplicados**: uma linha é considerada duplicada se tiver o mesmo
  par **Nome + Contacto** que outra já processada; fica só a
  primeira ocorrência.
- **Ordenação**: resultado final ordenado alfabeticamente por Nome.

## ⚠️ Limitações e pontos de atenção

- **Campo Email não é extraído**: o docstring do script menciona
  "Email" como um dos campos da agenda, mas o código atual **não lê
  nem inclui essa coluna** em lugar nenhum. Se precisar dela, é
  necessário adicionar uma `COL_EMAIL` e incluí-la em
  `processar_arquivo()`.
- **Deduplicação por Nome+Contacto**: se duas pessoas com o mesmo
  nome tiverem números diferentes, ambas ficam na agenda (o que é
  esperado); mas se o mesmo contacto aparecer com nomes escritos de
  forma ligeiramente diferente (ex: com/sem acento, maiúsculas), não
  é tratado como duplicado.
- **Morada depende dos nomes exatos das colunas**: se os ficheiros de
  origem tiverem variações no nome das colunas (ex: "Direção" vs
  "Direcção"), essas linhas ficam sem aquela parte da morada,
  silenciosamente.
- **Desempenho**: para milhares de ficheiros, a leitura com
  `pd.read_excel` é o gargalo — é normal o processo demorar alguns
  minutos. Não há paralelização.
- **`.xls` (formato antigo)**: exige o pacote `xlrd` instalado
  separadamente; sem ele, ficheiros `.xls` vão falhar na leitura.

## Possíveis melhorias futuras

- Adicionar extração do campo Email.
- Normalizar nomes (remover acentos/maiúsculas) antes de comparar
  duplicados.
- Gerar um relatório separado dos ficheiros que falharam ou foram
  ignorados, em vez de só imprimir no terminal.
- Paralelizar a leitura dos ficheiros para acelerar em volumes muito
  grandes.
