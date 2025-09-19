# Deployment on Render

Here are the steps to deploy your project on Render:

## 1. Connect your GitHub repository

- Create a new "Web Service" on Render and connect it to your GitHub repository.

## 2. Configure the service

- **Name:** Give your service a name (e.g., `my-django-app`).
- **Region:** Choose a region close to you.
- **Branch:** Choose the branch you want to deploy (e.g., `main`).
- **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input`
- **Start Command:** `gunicorn core.wsgi:application`

## 3. Add Environment Variables

- Go to the "Environment" tab and add the following environment variables:

  - `SECRET_KEY`: Generate a new secret key.
  - `DEBUG`: `false`
  - `ALLOWED_HOSTS`: `yourapp.onrender.com` (replace with your app's domain on Render).
  - `DATABASE_URL`: This will be automatically set by Render when you create the database.
  - `REDIS_URL`: This will be automatically set by Render when you create the Redis instance.
  - `STRIPE_SECRET_KEY`: Your Stripe secret key.
  - `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key.
  - `PAYMENT_WEBHOOK_SECRET`: Your payment webhook secret.
  - `EMAIL_HOST`: Your email host.
  - `EMAIL_PORT`: Your email port.
  - `EMAIL_HOST_USER`: Your email host user.
  - `EMAIL_HOST_PASSWORD`: Your email host password.
  - `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`: Your Google OAuth2 key.
  - `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET`: Your Google OAuth2 secret.

## 4. Create a PostgreSQL Database

- Go to the "Databases" tab and create a new PostgreSQL database.
- Render will automatically provide the `DATABASE_URL` environment variable to your web service.

## 5. Create a Redis Instance

- Go to the "Redis" tab and create a new Redis instance.
- Render will automatically provide the `REDIS_URL` environment variable to your web service.

## 6. Deploy

- Click the "Create Web Service" button.
- Render will now build and deploy your application.

## 7. Run Migrations

- After the first deployment, you need to run the database migrations.
- Go to the "Shell" tab of your web service and run the following command:
  ```
  python manage.py migrate
  ```

That's it! Your application should now be live on Render.
