grammar Language;

program: statement? ('\n'+ statement?)* EOF;
statement: bind | print;

bind: 'ПУСТЬ' var '=' expr;
print: 'ВЫВЕСТИ' expr;

expr:
	'(' expr ')'
	| var
	| val
	| 'УСТАНОВИТЬ' expr 'КАК' ('СТАРТОВЫЕ' | 'ФИНАЛЬНЫЕ') 'ДЛЯ' expr
	| 'ДОБАВИТЬ' expr 'К' ('СТАРТОВЫМ' | 'ФИНАЛЬНЫМ') 'ДЛЯ' expr
	| ('СТАРТОВЫЕ' | 'ФИНАЛЬНЫЕ' | 'ВЕРШИНЫ' | 'РЕБРА' | 'МЕТКИ' | 'ДОСТИЖИМЫЕ') 'ИЗ' expr
	| ('ОТОБРАЗИТЬ' | 'ФИЛЬТРОВАТЬ') lambda expr
	| 'ЗАГРУЗИТЬ' 'ГРАФ' 'ИЗ' STR
	| expr 'И' expr // пересечение языков
	| expr expr // конкатенация языков
	| expr 'ИЛИ' expr // объединение языков
	| expr '*' // замыкание языков
	| expr 'ПРИНАДЛЕЖИТ' expr // вхождение в множество
	| expr 'ПОДМНОЖЕСТВО' 'ДЛЯ' expr // подмножество другого множества
	| expr '==' expr
	| expr '!=' expr
	| 'НЕ' expr; // отрицание условия

lambda: '(' lambda ')' | pattern (',' pattern)* '->' expr;
pattern: var | '(' pattern (',' pattern)+ ')';

var: ID;
val: simple_val | set_val | tuple_val;
simple_val: INT | STR;

tuple_val: '(' tuple_elem (',' tuple_elem)+ ')';
tuple_elem: simple_val | tuple_val;

set_val: '{' set_elem (',' set_elem)* '}';
set_elem: simple_val | tuple_val | set_elem_interval;
set_elem_interval: INT '..' INT;

ID: [а-яА-Яa-zA-Z_][а-яА-Яa-zA-Z0-9_']*;
INT: [0-9]+;
STR: '"' (~["\\] | '\\' .)* '"';

COMMENT: ('//' ~[\n]* | '/*' .*? '*/') -> skip;
WS: [ \t\r]+ -> skip;