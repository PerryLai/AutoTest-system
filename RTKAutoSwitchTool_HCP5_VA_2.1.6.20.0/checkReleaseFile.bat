@echo off

set FILENAME=releaseFileList.txt
for /f "delims=^" %%i in (%FILENAME%) do (
	if not exist %%i (
		echo [Warning] %%i is not existed.
	)
)
pause >nul