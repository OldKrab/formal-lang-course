## Правила вывода типов

$$\frac
{\text{x : str}}
{\text{ЗАГРУЗИТЬ x : FA}}$$

$$\frac
{\text{x : str}}
{\text{КА ИЗ x : FA}}$$

$$\frac
{\text{x : FA}}
{\text{РКА ИЗ x : RSM}}$$

$$\frac
{\text{x : Set \quad fa: FA}}
{\text{УСТАНОВИТЬ x КАК СТАРТОВЫЕ ДЛЯ fa : FA}}$$

$$\frac
{\text{x : Set \quad fa: FA}}
{\text{УСТАНОВИТЬ x КАК ФИНАЛЬНЫЕ ДЛЯ fa : FA}}$$

$$\frac
{\text{x : Set \quad fa: FA}}
{\text{ДОБАВИТЬ x К СТАРТОВЫМ ДЛЯ fa : FA}}$$

$$\frac
{\text{x : Set \quad fa: FA}}
{\text{ДОБАВИТЬ x К ФИНАЛЬНЫМ ДЛЯ fa : FA}}$$

$$\frac
{\text{fa : FA}}
{\text{СТАРТОВЫЕ ИЗ fa : Set}}$$

$$\frac
{\text{fa : FA}}
{\text{ФИНАЛЬНЫЕ ИЗ fa : Set}}$$

$$\frac
{\text{fa : FA}}
{\text{ВЕРШИНЫ ИЗ fa : Set}}$$

$$\frac
{\text{fa : FA}}
{\text{РЕБРА ИЗ fa : Set}}$$

$$\frac
{\text{fa : FA}}
{\text{МЕТКИ ИЗ fa : Set}}$$

$$\frac
{\text{rsm : RSM}}
{\text{СТАРТОВЫЕ ИЗ rsm : Set}}$$

$$\frac
{\text{rsm : RSM}}
{\text{ФИНАЛЬНЫЕ ИЗ rsm : Set}}$$

$$\frac
{\text{rsm : RSM}}
{\text{ВЕРШИНЫ ИЗ rsm : Set}}$$

$$\frac
{\text{rsm : RSM}}
{\text{РЕБРА ИЗ rsm : Set}}$$

$$\frac
{\text{rsm : RSM}}
{\text{МЕТКИ ИЗ rsm : Set}}$$

$$\frac
{\text{fa : FA \quad regex: str}}
{\text{ДОСТИЖИМЫЕ ИЗ fa С ОГРАНИЧЕНИЯМИ regex: Set}}$$


$$\frac
{\text{s : Set \quad func : Lambda}}
{\text{ОТОБРАЗИТЬ func s : Set}}$$

$$\frac
{\text{s : Set \quad func : Lambda}}
{\text{ФИЛЬТРОВАТЬ func s : Set}}$$

$$\frac
{\text{x : FA \quad y : FA}}
{\text{x И y : FA}}$$

$$\frac
{\text{x : FA \quad y : FA}}
{\text{x ИЛИ y : FA}}$$

$$\frac
{\text{x : str \quad y : str}}
{\text{x ИЛИ y : str}}$$

$$\frac
{\text{x : FA}}
{\text{x* : FA}}$$

$$\frac
{\text{x : str}}
{\text{x* : str}}$$

$$\frac
{\text{x : FA \quad y : FA}}
{\text{x ++ y : FA}}$$

$$\frac
{\text{x : str \quad y : str}}
{\text{x ++ y : str}}$$

$$\frac
{\text{x : Int \quad y : Int}}
{\text{x == y : Int}}$$

$$\frac
{\text{x : Str \quad y : Str}}
{\text{x == y : Int}}$$

$$\frac
{\text{x : Set \quad y : Set}}
{\text{x == y : Int}}$$

$$\frac
{\text{x : Int}}
{\text{НЕ x : Int}}$$

$$\frac
{\text{x : int \quad y : int}}
{\text{x ИЛИ y : int}}$$

$$\frac
{\text{x : int \quad y : int}}
{\text{x И y : int}}$$

$$\frac
{\text{x : T \quad s : Set}}
{\text{x ПРИНАДЛЕЖИТ s : Int}}$$

$$\frac
{\text{x : Set \quad s : Set}}
{\text{x ПОДМНОЖЕСТВО ДЛЯ s : Int}}$$


## Типизация стандартных функций

* print принимает str, int, Set или Tuple
