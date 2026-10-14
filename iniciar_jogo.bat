@echo off
title Palavras Cruzadas - Duelo Local
cls
echo ========================================================
echo    PALAVRAS CRUZADAS - DUELO COMPETITIVO LOCAL
echo ========================================================
echo.
echo  Iniciando o servidor do jogo...
echo.
for /f "tokens=4" %%a in ('route print 0.0.0.0 ^| find "0.0.0.0" ^| find /v "0.0.0.0      0.0.0.0"') do set IP=%%a
echo  -------------------------------------------------------
echo  COMO JOGAR NO CELULAR:
echo.
echo  1. Conecte o celular na mesma rede Wi-Fi deste computador.
echo  2. Abra o navegador do celular (Chrome ou Safari) e acesse:
echo.
echo     http://%IP%:5173
echo.
echo  DICA: No celular, toque em "Opcoes" e depois em
echo  "Adicionar a tela de inicio" para jogar como um App!
echo  -------------------------------------------------------
echo.
npx vite --host 0.0.0.0 --port 5173
pause
