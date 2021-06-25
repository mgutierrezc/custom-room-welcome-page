from pathlib import Path
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='')


labels = Path('labels.txt').read_text('utf8').split()

print('labels:', labels)

OTREE_SERVER = "http://cgr-bid.econ.columbia.edu"
ROOM_NAME = 'test_room'


def homepage(request: Request):
    label = request.query_params.get('participant_label', '')
    wrong_label = False
    if label:
        if label in labels:
            return RedirectResponse(
                f'{OTREE_SERVER}/room/{ROOM_NAME}?participant_label={label}'
            )
        wrong_label = True
    return templates.TemplateResponse(
        'RoomInputLabel.html',
        dict(request=request, wrong_label=wrong_label, label=label),
    )


app = Starlette(debug=True, routes=[Route('/', homepage)])
