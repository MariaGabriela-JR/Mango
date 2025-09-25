from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from scientists.models import Scientist
from patients.models import Patient
from eeg_sessions.models import EEGSession
from datetime import date, timedelta

class EEGSessionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Criar cientista
        self.scientist = Scientist.objects.create_user(
            email="eeg_scientist@test.com",
            password="test123",
            first_name="EEG",
            last_name="Researcher",
            institution="UTFPR",
            specialization="Neuroengineering"
        )
        
        # Criar segundo cientista (para testar isolamento)
        self.other_scientist = Scientist.objects.create_user(
            email="other_scientist@test.com",
            password="test123",
            first_name="Other",
            last_name="Scientist",
            institution="Other Uni",
            specialization="Other Field"
        )
        
        # Criar paciente
        self.patient = Patient.objects.create(
            scientist=self.scientist,
            first_name="EEG Test",
            last_name="Patient",
            email="eeg.patient@test.com",
            birth_date="1998-09-24",
            gender="F"
        )
        
        # Criar sessão de EEG para testes
        self.eeg_session = EEGSession.objects.create(
            scientist=self.scientist,
            patient=self.patient,
            title="Initial Test Session",
            description="Test description",
            status='pending'
        )
        
        # Autenticar como o cientista principal
        self.client.force_authenticate(user=self.scientist)

    def test_create_eeg_session(self):
        """Teste de criação de sessão EEG"""
        url = reverse('eeg-sessions-create')
        data = {
            'title': 'New EEG Session',
            'description': 'Session for emotion recognition',
            'patient': self.patient.id,
            'parameters': {'sample_rate': 256, 'channels': 32}
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EEGSession.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New EEG Session')
        new_session = EEGSession.objects.get(title='New EEG Session')
        self.assertEqual(new_session.status, 'pending')

    def test_create_eeg_session_without_patient(self):
        """Teste de criação de sessão EEG sem paciente"""
        url = reverse('eeg-sessions-create')
        data = {
            'title': 'Session Without Patient',
            'description': 'Test session without patient association'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['patient'])

    def test_list_eeg_sessions(self):
        """Teste de listagem de sessões EEG"""
        # Criar mais uma sessão
        EEGSession.objects.create(
            scientist=self.scientist,
            title='Second Session',
            status='completed'
        )
        
        url = reverse('eeg-sessions-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_eeg_session(self):
        """Teste de visualização de sessão específica"""
        url = reverse('eeg-sessions-detail', kwargs={'pk': self.eeg_session.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Initial Test Session')
        self.assertEqual(response.data['status'], 'pending')

    def test_update_eeg_session(self):
        """Teste de atualização de sessão EEG"""
        url = reverse('eeg-sessions-detail', kwargs={'pk': self.eeg_session.id})
        data = {
            'title': 'Updated Session Title',
            'description': 'Updated description',
            'status': 'in_progress'
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Session Title')
        self.assertEqual(response.data['status'], 'in_progress')

    def test_delete_eeg_session(self):
        """Teste de exclusão de sessão EEG"""
        url = reverse('eeg-sessions-delete', kwargs={'pk': self.eeg_session.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EEGSession.objects.count(), 0)

    def test_sync_fastapi(self):
        """Teste de sincronização com FastAPI"""
        url = reverse('eeg-sessions-sync-fastapi', kwargs={'pk': self.eeg_session.id})
        data = {
            'edf_file_id': '12345678-1234-5678-1234-567812345678',
            'trial_index': 1,
            'start_time': 1627833600.0,
            'duration': 300.5,
            'emotion_category': 'happy',
            'parameters': {'analysis': 'complete', 'confidence': 0.95},
            'status': 'completed'
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se os dados foram atualizados
        self.eeg_session.refresh_from_db()
        self.assertEqual(self.eeg_session.status, 'completed')
        self.assertEqual(self.eeg_session.emotion_category, 'happy')
        self.assertEqual(self.eeg_session.trial_index, 1)

    def test_change_status(self):
        """Teste de mudança de status"""
        url = reverse('eeg-sessions-change-status', kwargs={'pk': self.eeg_session.id})
        data = {'status': 'completed'}
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_update_data(self):
        """Teste de atualização de dados da sessão"""
        url = reverse('eeg-sessions-update-data', kwargs={'pk': self.eeg_session.id})
        data = {
            'title': 'New Title',
            'description': 'New description',
            'emotion_category': 'surprise'
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'New Title')
        self.assertEqual(response.data['emotion_category'], 'surprise')

    def test_list_by_patient(self):
        """Teste de listagem por paciente"""
        # Criar outra sessão para o mesmo paciente
        EEGSession.objects.create(
            scientist=self.scientist,
            patient=self.patient,
            title='Second Session for Patient',
            status='pending'
        )
        
        url = reverse('eeg-sessions-by-patient', kwargs={'patient_id': self.patient.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_by_status(self):
        """Teste de listagem por status"""
        # Criar sessões com diferentes status
        EEGSession.objects.create(
            scientist=self.scientist,
            title='Completed Session',
            status='completed'
        )
        EEGSession.objects.create(
            scientist=self.scientist,
            title='Another Pending',
            status='pending'
        )
        
        url = reverse('eeg-sessions-by-status', kwargs={'status': 'pending'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # A inicial + a nova pending

    def test_isolation_between_scientists(self):
        """Teste que cientistas não veem sessões de outros"""
        # Criar sessão com outro cientista
        other_session = EEGSession.objects.create(
            scientist=self.other_scientist,
            title='Other Scientist Session',
            status='pending'
        )
        
        # Tentar acessar sessão do outro cientista
        url = reverse('eeg-sessions-detail', kwargs={'pk': other_session.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        """Teste de acesso não autenticado"""
        self.client.logout()
        
        url = reverse('eeg-sessions-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_patient_association(self):
        """Teste com paciente que não pertence ao cientista"""
        # Criar paciente com outro cientista
        other_patient = Patient.objects.create(
            scientist=self.other_scientist,
            first_name='Other',
            last_name='Patient',
            birth_date=date.today() - timedelta(days=30*365),
            gender='M'
        )
        
        url = reverse('eeg-sessions-create')
        data = {
            'title': 'Invalid Patient Session',
            'patient': other_patient.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)