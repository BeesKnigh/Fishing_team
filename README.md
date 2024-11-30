![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)

# Контроль и управление изменениями в тендерных закупках
## Описание проекта

Инструмент на базе ИИ для выявления аномальных паттернов в финансовом поведении.

# Метрики качества решения
## Описание метрик

1. Метрика MSE (Mean Squared Error) Формула для вычисления MSE:

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$ 

# Инструкция по работе с проектом
## Создание виртуальной среды и работа с ноутбуками

Для подготовки окружения для работы с модулями и ноутбуками выполните следующие команды, находясь в корневой директории проекта:

```bash
# команды создания виртуального окружения
python3 -m venv .venv

# активация виртуального окружения
## Windows
.venv\Scripts\activate

## macOS & Linux
source .venv/bin/activate

# установка необходимых библиотек в виртуальное окружение
pip install -r requirements.txt
```

## Режим разработки

Режим разработки ведется в следующих Jupyter Notebook'ах:
- `ds_creation.ipynb`
   - Представление текстовых .docx-файлов заключений типа HMI и SSTS в виде датасета, хранящийся в `data\raw_data`
   - Формирование целевого признака на основе размеченных данных из `data\raw_data\train_data_markup.xlsx`
  
# Структура проекта

```bash
atom-compliance-ml
├─ .gitignore
├─ data                          # Данные для обучения и тестирования
│  ├─ dataset.csv
├─ logs                          # Логи инференса (FULL LAUNCH)
├─ frontend                      # Весь фронтенд проекта
├─ backend                       # Весь бекенд проекта
│  ├─ src                       
└─ model
   ├─ src
   │  ├─ notebooks   
   │  ├─ modules
   │  ├─ scripts 
   ├─ eda                             # Ноутбуки для обучения и экспериментов, модули
   ├─ models                    # Функциональная и бизнес логика, используемая во всех ноутбуках  

```

# Контакты
Если у вас есть вопросы или предложения по проекту, пожалуйста, свяжитесь с нами:
- Александр, DS, TL
   - @BeesKnights
- Анна, Frontend
   - @mbhopper
- Денис, Backend
   - @Denbay0
- Варвара, Designer
   - @shterenfeld



![alt text](team_logov2.png)

