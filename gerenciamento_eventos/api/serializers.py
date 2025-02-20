from rest_framework import serializers
from gerenciamento_eventos.models import Usuario, Evento, Inscricao, Pagamento

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'

class InscricaoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    evento = EventoSerializer(read_only=True)
    pagamento = PagamentoSerializer(read_only=True)

    class Meta:
        model = Inscricao
        fields = '__all__'
