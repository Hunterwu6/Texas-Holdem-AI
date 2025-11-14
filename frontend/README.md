# Texas Hold'em AI Battle Simulator - Frontend

Beautiful React + TypeScript + TailwindCSS frontend for playing poker against AI.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
# or
pnpm install
```

### 2. Start Development Server

```bash
npm run dev
# or
pnpm dev
```

Frontend will be available at: **http://localhost:3000**

### 3. Make Sure Backend is Running

The frontend needs the backend API running:
```bash
cd ../backend
python -m app.main
```

Backend should be at: **http://localhost:8000**

## ✨ Features

### Implemented
- ✅ Beautiful poker table UI with green felt
- ✅ Player seats arranged in circle
- ✅ Card display with suits and ranks
- ✅ Real-time game state updates
- ✅ Action panel with all poker actions
- ✅ Fold, Check, Call, Bet, Raise, All-In buttons
- ✅ Quick bet buttons (1/2 pot, pot, all-in)
- ✅ Player stack and bet display
- ✅ Dealer button indicator
- ✅ Current player highlighting
- ✅ Community cards display
- ✅ Pot display
- ✅ Game phase indicator
- ✅ Responsive design

### UI Components
- **PokerTable**: Main table with player seats in circle
- **PlayerSeat**: Individual player display with cards and info
- **ActionPanel**: Control panel for player actions
- **Card**: Playing card component with suits

## 🎮 How to Play

1. **Create Game**
   - Enter your name
   - Select number of AI opponents (1-8)
   - Choose AI strategy (Aggressive, Conservative, or Random)
   - Click "Create Game"

2. **Start Hand**
   - Click "Start Hand" to begin
   - Cards are dealt
   - Blinds are posted

3. **Make Your Move**
   - Wait for your turn (yellow highlight)
   - Choose action: Fold, Check, Call, Raise, or All-In
   - Use quick bet buttons for common amounts
   - Game auto-refreshes every 2 seconds

4. **Watch AI Play**
   - AI players automatically make their moves
   - See their decisions in real-time

5. **Next Hand**
   - After hand completes, click "Next Hand"
   - Or start a new game

## 🎨 Design Features

### Colors
- **Background**: Dark slate (#0F172A)
- **Table**: Green felt (#065F46)
- **Primary**: Emerald green (#10B981)
- **Danger**: Red (#EF4444)
- **Warning**: Amber (#F59E0B)

### Animations
- Player turn highlighting (pulsing yellow ring)
- Hover effects on buttons
- Smooth transitions
- Card flip animations (CSS)

### Layout
- Circular player arrangement
- Center pot and community cards
- Bottom action panel
- Right sidebar for game info

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Card.tsx           # Playing card component
│   │   ├── PlayerSeat.tsx     # Player display
│   │   ├── PokerTable.tsx     # Main table layout
│   │   └── ActionPanel.tsx    # Player controls
│   ├── App.tsx                # Main application
│   ├── api.ts                 # API client
│   ├── types.ts               # TypeScript types
│   ├── main.tsx               # Entry point
│   └── index.css              # Global styles + Tailwind
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## 🔧 Configuration

### API Endpoint
Edit `src/api.ts` to change the API URL:
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

### Auto-Refresh Interval
Edit `src/App.tsx` to change refresh rate:
```typescript
const interval = setInterval(async () => {
  // ... refresh code
}, 2000); // milliseconds
```

## 🎯 Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🐛 Troubleshooting

### Backend Connection Error
**Problem**: "Failed to fetch" or CORS error

**Solution**: 
1. Make sure backend is running on port 8000
2. Check CORS settings in backend `main.py`
3. Verify API_BASE_URL in `src/api.ts`

### Port Already in Use
**Problem**: Port 3000 is busy

**Solution**: 
```bash
# Edit vite.config.ts and change port
server: {
  port: 3001
}
```

### Cards Not Showing
**Problem**: Cards show as "?"

**Solution**: Game needs to be started and in progress

## 🎨 Customization

### Change Table Color
Edit `tailwind.config.js`:
```javascript
'poker-felt': '#047857', // Your color here
```

### Add More AI Strategies
Edit `src/App.tsx` in the AI strategy select:
```tsx
<option value="balanced">Balanced (GTO)</option>
<option value="adaptive">Adaptive</option>
```

### Adjust Player Positions
Edit `src/components/PokerTable.tsx`:
```typescript
const radius = 45; // Adjust circle radius (percentage)
```

## ✨ Features to Add

Ideas for extending the frontend:

- [ ] Hand history panel
- [ ] Statistics display (VPIP, PFR)
- [ ] Sound effects
- [ ] Chat/log panel
- [ ] Multiple table support
- [ ] Tournament mode UI
- [ ] Mobile responsive improvements
- [ ] Dark/light theme toggle
- [ ] Save game state
- [ ] Replay hands

## 🏆 Production Build

```bash
# Build for production
npm run build

# Files will be in dist/
# Serve with any static hosting:
npm run preview
```

## 📱 Responsive Design

- **Desktop**: Full featured, optimal experience
- **Tablet**: Adapted layout, works well
- **Mobile**: Basic support, may need scrolling

## 🎉 You're Ready!

1. Start backend: `cd backend && python -m app.main`
2. Start frontend: `cd frontend && npm run dev`
3. Open: http://localhost:3000
4. Play poker! 🎰

Enjoy your beautiful poker game!

