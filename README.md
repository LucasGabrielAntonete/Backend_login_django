# safe-login-backend

Tutorial de como fazer um CRUD completo de usuario.

Neste tutorial você vai aprender:
- Como fazer um *Cadastro* e *Login* de Usuarios.
- Como utilizar a API do Google para *Cadastro* e *Login*


# 1. Modificando o usuário padrão do Django

Utilizaremos uma estratégia simples para a inclusão de campos ao usuário padrão do Django. Essa estratégia terá as seguintes características:

-   **Substituiremos** a classe `User` padrão do Django pela nossa própria classe `Usuario`.
-   **Não removeremos** os campos padrão do usuário.
-   **Incluiremos** os campos que precisamos no nosso usuário.
-   **Removeremos** o banco de dados e criaremos um novo, perdendo todos os dados.
-   Faremos a **migração** do banco de dados.
-   Modificaremos o **Admin** para que ele utilize a nossa classe `Usuario` e não a classe `User` padrão.
-   Em nosso exemplo, incluiremos os campos `cpf`, `telefone` e `data_nascimento` ao usuário.
-   Posteriormente, incluiremos a foto do usuário.


**Instalando o setuptools**

-   Instale o pacote `setuptools`:

```shell
pdm add setuptools
```

**Instalando a app `usuario`**

-   Baixe e descompacte o arquivo com a app pronta para ser utilizada:

```shell
wget https://github.com/marrcandre/django-drf-tutorial/raw/main/apps/usuario.zip -O usuario.zip && unzip usuario.zip && rm usuario.zip
```

No `Windows`, execute os seguintes comandos no `PowerShell`:

```shell
Invoke-WebRequest -Uri https://github.com/marrcandre/django-drf-tutorial/raw/main/apps/usuario.zip -OutFile usuario.zip
```

```shell
Expand-Archive -Path usuario.zip -DestinationPath .
```

```shell
Remove-Item -Force usuario.zip
```

A pasta ficará assim:

```
usuario
├── admin.py
├── apps.py
├── forms.py
├── __init__.py
├── managers.py
├── migrations
│   └── __init__.py
├── models.py
├── router.py
├── serializers.py
└── views.py
```

**Adicionando a app `usuario` ao projeto**

-   Edite o arquivo `settings.py` e inclua a app `usuario` na lista de apps instaladas:

```python
INSTALLED_APPS = [
    ...
    "usuario", # inclua essa linha
    "livraria",
]
```

-   Edite o arquivo `settings.py` e inclua a configuração abaixo:

```python
AUTH_USER_MODEL = "usuario.Usuario"
```

> Essa configuração indica ao Django que a classe `Usuario` da app `usuario` será utilizada como classe de usuário padrão.

-   Edite o arquivo `urls.py` e inclua as rotas da app `usuario`:

```python
...
from usuario.router import router as usuario_router
...

urlpatterns = [
    ...
    path("api/", include(usuario_router.urls)),
]
```

> Ela será acessada através da rota `/api/usuario/`.

**Removendo arquivos temporários, migrations e o banco de dados**

```shell
find . -name "__pycache__" -type d -exec rm -r {} +
find . -path "*/migrations/*.pyc" -delete
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
rm -rf __pypackages__ pdm.lock
rm db.sqlite3
```

**Reinstalando as dependências**

```shell
pdm install
```

**Criando o banco de dados e executando as migrações**

-   Crie novamente o banco de dados e execute as migrações:

```shell
pdm run python manage.py makemigrations
pdm run python manage.py migrate
```

**Criando um novo usuário**

-   Crie um novo superusuário:

```shell
pdm run python manage.py createsuperuser
```

# 2. Mudanças no Usuario.

Fazer as alterações.

# 3. Autenticação com o SimpleJWT

Vamos utilizar o **SimpleJWT** para a autenticação no **Django REST Framework**.

> **Resumindo**, utilizaremos o **SimpleJWT** para _autenticação_ e a _estrutura de permissões do Django_ para **autorização**.

**O SimpleJWT**

O [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) é um plug-in de autenticação JSON Web Token para o Django REST Framework.

**Instalação e configuração**

-   Para instalar o SimpleJWT, execute o seguinte comando:

```shell
pdm add djangorestframework-simplejwt
```

-   Adicione o `SimpleJWT` no arquivo `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "rest_framework_simplejwt",
    ...
]
```

-   Adicione o `SimpleJWT` no arquivo `settings.py`:

```python
REST_FRAMEWORK = {
    ...
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    ...
}
```

-   Adicione o `SimpleJWT` no arquivo `urls.py`:

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ...
]
```

-   Feitas essas alterações, coloque o servidor do Django novamente em execução.

-   # 4. Criando Login

-   Para criarmos o login nós precisamos criar um arquivo chamado *login* dentro da pasta *usuario*

-   Para deixar tudo um pouco mais organizado vamos criar uma pasta chamada *utils* e colocaremos o arquivo *login* dentro.

-   O nosso código será o seguinte:

   ```python
    from rest_framework.decorators import api_view, authentication_classes, permission_classes
    from rest_framework.permissions import AllowAny
    from rest_framework.response import Response
    from django.utils.translation import gettext_lazy as _
    from rest_framework.permissions import AllowAny
    from rest_framework.response import Response
    from rest_framework import status
    from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
    from django.contrib.auth import authenticate, get_user_model
    import json
    User = get_user_model()


    @api_view(['POST'])
    @authentication_classes([])
    @permission_classes([AllowAny]) 

    def login(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get("email", '')
    password = data.get("password", '')
    print(email, password)
    if email is not None and password is not None:
        try:
            user = User.objects.get(email=email)
            print(email)
            user = authenticate(email=email, password=password)
        except User.DoesNotExist:
            user = None   
    else:
        return Response(
            {"message": "Credenciais inválidas!"}, status=status.HTTP_400_BAD_REQUEST
        )
    print(user)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(access),
            "email": user.email,
            "id": user.id,
            "message": "Login realizado com sucesso!"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
          return Response(
            {"message": "Credenciais inválidas!"}, status=status.HTTP_400_BAD_REQUEST
        )
    ```

- Explicação:


- # 5: Cadastro

- Para o cadastro nós vamos fazer a mesma coisa que já fizemos com o arquivo *login*:

- Agora o nosso codigo é um pouco mais simples:

 ```python
    from rest_framework.decorators import api_view, authentication_classes, permission_classes
    from rest_framework.permissions import AllowAny
    from rest_framework.response import Response
    from django.utils.translation import gettext_lazy as _
    from rest_framework.response import Response
    from rest_framework import status
    from ..models import Usuario

    @api_view(["POST"])
    @authentication_classes([])
    @permission_classes([AllowAny])

    def cadastro(request):
         email = request.data.get("email")
         password = request.data.get("password")
         full_name = request.data.get("full_name")

         if(Usuario.objects.filter(email=email).exists()):
             return Response({"error": _("Email já cadastrado")}, status=status.HTTP_400_BAD_REQUEST)
         else:
                usuario = Usuario.objects.create(email=email, full_name=full_name)
                usuario.set_password(password)
                usuario.save()
                return Response({"message": _("Usuário cadastrado com sucesso")}, status=status.HTTP_201_CREATED)
   ```

- Explicação: 
    
