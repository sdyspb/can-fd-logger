# Правило для Cline: подключение к git@github.com:sdyspb/can-fd-logger.git

## Основные параметры репозитория

- **Remote name:** `origin`
- **Remote URL (SSH):** `git@github.com:sdyspb/can-fd-logger.git`
- **Основная ветка:** `main`

> ⚠️ **Предупреждение:** использовать только SSH-подключение. Никогда не переключаться на HTTPS-URL без явного указания пользователя.

## Проверка текущего состояния

Перед любой git-операцией Cline обязан выполнить:

```bash
git status
git remote -v
```

Ожидаемый вывод для remote:

```bash
origin  git@github.com:sdyspb/can-fd-logger.git (fetch)
origin  git@github.com:sdyspb/can-fd-logger.git (push)
```

## Инициализация репозитория

Если git ещё не инициализирован или remote отсутствует:

```bash
git init
git remote remove origin 2>/dev/null || true
git remote add origin git@github.com:sdyspb/can-fd-logger.git
git branch -M main
```

Если на GitHub уже есть коммиты:

```bash
git pull origin main --allow-unrelated-histories
```

## Первый push

```bash
git add .
git commit -m "chore: initial commit"
git push -u origin main
```

## Регламент работы с ветками

1. Основная ветка — `main`.
2. Ветки для задач:
   - `feature/<name>` — новые фичи
   - `fix/<name>` — исправления
3. Мерж в `main` — только через Pull Request, если не указано иное.

## Правила коммитов

- Формат сообщения: `<type>: <short description>`
- Допустимые типы:
  - `feat`
  - `fix`
  - `docs`
  - `refactor`
  - `test`
  - `chore`
- Запрещено коммитить:
  - секреты и токены
  - `.env` и аналогичные файлы
  - артефакты сборки
  - временные файлы

## Push и синхронизация

Перед каждым push:

```bash
git pull --rebase origin main
git push -u origin main
```

## Запрещённые действия без подтверждения пользователя

> ⚠️ **Предупреждение:** следующие команды выполняются только после явного согласия пользователя.

- `git push --force` / `git push -f`
- `git reset --hard` на удалённых ветках
- удаление remote `origin`
- изменение URL remote на другой репозиторий
- `git rebase` с перезаписью уже опубликованной истории

## Обработка конфликтов

> ⚠️ **Предупреждение:** при конфликтах merge/rebase запрещено автоматически выполнять `--abort`.

Порядок действий:

1. Показать пользователю список конфликтующих файлов.
2. Запросить решение по каждому конфликту.
3. Дождаться подтверждения перед продолжением операции.

## Проверка SSH-доступа

```bash
ssh -T git@github.com
```

Если ключ не настроен — сообщить пользователю и **не пытаться** переходить на HTTPS.

## Рекомендуемый `.gitignore`

Для проекта can-fd-logger рекомендуется исключить:

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
build/
dist/
*.egg-info/
*.log
*.bin
*.blf
.env
.vscode/
.idea/
```