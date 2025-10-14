@echo off
chcp 65001 > nul
echo ================================================
echo    RFP JSON 파일 GitHub 업로드
echo ================================================
echo.

REM JSON 파일 확인
echo 📁 JSON 파일 확인 중...
if not exist "*.json" (
    echo ❌ JSON 파일이 없습니다!
    pause
    exit /b
)

echo 📋 업로드할 파일:
dir /b *.json
echo.

REM Git 상태 확인
echo 🔍 변경사항 확인 중...
git status --short *.json
echo.

REM 사용자 확인
set /p confirm="위 파일들을 GitHub에 업로드하시겠습니까? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo ❌ 취소되었습니다.
    pause
    exit /b
)

echo.
echo 📤 GitHub에 업로드 중...
echo.

REM Git 작업
git add *.json

if errorlevel 1 (
    echo ❌ Git add 실패!
    pause
    exit /b
)

REM 타임스탬프로 커밋 메시지 생성
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%a-%%b-%%c)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (set mytime=%%a:%%b)
git commit -m "Update JSON files - %mydate% %mytime%"

if errorlevel 1 (
    echo ⚠️ 변경사항이 없거나 커밋 실패!
    echo.
    pause
    exit /b
)

git push

if errorlevel 1 (
    echo ❌ Push 실패! 인터넷 연결이나 Git 설정을 확인하세요.
    pause
    exit /b
)

echo.
echo ================================================
echo ✅ 성공적으로 업로드되었습니다!
echo ================================================
echo.
echo 🌐 1~2분 후 웹사이트에서 확인하세요:
echo    https://jinbless.github.io/rfp-viewer/
echo.
pause

