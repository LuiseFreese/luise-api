# Email Notification Setup Guide

## SendGrid Setup

### Step 1: Create SendGrid Account
1. Go to [SendGrid.com](https://sendgrid.com) and create a free account
2. Free tier includes 100 emails/day forever - perfect for question notifications

### Step 2: Get API Key
1. Login to SendGrid dashboard
2. Go to **Settings** → **API Keys**
3. Click **Create API Key**
4. Choose **Restricted Access** and give permissions for **Mail Send**
5. Copy the generated API key (starts with `SG.`)

### Step 3: Configure Environment Variables

#### For Local Development:
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file:
   ```bash
   SENDGRID_API_KEY=SG.your_actual_api_key_here
   NOTIFICATION_EMAIL=your-email@example.com
   ```

#### For Railway Deployment:
1. Go to your Railway project dashboard
2. Click on your service
3. Go to **Variables** tab
4. Add these environment variables:
   - `SENDGRID_API_KEY`: Your SendGrid API key
   - `NOTIFICATION_EMAIL`: Your email address

### Step 4: Verify Email Domain (Optional but Recommended)
1. In SendGrid dashboard, go to **Settings** → **Sender Authentication**
2. Authenticate your domain (m365princess.com)
3. This improves email deliverability and allows custom "from" addresses

## How It Works

When someone submits a question via the API:

1. ✅ **Question is saved** to `questions.json` file
2. ✅ **API responds** with success message  
3. ✅ **Email notification sent** to your configured email address
4. ✅ **If email fails**, API still succeeds (non-blocking)

## Email Content

You'll receive a nicely formatted HTML email with:
- Talk ID and Question ID
- User's name and email
- Full question text
- Submission timestamp
- Pink/purple branding matching your API theme

## Testing

Without environment variables configured:
- Questions still save to file ✅
- API still works ✅  
- You'll see "Email notification skipped" in logs

With environment variables configured:
- Everything above ✅
- Plus email notifications sent to your inbox 📧

## Troubleshooting

**No emails received?**
- Check SendGrid API key is correct
- Verify `NOTIFICATION_EMAIL` is set
- Check spam folder
- Look at server logs for error messages

**API errors?**
- Email failures won't break the API
- Questions still save even if email fails
- Check server logs for specific error details