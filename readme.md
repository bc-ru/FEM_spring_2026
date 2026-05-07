# Установка Docker и запуск контейнера для лабораторных работ по МКЭ

Этот репозиторий содержит окружение для выполнения лабораторных работ по методу конечных элементов.  
Основной способ работы — через Docker-контейнер с уже установленными `FEniCS Legacy`, `Gmsh`, `meshio`, `Streamlit` и другими необходимыми библиотеками.

## Требования

- Ubuntu Linux;
- установленный Docker;
- VS Code, если планируется работа через Dev Containers;
- внимательность при выполнении команд.

---

# 1. Установка Docker

Если Docker уже установлен, этот раздел можно пропустить.

## 1.1. Установка Docker Engine

Выполните следующие команды:

```bash
sudo apt update
sudo apt install ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 1.2. Проверка установки

Проверьте статус Docker:

```bash
sudo systemctl status docker
```

Если Docker не запущен, выполните:

```bash
sudo systemctl start docker
```

Проверьте работу Docker на тестовом образе:

```bash
sudo docker run hello-world
```

## 1.3. Запуск Docker без `sudo`

Чтобы не писать `sudo` перед каждой командой Docker, добавьте пользователя в группу `docker`:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

После этого может потребоваться перезагрузка системы или выход из сессии и повторный вход.

Проверьте, что Docker запускается без `sudo`:

```bash
docker run hello-world
```

---

# 2. Получение готового образа

Готовый образ находится в GitHub Container Registry:

```bash
docker pull ghcr.io/bc-ru/fenics-gmsh-env:stable
```

Образ содержит основное окружение для работы с:

- `FEniCS Legacy`;
- `Gmsh`;
- `meshio`;
- `Streamlit`;
- Python-библиотеками, необходимыми для выполнения лабораторных работ.

---

# 3. Запуск контейнера

Контейнер можно запускать двумя способами:

1. через VS Code Dev Containers;
2. через обычную консольную команду или скрипт.

---

## 3.1. Запуск через VS Code

В репозитории уже подготовлен файл конфигурации Dev Containers:

```text
.devcontainer/devcontainer.json
```

Для запуска:

1. Откройте папку проекта в VS Code.
2. Нажмите `Ctrl + Shift + P`.
3. Выберите команду:

```text
Dev Containers: Reopen in Container
```

После этого VS Code перезапустит проект внутри Docker-контейнера.

В результате вы окажетесь в новом окне VS Code, где:

- файлы проекта останутся теми же;
- Python-окружение будет взято из контейнера;
- должны работать Pylance, IntelliSense и отладчик;
- терминал VS Code будет открыт внутри контейнера.

Это основной рекомендуемый способ работы.

---

## 3.2. Запуск через CLI

Перед запуском нужно находиться в корневой директории репозитория.

```bash
docker run --rm -it \
  -p 127.0.0.1:8501:8501 \
  -v "$(pwd)":/workspace \
  -w /workspace \
  ghcr.io/bc-ru/fenics-gmsh-env:stable
```

Что делает эта команда:

- `--rm` — удаляет контейнер после завершения работы;
- `-it` — запускает контейнер в интерактивном режиме;
- `-v "$(pwd)":/workspace` — монтирует текущую директорию проекта внутрь контейнера;
- `-w /workspace` — задаёт рабочую директорию внутри контейнера;
- `ghcr.io/bc-ru/fenics-gmsh-env:stable` — образ, из которого запускается контейнер.

После запуска вы попадёте в консоль контейнера.  
Python-скрипты можно запускать обычным образом, например:

```bash
python3 solver/run_batch.py
```

---

## 3.3. Запуск через скрипт

Если в репозитории есть скрипт `run.sh`, сначала разрешите его выполнение:

```bash
chmod +x run.sh
```

Затем запускайте контейнер командой:

```bash
./run.sh
```

Скрипт нужно запускать из корневой директории проекта.

---

# 4. Рабочая директория контейнера

Внутри контейнера рабочей директорией является:

```text
/workspace
```

При запуске проекта текущая директория хоста монтируется внутрь контейнера как `/workspace`.

То есть файлы:

```text
на хосте:      текущая директория проекта
в контейнере: /workspace
```

являются одними и теми же файлами.

Поэтому все изменения, сделанные внутри `/workspace`, сохраняются в основной файловой системе хоста.

---

# 5. Проблема прав доступа

Контейнер запускается от имени `root`. Из-за этого файлы, созданные внутри контейнера, могут принадлежать пользователю `root` на хосте.

Если после работы с контейнером некоторые файлы нельзя редактировать или удалять с хоста, выполните из корневой директории проекта:

```bash
sudo chown -R "$(id -u):$(id -g)" .
chmod -R u+rwX .
```

Для удобства можно создать скрипт `fix_permissions.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

case "$(pwd)" in
  /|/home|/root|/usr|/etc|/var|/opt)
    echo "Refusing to run from unsafe directory: $(pwd)" >&2
    exit 1
    ;;
esac

echo "Fixing ownership under: $(pwd)"
echo "New owner: ${HOST_UID}:${HOST_GID}"

sudo chown -R "${HOST_UID}:${HOST_GID}" .
chmod -R u+rwX .

echo "Done."
```

Затем:

```bash
chmod +x fix_permissions.sh
./fix_permissions.sh
```

Важно: этот скрипт нужно запускать только из корневой директории проекта.

---

# 6. Запуск Streamlit-приложения

Для запуска Streamlit внутри контейнера выполните:

```bash
streamlit run app.py
```

После запуска Streamlit выведет адрес в консоль. Обычно это:

```text
http://127.0.0.1:8501
```

Если порт отличается, используйте тот адрес, который показан в терминале.

---

# 7. Сборка собственного образа

При необходимости можно создать собственный Docker-образ на основе готового окружения.

## 7.1. Dockerfile

Создайте файл `Dockerfile` и укажите базовый образ:

```dockerfile
FROM ghcr.io/bc-ru/fenics-gmsh-env:stable
```

Ниже можно добавить свои изменения. Например, установить дополнительную Python-библиотеку:

```dockerfile
RUN python3 -m pip install --no-cache-dir some-lib-name
```

## 7.2. Сборка образа

Команда сборки выполняется из директории, где находится `Dockerfile`:

```bash
docker build -t your-image-name .
```

После этого образ можно запустить:

```bash
docker run --rm -it \
  -p 127.0.0.1:8501:8501 \
  -v "$(pwd)":/workspace \
  -w /workspace \
  your-image-name
```

---

# 8. Краткий сценарий работы

Самый простой способ начать работу:

1. Установить Docker.
2. Установить VS Code.
3. Открыть папку проекта в VS Code.
4. Выполнить:

```text
Dev Containers: Reopen in Container
```

После этого проект откроется внутри контейнера.  
Можно запускать Python-скрипты, пользоваться автодополнением, отладчиком и всеми библиотеками из подготовленного окружения.

Для ручного запуска из терминала используйте:

```bash
docker run --rm -it \
  -p 127.0.0.1:8501:8501 \
  -v "$(pwd)":/workspace \
  -w /workspace \
  ghcr.io/bc-ru/fenics-gmsh-env:stable
```