# 🚀 Инструкция по деплою дашборда

## Варианты деплоя

### 1. Streamlit Cloud (Рекомендуется)

**Преимущества**: Бесплатно, простота настройки, автоматические обновления

**Шаги**:
1. Загрузите проект на GitHub
2. Перейдите на [share.streamlit.io](https://share.streamlit.io)
3. Подключите GitHub аккаунт
4. Выберите репозиторий и ветку
5. Укажите путь к файлу: `app.py`
6. Нажмите "Deploy"

**Время деплоя**: 2-5 минут

### 2. Heroku

**Преимущества**: Надежность, масштабируемость

**Дополнительные файлы**:

Создайте `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Создайте `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**Шаги**:
1. Установите Heroku CLI
2. `heroku create your-app-name`
3. `git push heroku main`

### 3. Docker

**Создайте Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Команды**:
```bash
docker build -t warehouse-dashboard .
docker run -p 8501:8501 warehouse-dashboard
```

### 4. VPS/Сервер

**Установка на Ubuntu**:
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip -y

# Клонирование проекта
git clone <your-repo-url>
cd streamlit_dashboard

# Установка зависимостей
pip3 install -r requirements.txt

# Запуск (для тестирования)
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Для продакшена используйте systemd или supervisor
```

**Создание systemd сервиса** (`/etc/systemd/system/dashboard.service`):
```ini
[Unit]
Description=Warehouse Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/streamlit_dashboard
ExecStart=/usr/local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Активация:
```bash
sudo systemctl enable dashboard
sudo systemctl start dashboard
```

## Настройка доменного имени

### Nginx конфигурация

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL сертификат (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Мониторинг и логи

### Просмотр логов
```bash
# Systemd
sudo journalctl -u dashboard -f

# Docker
docker logs -f container-name

# Heroku
heroku logs --tail -a your-app-name
```

### Мониторинг ресурсов
```bash
# CPU и память
htop

# Дисковое пространство
df -h

# Сетевые подключения
netstat -tulpn | grep 8501
```

## Безопасность

### Базовые настройки

1. **Обновите пароли по умолчанию**
2. **Настройте файрвол**:
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

3. **Ограничьте доступ к данным**:
   - Используйте переменные окружения для чувствительных данных
   - Настройте права доступа к файлам

### Переменные окружения

Создайте `.env` файл (не добавляйте в Git):
```env
DATABASE_URL=your_database_url
API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

Используйте в коде:
```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
```

## Обновление приложения

### Автоматическое обновление (GitHub Actions)

Создайте `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.KEY }}
        script: |
          cd /path/to/your/app
          git pull origin main
          pip install -r requirements.txt
          sudo systemctl restart dashboard
```

### Ручное обновление
```bash
cd /path/to/your/app
git pull origin main
pip install -r requirements.txt
sudo systemctl restart dashboard
```

## Резервное копирование

### Скрипт бэкапа
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/dashboard"
APP_DIR="/home/ubuntu/streamlit_dashboard"

mkdir -p $BACKUP_DIR

# Бэкап файлов приложения
tar -czf $BACKUP_DIR/app_$DATE.tar.gz -C $APP_DIR .

# Бэкап данных
cp -r $APP_DIR/data $BACKUP_DIR/data_$DATE

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "data_*" -mtime +30 -exec rm -rf {} \;
```

### Автоматизация бэкапов (crontab)
```bash
# Ежедневный бэкап в 2:00
0 2 * * * /path/to/backup_script.sh
```

## Производительность

### Оптимизация Streamlit

1. **Кэширование данных**:
   ```python
   @st.cache_data(ttl=300)  # 5 минут
   def load_data():
       return expensive_operation()
   ```

2. **Ленивая загрузка**:
   ```python
   if 'data' not in st.session_state:
       st.session_state.data = load_data()
   ```

3. **Оптимизация графиков**:
   ```python
   # Уменьшение количества точек для больших датасетов
   if len(data) > 1000:
       data = data.sample(1000)
   ```

### Мониторинг производительности

```python
import time
import streamlit as st

start_time = time.time()
# Ваш код
execution_time = time.time() - start_time

if execution_time > 1:
    st.warning(f"Медленная операция: {execution_time:.2f}s")
```

## Устранение проблем

### Частые ошибки

1. **Port already in use**:
   ```bash
   sudo lsof -i :8501
   sudo kill -9 PID
   ```

2. **Permission denied**:
   ```bash
   sudo chown -R $USER:$USER /path/to/app
   chmod +x app.py
   ```

3. **Module not found**:
   ```bash
   pip install -r requirements.txt
   # или
   pip install --upgrade streamlit
   ```

### Логи и отладка

```bash
# Подробные логи Streamlit
streamlit run app.py --logger.level debug

# Проверка конфигурации
streamlit config show

# Очистка кэша
streamlit cache clear
```

## Контакты и поддержка

- **Документация Streamlit**: https://docs.streamlit.io/
- **GitHub Issues**: Создайте issue в репозитории проекта
- **Сообщество**: https://discuss.streamlit.io/

---

**Удачного деплоя! 🚀**

