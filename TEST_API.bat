@echo off
echo Testing Backend API...
echo.

echo [1] Testing health endpoint...
curl http://localhost:8000/health
echo.
echo.

echo [2] Testing create game endpoint...
curl -X POST http://localhost:8000/api/games -H "Content-Type: application/json" -d "{\"player_names\":[\"Test\"],\"ai_players\":[\"aggressive\"],\"small_blind\":5,\"big_blind\":10,\"starting_stack\":1000}"
echo.
echo.

pause

