from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=255)
    data = models.DateField()
    local = models.CharField(max_length=255)
    capacidade = models.PositiveIntegerField()
    
    def __str__(self):
        return self.nome

class Pagamento(models.Model):
    valor = models.FloatField()
    data = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('pago', 'Pago'), ('cancelado', 'Cancelado')],
        default='pendente'
    )
    
    def __str__(self):
        return f"Pagamento {self.id} - {self.status}"

class Inscricao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inscricoes')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('cancelado', 'Cancelado')],
        default='pendente'
    )
    data_inscricao = models.DateField(auto_now_add=True)
    pagamento = models.OneToOneField(Pagamento, on_delete=models.CASCADE, related_name='inscricao')
    
    def __str__(self):
        return f"{self.usuario.nome} - {self.evento.nome}"
