# Антиспам-бот для групп в Telegram

Этот бот предназначен для автоматической обработки новых участников в группах Telegram. Он проверяет новых участников и ограничивает их, если они не подтвердят, что не являются спамерами.

## Как работает

1. Когда новый участник присоединяется к группе, бот отправляет приветственное сообщение с кнопкой подтверждения.
2. У нового участника есть 10 минут, чтобы нажать на кнопку и подтвердить, что он не спамер.
3. Если участник нажимает на кнопку вовремя, бот удаляет приветственное сообщение и отправляет сообщение о подтверждении.
4. Если участник не нажимает на кнопку в течение 10 минут, бот ограничивает его права в группе и отправляет сообщение об ограничении.

### Особенности работы

- Бот использует встроенные кнопки Telegram для подтверждения
- Все сообщения бота отправляются как ответ на сообщение о присоединении участника к группе
- Бот автоматически удаляет свои сообщения для поддержания чистоты в чате
- Администраторы могут легко изменять тексты сообщений и настройки бота

## Установка

1. Установите зависимости:
   ```bash
   pip install python-telegram-bot python-dotenv
   ```

2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/riders-agency/simply_telegram_group_antispam_bot.git
   cd simply_telegram_group_antispam_bot
   ```

3. Создайте файл `.env` в корневой директории командой или через редактор:
   ```bash
   echo "TOKEN=ваш_токен_бота" > .env
   ```

## Использование

1. Запустите бота:
   ```bash
   python src/simply_telegram_group_antispam_bot/main.py
   ```

2. Настройка бота как службы systemd:
   Создайте файл `/etc/systemd/system/simply_telegram_group_antispam_bot.service`:
   ```ini
   [Unit]
   Description=Служба для антиспам-бота Telegram
   After=network.target

   [Service]
   User=ваше_имя_пользователя
   WorkingDirectory=/path/to/simply_telegram_group_antispam_bot
   ExecStart=/usr/bin/python3 /path/to/simply_telegram_group_antispam_bot/main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Запустите и активируйте службу:
   ```bash
   sudo systemctl start simply_telegram_group_antispam_bot
   sudo systemctl enable simply_telegram_group_antispam_bot
   ```

## Изменение сообщений и текста кнопок

Чтобы изменить сообщения и текст кнопок, отредактируйте файл `/simply_telegram_group_antispam_bot/main.py`:

1. Приветственное сообщение:
   ```python
   self.WELCOME_MESSAGE = "Ваше новое приветственное сообщение"
   ```

2. Текст кнопки:
   ```python
   self.BUTTON_TEXT = "Ваш новый текст кнопки"
   ```

3. Сообщение подтверждения:
   ```python
   self.VERIFIED_MESSAGE = "Ваше новое сообщение подтверждения"
   ```

4. Какое сообщение получает учатник, если не нажал кнопку:
   ```python
   self.RESTRICTED_MESSAGES = [
       "Ваше новое сообщение ограничения 1",
       "Ваше новое сообщение ограничения 2",
       # Добавьте столько сообщений, сколько хотите
   ]
   ```

После внесения изменений перезапустите бота или службу.

## Обновление бота

1. Остановите службу:
   ```bash
   sudo systemctl stop simply_telegram_group_antispam_bot
   ```

2. Обновите код:
   ```bash
   cd /path/to/simply_telegram_group_antispam_bot
   git pull
   ```

3. Перезапустите службу:
   ```bash
   sudo systemctl start simply_telegram_group_antispam_bot
   ```

## Устранение неполадок

- Проверьте токен в файле `.env`
- Проверьте логи: `sudo journalctl -u simply_telegram_group_antispam_bot`
- Убедитесь, что бот имеет необходимые права в группе Telegram

---

# Anti-Spam Bot for Telegram Groups (simply_telegram_group_antispam_bot)

This bot is designed to automatically handle new members in Telegram groups. It checks new members and restricts them if they do not confirm they are not spammers.

## How the bot works

1. When a new member joins the group, the bot sends a welcome message with a confirmation button.
2. The new member has 10 minutes to press the button and confirm they are not a spammer.
3. If the member presses the button in time, the bot deletes the welcome message and sends a confirmation message.
4. If the member doesn't press the button within 10 minutes, the bot restricts their rights in the group and sends a restriction message.

### Bot operation scenarios

1. **Successful confirmation scenario:**
   - A new member joins the group
   - The bot sends a welcome message with a button
   - The member presses the button within 10 minutes
   - The bot deletes the welcome message
   - The bot sends a successful confirmation message

2. **Rights restriction scenario:**
   - A new member joins the group
   - The bot sends a welcome message with a button
   - The member doesn't press the button within 10 minutes
   - The bot restricts the member's rights in the group
   - The bot deletes the welcome message
   - The bot sends a rights restriction message

3. **Settings change scenario:**
   - An administrator edits the `main.py` file
   - The administrator changes message texts or other parameters
   - The administrator restarts the bot or service
   - The bot starts working with the new settings

### Bot features

- The bot uses Telegram's inline buttons for confirmation
- All bot messages are sent as replies to the member join message
- The bot automatically deletes its messages to keep the chat clean
- Administrators can easily change message texts and bot settings

## Installation

1. Install dependencies:
   ```bash
   pip install python-telegram-bot python-dotenv
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/riders-agency/simply_telegram_group_antispam_bot.git
   cd simply_telegram_group_antispam_bot
   ```

3. Create a `.env` file in the root directory:
   ```bash
   echo "TOKEN=your_bot_token" > .env
   ```

## Usage

1. Run the bot:
   ```bash
   python src/simply_telegram_group_antispam_bot/main.py
   ```

2. Set up the bot as a systemd service:
   Create a file `/etc/systemd/system/simply_telegram_group_antispam_bot.service`:
   ```ini
   [Unit]
   Description=Service for Telegram Anti-Spam Bot
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/simply_telegram_group_antispam_bot
   ExecStart=/usr/bin/python3 /path/to/simply_telegram_group_antispam_bot/main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Start and enable the service:
   ```bash
   sudo systemctl start simply_telegram_group_antispam_bot
   sudo systemctl enable simply_telegram_group_antispam_bot
   ```

## Changing Messages and Button Text

To change messages and button text, edit the `src/simply_telegram_group_antispam_bot/main.py` file:

1. Change the welcome message:
   ```python
   self.WELCOME_MESSAGE = "Your new welcome message"
   ```

2. Change the button text:
   ```python
   self.BUTTON_TEXT = "Your new button text"
   ```

3. Change the verification message:
   ```python
   self.VERIFIED_MESSAGE = "Your new verification message"
   ```

4. Change the restriction messages:
   ```python
   self.RESTRICTED_MESSAGES = [
       "Your new restriction message 1",
       "Your new restriction message 2",
       # Add as many messages as you want
   ]
   ```

After making changes, restart the bot or the service.

## Updating the Bot

1. Stop the service:
   ```bash
   sudo systemctl stop simply_telegram_group_antispam_bot
   ```

2. Update the code:
   ```bash
   cd /path/to/simply_telegram_group_antispam_bot
   git pull
   ```

3. Restart the service:
   ```bash
   sudo systemctl start simply_telegram_group_antispam_bot
   ```

## Troubleshooting

- Check the token in the `.env` file
- Check the logs: `sudo journalctl -u simply_telegram_group_antispam_bot`
- Ensure the bot has the necessary permissions in the Telegram group