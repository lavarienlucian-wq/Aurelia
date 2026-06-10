import json

from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Contract


FIELD_MAP = {
    'contact_person': ('contact_person', 'contactName'),
    'phone': ('phone',),
    'company_brand': ('company_brand', 'company'),
    'project_type': ('project_type', 'projectType'),
    'expected_quantity': ('expected_quantity', 'quantity'),
    'delivery_city': ('delivery_city', 'city'),
    'budget_range': ('budget_range', 'budget'),
    'requirement_description': ('requirement_description', 'message'),
}


def _get_payload_value(payload, aliases):
    for alias in aliases:
        if alias in payload:
            value = payload[alias]
            return value.strip() if isinstance(value, str) else value
    return ''


@csrf_exempt
def create_contract(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '仅支持 POST 请求。'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': '请求体必须是有效的 JSON。'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'success': False, 'error': '请求体必须是 JSON 对象。'}, status=400)

    data = {
        field_name: _get_payload_value(payload, aliases)
        for field_name, aliases in FIELD_MAP.items()
    }
    errors = {
        field_name: '该字段不能为空。'
        for field_name, value in data.items()
        if not value
    }
    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    contract = Contract.objects.create(**data)
    return JsonResponse(
        {
            'success': True,
            'id': contract.id,
            'message': '需求已提交。',
        },
        status=201,
    )


def vue_frontend(request, spa_path=''):
    index_path = settings.BASE_DIR / 'static' / 'frontend' / 'index.html'
    if not index_path.exists():
        return HttpResponse(
            'Vue frontend is not built. Run "npm.cmd run build" in the frontend directory.',
            status=503,
        )

    return FileResponse(index_path.open('rb'), content_type='text/html')
