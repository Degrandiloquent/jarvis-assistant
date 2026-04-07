# Vercel HTML Fix - Implementation TODO

## Plan Breakdown & Progress

### 1. ✅ Create TODO.md (Current step - done)

### 2. ✅ Restructure files to root for Vercel (copied successfully)
   - [x] Move frontend/index.html → root/index.html
   - [x] Move frontend/style.css → root/style.css  
   - [x] Move frontend/app.js → root/app.js
   - [x] Move frontend/vercel.json → root/vercel.json
   - [x] Move frontend/package.json → root/package.json
   - [x] Ensure api/gemini.js stays at root/api/gemini.js

### 3. ✅ Update package.json 
   - [x] Added Windows-compatible build script

### 4. ✅ Fix api/gemini.js body parsing
   - [x] Updated to handle frontend's body.contents format

### 5. Test local
   - [ ] Run `npm install` (if deps added)
   - [ ] Test static serve: npx serve .

### 6. Deploy followups (user actions)
   - [ ] vercel env add GEMINI_API_KEY
   - [ ] vercel --prod
   - [ ] Verify deployed site & API
