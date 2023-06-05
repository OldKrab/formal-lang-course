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
{\text{fa : FA}}
{\text{ДОСТИЖИМЫЕ ИЗ fa : Set}}$$

$$\frac
{\text{fa : Set \quad func : Lambda}}
{\text{ОТОБРАЗИТЬ func fa : Set}}$$

$$\frac
{\text{fa : Set \quad func : Lambda}}
{\text{ФИЛЬТРОВАТЬ func fa : Set}}$$

$$\frac
{\text{x : FA \quad y : FA}}
{\text{x И y : FA}}$$

$$\frac
{\text{x : FA \quad y : FA}}
{\text{x ИЛИ y : FA}}$$

$$\frac
{\text{x : FA}}
{\text{x* : FA}}$$

$$\frac
{\text{x : FA \quad y : FA}}
{\text{x ++ y : FA}}$$

$$\frac
{\text{x : RSM \quad y : RSM}}
{\text{x ИЛИ y : RSM}}$$

$$\frac
{\text{x : RSM \quad y : RSM}}
{\text{x ++ y : RSM}}$$

$$\frac
{\text{x : RSM}}
{\text{x* : RSM}}$$

$$\frac
{\text{x : T \quad s : Set}}
{\text{x ПРИНАДЛЕЖИТ s : Bool}}$$

$$\frac
{\text{x : Set \quad s : Set}}
{\text{x ПОДМНОЖЕСТВО ДЛЯ s : Bool}}$$
