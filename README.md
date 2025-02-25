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

1. Install dependencies using Poetry:
```sh
poetry install
```

2. Set up environment variables:
```sh
nano .env
SMTP_SERVER=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
```

### Frontend Setup

1. Navigate to the web directory:
```sh
cd web
```

2. Install dependencies and build the frontend:
```sh
npm install
```

## Development

### Running the Backend
```sh
poetry run python -m shared_planner
```

### Running the Frontend
```sh
cd web
npm run dev
```

The application will be available at http://localhost:5173

### Production Build

1. Build the frontend:
```sh
cd web
npm run build
```

2. Configure your web server to serve the static files from `web/dist`

3. Run the backend with a production WSGI server:
```sh
poetry run gunicorn shared_planner.main:app
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
