# Python backend challenge

Este é um projeto para demonstração de um micro-serviço RESTful fictício.

As duas primeiras tarefas são obrigatórias as duas últimas são opcionais.

Quando finalizar abra um PR para esse repositório descrevendo sua solução com o máximo de detalhes que puder. boa sorte !!!

## Tarefas:

### 1. Crie um endpoint para retornar informações sobre o serviço.
Para testar rapidamente se nosso serviço está funcionando, crie um endpoint GET /about que retorna uma mensagem confirmando que nosso serviço está funcionando e recebendo requisições.

### 2. Integração com OpenWeatherMap.
Vamos usar o OpenWeatherMap para obter informações do clima de uma cidade.

Primeiro, faça um registro rápido no OpenWeatherMaps para obter uma API Key.

Agora, crie um endpoint GET /weather no nosso micro-serviço que aceite o parâmetro city e retorne os detalhes do tempo na cidade (ensolarado, nublado, etc) e detalhes meteorológicos (temperatura, pressão, etc), utilizando requisições HTTP para o OpenWeatherMaps.

Estruture a resposta da maneira que achar mais organizada.

Sugestão: Pesquise alguma biblioteca de requisições HTTP robusta.

### 3. Cache
Adicione cache na chamada ao servidor do OpenWeatherMaps para tornar nosso micro-serviço mais rápido.

### 4. Tolerância a falhas
Se por algum motivo o serviço do OpenWeatherMaps estiver indisponível, não deveríamos deixar que nosso micro-serviço seja afetado.

Para isso, podemos adicionar uma biblioteca de controle de falhas chamada [circuitbreaker](https://pypi.org/project/circuitbreaker/).

Nessa etapa, adicione e configure o "circuitbreaker" para tornar nosso micro-serviço mais robusto.

Em caso de falha... o que poderia acontecer para que o nosso endpoint não retorne apenas uma resposta de erro genérica?
