# 🔧 Troubleshooting Guide - Vercel + Railway Connection

## Common Issues and Solutions

### Issue 1: "Cannot connect to backend API"

**Check these:**

1. **Railway Backend is Running:**
   - Go to Railway Dashboard → Your Service
   - Check if status is "Active" (green)
   - Check logs for any errors

2. **Railway URL is Accessible:**
   - Open: `https://medicalchatbot-production-1957.up.railway.app` in browser
   - Should show Flask app or JSON response
   - If you see "Connection refused" or timeout, Railway service might be down

3. **Test API Endpoint:**
   - Open: `https://medicalchatbot-production-1957.up.railway.app/predict`
   - Should show error about "missing symptoms" (not connection error)
   - This confirms the endpoint is working

### Issue 2: Environment Variables Not Working

**Check these:**

1. **Variable Name is Correct:**
   - Must be exactly: `VITE_API_URL` (case-sensitive)
   - Not: `VITE_API_URL_` or `API_URL` or `VITE_API`

2. **Value is Correct:**
   - Must include `https://`
   - Example: `https://medicalchatbot-production-1957.up.railway.app`
   - NOT: `medicalchatbot-production-1957.up.railway.app` (missing https://)

3. **Environment is Selected:**
   - In Vercel, when adding variable, select:
     - ✅ Production
     - ✅ Preview  
     - ✅ Development
   - If only Production is selected, Preview/Dev won't work

4. **Redeployed After Adding:**
   - **CRITICAL:** After adding env vars, you MUST redeploy!
   - Go to Deployments → Click "Redeploy"
   - Environment variables are baked into the build at build time

### Issue 3: CORS Errors

**Symptoms:**
- Browser console shows: "Access-Control-Allow-Origin" error
- Network tab shows OPTIONS request failing

**Solution:**
- Backend has CORS enabled (already fixed in code)
- Make sure Railway backend is using latest code
- Redeploy Railway if needed

### Issue 4: "API URL not configured" Error

**This means:**
- `VITE_API_URL` is not set in Vercel
- OR Vercel wasn't redeployed after adding it

**Fix:**
1. Go to Vercel → Settings → Environment Variables
2. Add `VITE_API_URL` = `https://medicalchatbot-production-1957.up.railway.app`
3. Select all environments
4. Save
5. **Redeploy Vercel** (important!)

### Issue 5: Check Browser Console

**Steps:**
1. Open your Vercel app
2. Press F12 (open DevTools)
3. Go to "Console" tab
4. Look for:
   - `API URL: https://...` (should show your Railway URL)
   - Any red errors
   - CORS errors

5. Go to "Network" tab
6. Try making a prediction
7. Look for the `/predict` request
8. Check:
   - Status code (200 = success, 404/500 = error)
   - Request URL (should be your Railway URL)
   - Response (should be JSON with prediction)

## Quick Checklist

- [ ] Railway service is running (green status)
- [ ] Railway URL is accessible in browser
- [ ] `VITE_API_URL` is set in Vercel (with `https://`)
- [ ] Environment variable is set for Production
- [ ] Vercel was redeployed after adding env var
- [ ] Browser console shows correct API URL
- [ ] No CORS errors in console

## Still Not Working?

1. **Check Railway Logs:**
   - Railway Dashboard → Your Service → Logs
   - Look for errors when making API calls

2. **Check Vercel Logs:**
   - Vercel Dashboard → Your Project → Deployments
   - Click on latest deployment → View Function Logs

3. **Test API Directly:**
   ```bash
   curl -X POST https://medicalchatbot-production-1957.up.railway.app/predict \
     -H "Content-Type: application/json" \
     -d '{"symptoms": ["fever", "cough"]}'
   ```

4. **Verify Environment Variable:**
   - In Vercel, check if variable shows in the list
   - Make sure it's not hidden or deleted

---

**Most common issue: Forgetting to redeploy Vercel after adding environment variables!**

