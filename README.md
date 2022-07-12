# RPA - Robotic Process Automation na consulta de vulnerabilidades no site da NVD - National Vulnerability Database

## Site de consulta às vulnerabilidades
##### Trata-se de um site onde pode-se visualizar as vulnerabilidades de um software através de uma pesquisa por intervalo de tempo de até 120 dias. O site (disponível em: https://nvd.nist.gov/vuln/search) é vinculado ao NIST (National Institute of Standards and Technology). As vulnerabilidades possuem indentificadores (CVE's - Commom Vulnerabilities and Exposures) para catalogá-las e codificação (CVSSs - Common Vulnerability Scoring System) que as rotula como vulnerabilidades baixas, médias, altas ou críticas (mais sobre CVE e CVSS: https://aiqon.com.br/blog/explicar-o-cve-e-o-cvss/).
![image](https://user-images.githubusercontent.com/8295184/169683165-3aeaf0d2-ff8d-4f45-b024-87fad264ff30.png)

## A solução
##### Foi desenvolvido uma RPA que consistui-se em 4 bots e 2 maneiras de acesso bem como 2 meios de recebimento dos resultados. Todos os programas foram desenvolvidos em python (usando vários pacotes como Selenium, Pandas, Openpyxl, BeautifulSoup, etc.) com auxílio do QT Designer (vinculado ao python via package PyQt6) para criação da interface gráfica e uso de Flask, Heroku, html e afins para criação de aplicação web. Na planilha gerada, os CVE críticos ficam destacados em vermelho e os altos em amarelo. Estes mesmos dados são enviados no corpo do email do solicitante e também via mensagem de texto no whatsapp se assim o usuário desejar. Em anexo, tanto no email tanto no whatsapp a planilha completa com todos resultados (sejam quais forem os valores de CVSS) é enviada. CVE's com CVSS's maiores ou igual a 7 são os que aparecem em destaque no corpo das mensagens. Ademais, para fins de estudo e proteção, foi feita a criptografia do arquivo cujo conteúdo são dados de login e configuração do email remetente da aplicação (algoritmo utilizado: AES - Advanced Encryption Standard). Em suma, para isso tudo funcionar houve a necessidade de criar os seguintes bots:
  * Bot de execução do web scraping
  * Bot de registro no excel
  * Bot de envio de email
  * Bot de envio de whatsapp

### Assim ficou a interface gráfica:
<img src="https://user-images.githubusercontent.com/8295184/170782742-adcbaa72-7005-49bf-8e0a-7939bb24934e.png" width="300" height="400">

### Assim ficou a interface web:
<img src="https://user-images.githubusercontent.com/8295184/169683476-b7e3657b-a2df-4493-91d5-8d361f3cb1e6.png" width="300" height="400">

### Assim +/- ficam os emails:
<img src="https://user-images.githubusercontent.com/8295184/169682516-90f78a2c-bb8c-410e-91cf-2d7985b6ac8a.png" width="900" height="600">

### Assim +/- ficam as mensagens de whatsapp:
<img src="https://user-images.githubusercontent.com/8295184/169682569-13e73088-cfef-44ce-975e-f53d63223473.png" width="500" height="400">

## Links para o site, donwload da aplicação para desktop e vídeo explicativo:
  * https://appg3wspwa.herokuapp.com/ >>> Site
  * https://www.4shared.com/s/fJjZATZ0-ea >>> Download
  * https://www.youtube.com/watch?v=aZzSfYX1B_E >>> Vídeo
