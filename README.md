# Shared Planner

A collaborative planning application with calendar integration and email notifications.

## Features

- User management with admin capabilities
- Shop and reservation management
- Email notifications and reminders
- Calendar integration (ICS format)
- Multi-language support (English and French)
- Responsive web interface

## Project Structure

- `shared_planner/` - Python backend
  - `api/` - REST API endpoints
  - `db/` - Database models and operations
  - `ics.py` - Calendar integration
  - `mailer_daemon.py` - Email notification system
  - `week.py` - Week management logic
  - `templates/` - Email templates

- `web/` - Vue.js frontend application
  - Built with Vue 3 + TypeScript + Vite
  - PrimeVue component library

## Requirements

- Python 3.12+
- Node.js 16+
- SQLite3 database
- SMTP server for emails (e.g. OVH)

## Setup

### Backend Setup

1. Install `uv` (if not already installed):
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```sh
uv sync
```

3. Set up environment variables:
```sh
cp .env.example .env  # If an example exists, otherwise create .env
nano .env
```

### Frontend Setup

1. Navigate to the web directory:
```sh
cd web
```

2. Install dependencies:
```sh
npm install
```

## Development

### Using Docker (Recommended)

This project supports hot-reloading for both the UI and backend using Docker Compose.

1. Start the services:
   ```sh
   docker compose up --build
   ```

2. (Optional) Enable Docker Compose Watch for automatic sync:
   ```sh
   docker compose watch
   ```

The Backend will be available at `http://localhost:8000` and the UI at `http://localhost:5173`.

### Manual Running

**Backend:**
```sh
uv run python -m shared_planner
```

**Frontend:**
```sh
cd web
npm run dev
```

## Production

### Using Docker

The production setup bundles the UI and Backend into a single optimized container.

1. Build and run:
   ```sh
   docker compose -f docker-compose.prod.yml up --build -d
   ```
The application will be available at `http://localhost:8000`.

### Manual Build

1. Build the frontend:
```sh
cd web
npm run build
```

2. Run the backend with a production server:
```sh
uv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker shared_planner.api:app --bind 0.0.0.0:8000
```

## Configuration

### Required Settings

The following settings must be configured in the admin interface:

- `base_domain`: The domain name of your server (e.g., https://example.com)
- `admin_mail`: Email address for admin notifications
- `mail_from`: Email address used as the sender for notifications

### Optional Settings

- `block_all_emails`: Disable all email notifications (useful for testing)
- `email_notification_before`: Hours before a reservation to send a reminder
- `cleanup_reminders_days`: Days to keep reminders before cleanup
- `cleanup_notifications_days`: Days to keep notifications before cleanup
- `token_validity`: Hours before login tokens expire

For a complete list of settings and their descriptions, head to the Admin > Server Settings page where you will be able to modify them and find a detailed description of each setting.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
