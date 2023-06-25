#!/bin/bash
echo "<============= Running tests ===========>"
cd /server && poetry run pytest . --alluredir=allure_report
cd /server && allure generate allure_report \
&& python3 -m http.server --directory allure-report \
&& sleep infinity