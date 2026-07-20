# Step 1: Deploy to Vercel (Production)

Deploying to Vercel is the easiest and fastest way to get your Hackathon project live on the internet so the judges can interact with it.

Because we are using **Vite + React**, Vercel will automatically detect the framework and deploy it instantly.

## Deployment Instructions

1. **Push your code to GitHub (if you haven't already):**
   Open your terminal in the root of the project and run:
   ```bash
   git add .
   git commit -m "Final Hackathon Architecture Complete"
   git push origin main
   ```

2. **Log into Vercel:**
   Go to [Vercel.com](https://vercel.com/) and log in with your GitHub account.

3. **Import your Repository:**
   - Click the **Add New...** button and select **Project**.
   - Find your AIDP repository in the list and click **Import**.

4. **Configure & Deploy:**
   - Vercel will automatically detect the **Framework Preset** as `Vite`.
   - Leave the Build Command (`npm run build`) and Output Directory (`dist`) as the defaults.
   - Click **Deploy**.

Within 60 seconds, your site will be live! Vercel will generate a secure `https://...` URL that you can immediately paste into your Devpost submission!
