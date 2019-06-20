pyinstaller -F build.spec

REM Copy Basic files
cp README.md dist
cp CHANGELOG.md dist
cp Setup.txt dist

xcopy /Y /S /I "./templates" "./dist/templates"

REM move exe to bin folder
mkdir "./dist/bin"
rm ./dist/bin/GenerateTopAPACCallsTemplate.exe
mv "./dist/GenerateTopAPACCallsTemplate.exe" "./dist/bin/GenerateTopAPACCallsTemplate.exe"
cp client_secret.json "./dist/bin"
cp credentials.json "./dist/bin"

REM Create Batch File
echo @echo off > "dist/GenerateTopAPACCallsTemplate.bat"
echo bin\GenerateTopAPACCallsTemplate.exe >> "dist/GenerateTopAPACCallsTemplate.bat"
echo pause >> "dist/GenerateTopAPACCallsTemplate.bat"

pause