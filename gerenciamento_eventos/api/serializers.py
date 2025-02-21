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
    class Meta:
        model = Inscricao
        fields = ['usuario', 'evento', 'pagamento', 'status', 'data_inscricao']  # Exclua os campos relacionados que são read_only

    def create(self, validated_data):
        # Aqui você pode criar a inscrição com base nos dados validados
        return Inscricao.objects.create(**validated_data)


    class Meta:
        model = Inscricao
        fields = '__all__'
