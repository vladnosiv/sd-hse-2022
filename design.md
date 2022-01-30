## Домашняя работа 1. Архитектура CLI

### Участники группы

* Носивской Владислав
* Саврасов Михаил
* Левин Лев
* Широков Кирилл

### Структурная диаграмма

TODO: Вставить картинку новой диаграммы

### Правила для лексера и парсера

В этой части будут расписаны формальные правила для лексера и парсера,
которые программист перенесет в код (как именно -- будет расписано
позднее)

Синтаксис отсылается к использованию библиотеки `yecc` (`yacc` для Erlang)

Есть отдельный парсер для команд и для аргументов. Это сделано, чтобы
передавать в парсер аргументов вывод команд при перебрасывании вывода в пайпе.


* Лексер

```
Definitions.

WORD = [_a-zA-Z][_a-zA-Z0-9]*
WHITESPACE = [\s\t\n\r]

Rules.

|             : pipe.
=             : assign.
"             : double_quote.
[^"]*         : double_quote_interior.
'             : single_quote.
[^']*         : single_quote_interior.
{WORD}        : word.
{WHITESPACE}+ : skip_token.
```

* Парсер команд (Оставляет аргументы как есть)

```
Nontermials command, assignment, atom, function, var_name.
Terminals pipe, word, args.
Rootsymbol command.

Left pipe. (Левоасс. оператор)

command -> command pipe command.
command -> assignment.
command -> atom.

assignment -> var_name assign word.

atom -> function.
atom -> function args.

var_name -> word.
function -> word.
```

* Парсер аргументов

```
Nonterminals args.
Terminals double_quote, double_quote_interior, single_quote, single_quote_interior.
Rootsymbol args.

args -> arg.
args -> arg args.

arg -> word.
arg -> double_quote double_quote_interior double_quote.
arg -> single_quote single_quote_interior single_quote.
```



















