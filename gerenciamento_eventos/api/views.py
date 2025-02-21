from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from gerenciamento_eventos.models import Usuario, Evento, Inscricao, Pagamento
from gerenciamento_eventos.api.serializers import UsuarioSerializer, EventoSerializer, InscricaoSerializer, PagamentoSerializer

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class EventoViewSet(ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def create(self, request, *args, **kwargs):
        """Impede a criação de eventos duplicados."""
        nome = request.data.get('nome', '').strip()
        data = request.data.get('data', '').strip()
        local = request.data.get('local', '').strip()

        if not nome or not data or not local:
            return Response({"detail": "Todos os campos (nome, data e local) são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        if Evento.objects.filter(nome=nome, data=data, local=local).exists():
            return Response({"detail": "Esse evento já está cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class PagamentoViewSet(ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

class InscricaoViewSet(ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer

    def create(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario')
        evento_id = request.data.get('evento')
        pagamento_id = request.data.get('pagamento')

        if not Usuario.objects.filter(id=usuario_id).exists():
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if not Evento.objects.filter(id=evento_id).exists():
            return Response({"detail": "Evento não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if not Pagamento.objects.filter(id=pagamento_id).exists():
            return Response({"detail": "Pagamento não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def solicitar_devolucao(self, request, pk=None):
        """Rota personalizada para solicitar a devolução"""
        try:
            inscricao = self.get_object()

            # Verifica se o usuário autenticado é o dono da inscrição
            if inscricao.usuario != request.user:
                return Response({"detail": "Permissão negada."}, status=status.HTTP_403_FORBIDDEN)

            # Verifica se o usuário é elegível para devolução
            if inscricao.status != "confirmado":
                return Response({"detail": "Você não pode solicitar devolução para esta inscrição."}, status=status.HTTP_400_BAD_REQUEST)

            # Criar solicitação de devolução (simulando uma solicitação em análise)
            inscricao.status = "pendente"
            inscricao.save()

            # Aqui poderia haver um sistema de notificação para os administradores

            return Response({"detail": "Sua solicitação de devolução foi enviada para análise."}, status=status.HTTP_200_OK)

        except Inscricao.DoesNotExist:
            return Response({"detail": "Inscrição não encontrada."}, status=status.HTTP_404_NOT_FOUND)
