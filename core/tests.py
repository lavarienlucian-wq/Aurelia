import json

from django.test import TestCase

from .models import Contract


class ContractApiTests(TestCase):
    def test_create_contract_from_vue_payload(self):
        response = self.client.post(
            '/api/contracts/',
            data=json.dumps(
                {
                    'contactName': '张三',
                    'phone': '13800138000',
                    'company': '朗境合作品牌',
                    'projectType': '工程批量',
                    'quantity': '51-200 件',
                    'city': '上海',
                    'budget': '30-80 万',
                    'message': '需要客厅和卧室成套家具报价。',
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contract.objects.count(), 1)

        contract = Contract.objects.get()
        self.assertEqual(contract.contact_person, '张三')
        self.assertEqual(contract.company_brand, '朗境合作品牌')
        self.assertEqual(contract.requirement_description, '需要客厅和卧室成套家具报价。')

    def test_create_contract_requires_all_fields(self):
        response = self.client.post(
            '/api/contracts/',
            data=json.dumps({'contactName': '张三'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Contract.objects.count(), 0)
        self.assertIn('phone', response.json()['errors'])
