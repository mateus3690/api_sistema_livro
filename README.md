# Desafio Mesha

Projeto feito com o back-end em python/ Flask

Instruções:

    Clone o repositório:

     >> git clone https://github.com/mateus3690/api_sistema_livro/

    Inicie fazendo a build para docker

     >> docker build -t flask-api .  

    Em seguida crie o conteiner e que irá ser executado em segundo plano
    
      >> docker run -it --name desafio-mesha -p 8000:8000 -d flask-api 

    Acesse o caminho e com a docmuentação navege nas rotas:

    http://localhost:8000/
