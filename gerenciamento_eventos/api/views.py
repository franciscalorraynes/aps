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

class PagamentoViewSet(ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

class InscricaoViewSet(ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer

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

            # Criar solicitação de devolução (aqui pode ser um novo modelo ou flag)
            inscricao.status = "pendente"  # Simulando uma solicitação em análise
            inscricao.save()

            # Simulação do envio para administração
            # Aqui poderia haver um sistema de notificação para os administradores

            return Response({"detail": "Sua solicitação de devolução foi enviada para análise."}, status=status.HTTP_200_OK)

        except Inscricao.DoesNotExist:
            return Response({"detail": "Inscrição não encontrada."}, status=status.HTTP_404_NOT_FOUND)
