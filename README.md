# Bybit Multi-Pair Strong Zones Bot

### 🔧 Налаштування
1. Створіть сервіс на [Render](https://render.com).
2. Завантажте цей репозиторій.
3. У **Environment** додайте:
   - `BYBIT_API_KEY=ваш_api_key`
   - `BYBIT_API_SECRET=ваш_api_secret`
4. Deploy → Start worker.

Бот автоматично:
- Сканує список монет (BTC, ETH, SOL, XRP).
- Визначає сильні зони.
- Входить у угоди на пробій рівня.
- Можна розширювати список монет у `bot.py`.
