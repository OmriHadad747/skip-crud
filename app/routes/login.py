from app.routes import login_router
from app.services.login import Login




@login_router.post()
def login():
    pass
    # return Login.login(request.json)
