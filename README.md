# Python :snake:, Telegram <img src="https://logos-download.com/wp-content/uploads/2016/07/Telegram_logo.png" width="40" height="40"> e Democracia :fire:

A idéia principal desse script é postar em um canal aberto e público do Telegram toda vez que um novo Fact Check é feito nos principais canais de checagem de fatos do Brasil.

*Preciso deixar claro, não desenvolvedor então há oportunidades óbvias de melhoria no código então qualquer um pode ajudar a melhorar o que foi desenvolvido*. :sunglasses:

### Os canais que estão sendo manitorados são:
- Agência Lupa - https://piaui.folha.uol.com.br/lupa/
- UOL Confere - https://noticias.uol.com.br/confere
- Projeto Comprova - https://projetocomprova.com.br/
- G1 Fato ou Fake - https://g1.globo.com/fato-ou-fake/
- G1 Fato ou Fake (Corona Virus) - https://g1.globo.com/fato-ou-fake/coronavirus/
- Estadão Verifica - https://politica.estadao.com.br/blogs/estadao-verifica/
- Aos Fatos - https://www.aosfatos.org/noticias/nas-redes/
- Boatos - https://www.boatos.org/

## Vamos aos comentários do código:
### Setup
Esse script está rodando em uma Raspberry Pi com linux por isso desenvolvi um Shell script para verificar se o script está rodando a cada 15 minutos. Caso o script pare ele reinicia automaticamente.

### Python Requirements
Para instalar os requirements rode o comando `sudo pip3 install -r requirements.txt`.
Este comando instalará as seguintes bibliotecas do Python:
- Pandas
- Telegram
- xmltodict

### O shell script para fazer essas verificações é súper simples e segue abaixo:
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
### API do Telegram
Para rodar o programa é preciso criar um Token Key para o Telegram, para fazer isso procure o usuário BotFather no telegram
<img src="https://cdn-images-1.medium.com/max/1600/1*XolFpjck53uWNRG8dOZz7w.png" width="100" height="100">

Ao encontrar o BotFather digite o seguinte comando
`/newbot` - Para criar um novo bot
`/setname` - Para dar nome ao bot
`/setdescription` - Para criar a descrição do bot
`/setyourpic` - Para adicionar uma foto ao bot (eu usei o https://thispersondoesnotexist.com/ um projeto muito massa que cria foto de pessoas que não existem)
`/token` - Para criar e verificar o API Token do seu robô
`/setprivacy` - Aqui você tem que desligar a privacy para poder deixar o robô postar em um Canal do Telegram ou Groupo

Depois de feito isso você tem que criar um Canal ou um Grupo do Telegram com seu usuário e adicionar o robô. Eu geralmente adiciono o robô como administrador o que ajudar a não se preocupar se ele pode ou não postar alguma coisa.

### Python
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
```python
try:
	# Código inteiro roda aqui
	...
finally:
	# Finaliza o arquivo PID
	os.unlink(pidfile)
```

