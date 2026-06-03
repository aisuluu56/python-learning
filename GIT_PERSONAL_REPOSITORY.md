# Git. Как отправить клонированный учебный репозиторий в свой личный репозиторий

## Зачем это нужно

Если студент клонировал учебный репозиторий преподавателя, то локальная папка уже связана с удаленным репозиторием. Обычно эта связь называется `origin`.

Проблема в том, что `origin` после клонирования указывает не на личный репозиторий студента, а на исходный учебный репозиторий.

Поэтому перед первой отправкой своих решений нужно проверить, куда Git будет делать `push`.

## Главная идея

У локального репозитория может быть несколько удаленных адресов:

- `origin` - основной удаленный репозиторий, куда обычно отправляют свои коммиты;
- `upstream` - исходный репозиторий преподавателя, из которого можно получать обновления.

Хорошая схема для учебного проекта:

- `origin` указывает на личный репозиторий студента;
- `upstream` указывает на репозиторий преподавателя.

Так студент пушит свои решения к себе, но при необходимости может подтянуть обновления из исходного проекта.

## Шаг 1. Проверить текущий remote

В папке проекта выполните:

```bash
git remote -v
```

Пример вывода после клонирования учебного репозитория:

```bash
origin  https://github.com/teacher/python_syntax_practice.git (fetch)
origin  https://github.com/teacher/python_syntax_practice.git (push)
```

Это значит, что `origin` сейчас указывает на репозиторий преподавателя.

## Шаг 2. Создать личный репозиторий

На GitHub, GitLab или другой платформе создайте новый пустой репозиторий.

Важно:

- не добавляйте `README.md`;
- не добавляйте `.gitignore`;
- не добавляйте лицензию.

Репозиторий должен быть пустым, потому что локальный проект уже содержит файлы и историю коммитов.

Пример адреса личного репозитория:

```bash
https://github.com/student/python_syntax_practice.git
```

## Шаг 3. Сохранить исходный репозиторий как upstream

Чтобы не потерять ссылку на репозиторий преподавателя, можно переименовать текущий `origin` в `upstream`:

```bash
git remote rename origin upstream
```

После этого проверьте:

```bash
git remote -v
```

Теперь должно быть примерно так:

```bash
upstream  https://github.com/teacher/python_syntax_practice.git (fetch)
upstream  https://github.com/teacher/python_syntax_practice.git (push)
```

## Шаг 4. Добавить личный репозиторий как origin

Теперь добавьте личный репозиторий:

```bash
git remote add origin https://github.com/student/python_syntax_practice.git
```

Проверьте результат:

```bash
git remote -v
```

Должно получиться так:

```bash
origin    https://github.com/student/python_syntax_practice.git (fetch)
origin    https://github.com/student/python_syntax_practice.git (push)
upstream  https://github.com/teacher/python_syntax_practice.git (fetch)
upstream  https://github.com/teacher/python_syntax_practice.git (push)
```

Главное: `origin` должен указывать на личный репозиторий студента.

## Шаг 5. Сделать коммит

Перед отправкой изменений проверьте состояние:

```bash
git status
```

Добавьте файлы:

```bash
git add .
```

Создайте коммит:

```bash
git commit -m "Complete practice tasks"
```

Если Git пишет, что нечего коммитить, значит новых изменений пока нет.

## Шаг 6. Отправить проект в личный репозиторий

Сначала узнайте название текущей ветки:

```bash
git branch --show-current
```

Чаще всего ветка называется `main` или `master`.

Если текущая ветка называется `master`, лучше сразу переименовать ее в `main`:

```bash
git branch -M main
```

После этого отправьте ветку `main` в личный репозиторий:

```bash
git push -u origin main
```

Если в вашей группе специально договорились оставлять ветку `master`, тогда можно пушить `master`:

```bash
git push -u origin master
```

Ключ `-u` запоминает связь между локальной веткой и веткой в личном репозитории. После этого следующие отправки можно делать короче:

```bash
git push
```

## Если origin уже был изменен неправильно

Если `origin` уже существует, но указывает не туда, можно заменить адрес:

```bash
git remote set-url origin https://github.com/student/python_syntax_practice.git
```

После этого обязательно проверьте:

```bash
git remote -v
```

## Как потом отправлять новые решения

Обычный цикл работы:

```bash
git status
git add .
git commit -m "Solve lesson tasks"
git push
```

Коммит лучше делать после логически законченного шага: решили тему, закончили этап проекта, исправили ошибку.

## Как подтянуть обновления от преподавателя

Если был добавлен `upstream`, обновления можно получить так:

```bash
git fetch upstream
git pull upstream main
```

Если в исходном репозитории основная ветка называется `master`, используйте:

```bash
git pull upstream master
```

Перед подтягиванием обновлений лучше сохранить свои изменения в коммит.

## Частые ошибки

### Ошибка 1. Push идет в репозиторий преподавателя

Проверьте:

```bash
git remote -v
```

Если `origin` указывает на репозиторий преподавателя, замените его на личный или используйте схему с `upstream`.

### Ошибка 2. Личный репозиторий создан не пустым

Если на GitHub был создан репозиторий с `README.md`, при первом `push` может появиться конфликт историй.

Для учебного сценария проще создать новый пустой репозиторий. Если репозиторий уже создан с файлами, можно удалить его и создать заново пустым.

### Ошибка 3. Не настроены имя и email

Если Git просит указать автора коммитов, выполните:

```bash
git config --global user.name "Student Name"
git config --global user.email "student@example.com"
```

После этого повторите `git commit`.

### Ошибка 4. GitHub не принимает пароль

GitHub не принимает обычный пароль для HTTPS push. Нужно использовать вход через браузер, SSH-ключ или personal access token.

Если не хочется разбираться с токенами, удобный вариант - настроить SSH и использовать SSH-адрес репозитория:

```bash
git remote set-url origin git@github.com:student/python_syntax_practice.git
```

### Ошибка 5. `src refspec main does not match any`

Такая ошибка часто появляется, если локальная ветка называется не `main`.

Проверьте текущую ветку:

```bash
git branch --show-current
```

Если команда вывела `master`, сначала переименуйте ветку в `main`:

```bash
git branch -M main
```

После этого выполните:

```bash
git push -u origin main
```

Еще одна возможная причина - в репозитории нет ни одного коммита. Тогда сначала выполните:

```bash
git status
git add .
git commit -m "Complete practice tasks"
```

А потом повторите `git push` для своей текущей ветки.

## Короткая шпаргалка

Если студент уже клонировал репозиторий преподавателя и создал пустой личный репозиторий:

```bash
git remote -v
git remote rename origin upstream
git remote add origin https://github.com/student/python_syntax_practice.git
git remote -v
git status
git add .
git commit -m "Complete practice tasks"
git branch --show-current
git branch -M main
git push -u origin main
```

Команда `git branch -M main` нужна, чтобы привести локальную ветку к названию `main`. Если ветка уже называется `main`, команда ничего плохого не сделает.

Если в вашей группе специально договорились оставлять ветку `master`, вместо двух последних команд используйте:

```bash
git push -u origin master
```
