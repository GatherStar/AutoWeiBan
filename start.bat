@echo off
cat .\LICENSE
echo.
echo.
echo ͬ��Э���밴�س�������:
pause > nul

:testDependence
if not exist .\dependence (echo �����غ� Python3 ����) else (goto start)
goto end

:start
echo ��⵽Python3��������ʼ���г���
set /p _debug=�Ƿ���Ҫ����־��¼������Ҫ�밴y������
if "%_debug%"=="y" (goto debug) else (goto standard)

:debug
if not exist logs mkdir logs
set "datetime=%date:~,4%-%date:~5,2%-%date:~8,2%-%time:~0,2%-%time:~3,2%-%time:~6,2%"
.\dependence\python.exe main.py 2> .\logs\%datetime%.txt
echo ִ�н���������logs�ļ��в鿴��־
goto end

:standard
.\dependence\python.exe main.py
echo ִ�н���
goto end

:end
pause > nul & exit
