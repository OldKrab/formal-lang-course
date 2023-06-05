grammar Language;

program: statement? ('\n'+ statement?)* EOF;
statement: bind | print;

bind: 'ПУСТЬ' var '=' expr;
print: 'ВЫВЕСТИ' expr;

expr:
	'(' expr ')'													# brackets_expr
	| var															# var_expr
	| val															# val_expr
	| lambda														# lambda_expr
	| 'УСТАНОВИТЬ' what = expr 'КАК' 'СТАРТОВЫЕ' 'ДЛЯ' for = expr	# set_start_expr
	| 'УСТАНОВИТЬ' what = expr 'КАК' 'ФИНАЛЬНЫЕ' 'ДЛЯ' for = expr	# set_final_expr
	| 'ДОБАВИТЬ' what = expr 'К' 'СТАРТОВЫМ' 'ДЛЯ' for = expr		# add_start_expr
	| 'ДОБАВИТЬ' what = expr 'К' 'ФИНАЛЬНЫМ' 'ДЛЯ' for = expr		# add_final_expr
	| 'СТАРТОВЫЕ' 'ИЗ' expr											# start_from_expr
	| 'ФИНАЛЬНЫЕ' 'ИЗ' expr											# final_from_expr
	| 'ВЕРШИНЫ' 'ИЗ' expr											# vertexes_from_expr
	| 'РЕБРА' 'ИЗ' expr												# edges_from_expr
	| 'МЕТКИ' 'ИЗ' expr												# labels_from_expr
	| 'ДОСТИЖИМЫЕ' 'ИЗ' expr										# reach_from_expr
	| 'ОТОБРАЗИТЬ' with = expr what = expr							# map_expr
	| 'ФИЛЬТРОВАТЬ' with = expr what = expr							# filter_expr
	| 'ЗАГРУЗИТЬ' expr												# load_expr
	| expr 'И' expr													# intersect_expr
	| expr '++' expr												# concat_expr
	| expr 'ИЛИ' expr												# union_expr
	| expr '==' expr												# equal_expr
	| expr '!=' expr												# notequal_expr
	| 'НЕ' expr														# not_expr
	| expr '*'														# klein_expr
	| what = expr 'ПРИНАДЛЕЖИТ' to = expr							# in_set_expr
	| what = expr 'ПОДМНОЖЕСТВО' 'ДЛЯ' of = expr					# subset_expr;

lambda: patterns '->' expr;
patterns: pattern (',' pattern)*;
pattern: var | tuple_pattern;
tuple_pattern: '(' pattern (',' pattern)* ')';

var: ID;
val: simple_val | set_val | tuple_val;
simple_val: INT # int_val | STR # str_val;

tuple_val: '(' expr (',' expr)+ ')';

set_val: '{' set_elem (',' set_elem)* '}';
set_elem: expr | set_elem_interval;
set_elem_interval: INT '..' INT;

ID: [а-яА-Яa-zA-Z_][а-яА-Яa-zA-Z0-9_']*;
INT: [0-9]+;
STR: '"' (~["\\] | '\\' .)* '"';

COMMENT: ('//' ~[\n]* | '/*' .*? '*/') -> skip;
WS: [ \t\r]+ -> skip;
