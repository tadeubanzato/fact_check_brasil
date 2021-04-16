# Python :snake:, Telegram <img src="https://logos-download.com/wp-content/uploads/2016/07/Telegram_logo.png" width="25" height="25"> e Democracia :fire:

A idéia principal desse script é postar em um canal aberto e público do Telegram toda vez que um novo Fact Check é feito nos principais canais de checagem de fatos do Brasil.

Caso você ache interessante você pode colocar esse robô no grupo de Telegram da família ou daqueles amigos negacionistas que você adora. :grin:

*Preciso deixar claro, não desenvolvedor então há oportunidades óbvias de melhoria no código então qualquer um pode ajudar a melhorar o que foi desenvolvido*. :sunglasses:

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/tadeubanzato/fact_check_brasil/graphs/commit-activity) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/tadeubanzato/fact_check_brasil/blob/main/LICENSE) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/tadeubanzato/fact_check_brasil)
</br>

### Os canais que estão sendo manitorados são:
- Agência Lupa - https://piaui.folha.uol.com.br/lupa/
- UOL Confere - https://noticias.uol.com.br/confere
- Projeto Comprova - https://projetocomprova.com.br/
- G1 Fato ou Fake - https://g1.globo.com/fato-ou-fake/
- G1 Fato ou Fake (Corona Virus) - https://g1.globo.com/fato-ou-fake/coronavirus/
- Estadão Verifica - https://politica.estadao.com.br/blogs/estadao-verifica/
- Aos Fatos - https://www.aosfatos.org/noticias/nas-redes/
- Boatos - https://www.boatos.org/

## Vamos aos comentários:
### Configurações iniciais
Esse script está rodando em uma Raspberry Pi com linux por isso desenvolvi um Shell script para verificar se o script está rodando a cada 15 minutos. Caso o script pare ele reinicia automaticamente.

### Python Requirements :snake:
Para instalar os requirements rode o comando `sudo pip3 install -r requirements.txt`.
Este comando instalará as seguintes bibliotecas do Python:
- telegram-send==0.25
- more-itertools==8.7.0
- requests==2.25.1
- beautifulsoup4==4.9.3
- xmltodict==0.12.0
- urllib3==1.26.3
- pandas==1.2.3

### Shell script para manter o programa rodando
```shell
#!/bin/sh
## Cria variável com o caminho do script Python
CHECK=/tmp/check.pid

if [ -f "$CHECK" ]; then
    ## Se o arquivo existir ele não faz nada só avisa que está rodando
    echo "$CHECK exists."
else
    ## Se o arquivo não existir ele roda os comandos para rodar o script em Python
    echo "$CHECK does not exist."
    cd /home/pi/telegrambot/factcheck
    screen -dm -S CHECK python3 /home/pi/telegrambot/factcheck/fact_check.py
fi

```
### API do Telegram - BotFather
Para rodar o programa é preciso criar um Token Key para o Telegram, para fazer isso procure o usuário BotFather no telegram

<img src="https://cdn-images-1.medium.com/max/1600/1*XolFpjck53uWNRG8dOZz7w.png" width="40" height="40"> Link direto: https://web.telegram.org/#/im?p=@BotFather

### Chat ID do Telegram
O jeiro mais fácil de verificar o Chat-ID do Telegram para o bot mandar as mensagens basta entrar na URL com o token `https://api.telegram.org/bot"TOKEN-DO-TELEGRAM"/getUpdates`
#### Neste link você terá acesso ao JSON do Bot que trará os dados confirme abaixo:
```json
{"ok":true,"result":[{"update_id":0000000,
"channel_post":{"message_id":76,"sender_chat":{"id":-1234567890,"title":"Fact Check Bot \ud83d\udc4a\ud83c\udffd","username":"factcheckbrasil","type":"channel"},"chat":
```
**O que é importante neste JSON**</br>
`update_id":0000000` é o código do seu robô no Telegram</br>
`"id":-1234567890` é o ID que tem que ser inserido no código Python


#### Ao encontrar o BotFather digite o seguinte comando
- `/newbot` - Para criar um novo bot
- `/setname` - Para dar nome ao bot
- `/setdescription` - Para criar a descrição do bot
- `/setyourpic` - Para adicionar uma foto ao bot (eu usei o https://thispersondoesnotexist.com/ um projeto muito massa que cria foto de pessoas que não existem)
- `/token` - Para criar e verificar o API Token do seu robô
- `/setprivacy` - Aqui você tem que desligar a privacy para poder deixar o robô postar em um Canal do Telegram ou Groupo

Depois de feito isso você tem que criar um Canal ou um Grupo do Telegram com seu usuário e adicionar o robô. Eu geralmente adiciono o robô como administrador o que ajudar a não se preocupar se ele pode ou não postar alguma coisa.

### Principais observações do código :snake:
Adicionei a criação de um arquivo PID que rodo a cada 20 minutos para verificar se o script em Python caiu ou não, e salva um arquivo chamado `check.pid` no diretório /tmp/ do linux conforme script abaixo:
```python
# Número PID
pid = str(os.getpid())
# Variável com o caminho onde o arquivo será salvo
pidfile = "/tmp/check.pid"
# Se já houver o arquivo quer dizer que o programa está rodando
if os.path.isfile(pidfile):
    print ("%s already exists, exiting" % pidfile)
    sys.exit()
# Caso contrário abre e salva o arquivo no diretório definido
f = open(pidfile, "w")
f.write(pid)
```

#### Como usar o PID
```python
try:
	# Código inteiro roda aqui
	...
finally:
	# Finaliza o arquivo PID
	os.unlink(pidfile)
```

Esses são os detalhes iniciais do projeto, todo o resto está comentado no próprio script.
Caso crie uma nova versão ou faça algum ajuste avise para que possamos compartilhar este script com mais pessoas.</br></br>
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://github.com/tadeubanzato/fact_check_brasil)
