import discord
from discord import app_commands
import datetime

# Cole o ID do cargo do seu servidor aqui (apenas números)
CARGO_MATRICULADO_ID =1568000204655960265
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class MatriculaModal(discord.ui.Modal, title="Formulário de Matrícula"):
    nome = discord.ui.TextInput(
        label="Nome Completo",
        placeholder="Digite seu nome completo...",
        max_length=100
    )
    idade = discord.ui.TextInput(
        label="Idade",
        placeholder="Ex: 18",
        max_length=3
    )
    id_aluno = discord.ui.TextInput(
        label="ID / Matrícula",
        placeholder="Digite seu ID...",
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Evita erro de tempo limite (timeout) do Discord
        await interaction.response.defer(ephemeral=True)

        user_nome = self.nome.value
        user_idade = self.idade.value
        user_id_aluno = self.id_aluno.value
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Formata o texto para salvar no arquivo .txt
        linha_registro = f"[{data_atual}] Nome: {user_nome} | Idade: {user_idade} | ID: {user_id_aluno}\n"

        try:
            # Salva os dados no arquivo matriculas.txt local
            with open("matriculas.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(linha_registro)

            # Atribui o cargo automaticamente
            guild = interaction.guild
            cargo_status = ""
            
            if guild and CARGO_MATRICULADO_ID:
                cargo = guild.get_role(CARGO_MATRICULADO_ID)
                if cargo:
                    try:
                        await interaction.user.add_roles(cargo)
                        cargo_status = f" e o cargo **{cargo.name}** foi atribuído a você!"
                    except Exception:
                        cargo_status = ", mas houve um erro ao dar o cargo (verifique as permissões do bot)."
                else:
                    cargo_status = ", mas o ID do cargo configurado não foi encontrado no servidor."

            await interaction.followup.send(
                f"✅ Matrícula realizada com sucesso, **{user_nome}**! Seus dados foram salvos{cargo_status}",
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Erro ao salvar o registro no arquivo: {e}",
                ephemeral=True
            )

@tree.command(name="matricula", description="Abre o formulário para realizar a sua matrícula.")
async def matricula(interaction: discord.Interaction):
    await interaction.response.send_modal(MatriculaModal())

@client.event
async def on_ready():
    await tree.sync()
    print(f'Bot online e sincronizado como {client.user}!')

# Insira o Token do seu bot do Discord aqui
client.run('MTU2ODAxNDI4OTgzNzYyMTI5OA.G02sWy.Jtf3V5gJzX2d1-tKzyuZAg7j4ZXQwhTBNsgl1c')
