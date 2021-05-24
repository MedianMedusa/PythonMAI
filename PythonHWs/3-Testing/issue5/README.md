# pytest with mock
 Чтобы запустить проверку, надо выполнить:
 ```
 pip install pytest-cov
 python -m pytest --cov . --cov-report html
 ```

 В директории htmlcov, открыв index.html, для всех файлов покрытие должно быть 100% и ОК