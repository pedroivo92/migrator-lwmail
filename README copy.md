# Integrador

Este � um documento auxiliar para configura��o de ambiente e gera��o de build.

## Pr�-requisitos

* Python 3.7
* Pip 21.0.1 ou superior (garanta que o pip esteja apontando para a vers�o correta do Python)
* Docker
* Virtualenv (instale preferencialmente usando o Pip)

## Para executar a aplica��o no ambiente de desenvolvimento

Para executar a aplica��o v� na pasta raiz do projeto (globo-integrator) e execute o seguinte comando.

```
python3 -m venv venv
```

Em seguida acesse seu ambiente virual com o comando a seguir.

```
source venv_api/bin/activate
source venv_service/bin/activate
```


Os comandos dependem da sua instala��o e sistema operacional, se atente a isso.
Ap�s criar seu ambiente virtual, instale as dependencias do projeto com o seguinte comando, usando o comando 'pip' ou 'pip3'.

```
pip install -r requirements.txt

```

Agora seu ambiente virtual est� configurado e com todas as depend�ncias do projeto.
Para acessos ao banco utilize o container docker 'mariadb' j� configurado no arquivo 'docker-compose.yml'.

Caso queira executar a aplica��o por completo diretamente do docker basta executar o comando.

```
docker-compose up -d
```

Caso queira subir a aplicação com novo build

```
docker-compose up --build
```




