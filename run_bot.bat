@echo off
color c
title Bot Telegram horarios

:menu
echo.
echo.
echo Iniciando bot horarios...
echo.
python telegram_bot.py
pause >nul
goto menu
