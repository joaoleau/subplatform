
# Subscription Platform
- O projeto ainda esta em desenvolvimento e ainda será implementado as devidas funcionalidades!


## Rodando localmente

### Clone o projeto

```bash
  git clone https://github.com/joaoleau/subplatform.git
```

### Entre no diretório do projeto

```bash
  cd subplatform
```

### Ambiente Virtual Python

```bash
  python -m venv venv
```

### Ative o ambiente virtual
- No Windows:
```bash
  venv\Scripts\activate
```

- No Unix ou MacOS:
```bash
  source venv/bin/activate
```

### Instale as dependências

```bash
  pip install -r requirements.txt
```

### Configure as variaveis de ambiente
Faça os devidos ajustes no arquivo ".env-example" e depois altere seu nome para ".env"

### Faça as migrações

```bash
  python .manage.py migrate
```

### Inicie o projeto

```bash
  python .manage.py runserver
```


## Autores

- [@joaoleau](https://www.github.com/joaoleau)