from app.models.sqlite.movimentos_phc import PHCMovimento
from app.models.sqlite.conta_bancaria import ContaBancaria
from app.schemas.phc_entries import PHCEntry
from app.db_info import get_entries_by_date

from app.services.messages import mensagem_debug, mensagem_error, mensagem_sucess
from app.session import get_session


def importar_movimentos_phc(ano: int, mes: int):

    debug = False

    with get_session() as session:

        ano_mes = f"{ano:04d}{mes:02d}"

        deleted_entries = {}
        new_entries = {}

        contas = session.query(ContaBancaria).all()

        for conta in contas:
            if debug:
                mensagem_debug(f"\n ▶️ A processar conta \033[94m{conta.conta_phc}\033[0m - \033[94m{conta.nome_conta}\033[0m")

            success, msg, movimentos_raw = get_entries_by_date(ano, mes)

            if not success:
                mensagem_error(f"Erro ao procurar movimentos: {msg}")
                continue

            # Apenas os movimentos da conta atual
            movimentos_filtrados = [m for m in movimentos_raw if m.get("Conta") == conta.conta_phc]

            # Adicionar ao deleted_entries quantos movimentos existem
            deleted_entries[conta.conta_phc] = session.query(PHCMovimento).filter_by(
                conta_phc=conta.conta_phc,
                ano_mes=ano_mes
            ).count()

            # Apagar os que já existem para esta conta e período
            session.query(PHCMovimento).filter_by(
                conta_phc=conta.conta_phc,
                ano_mes=ano_mes
            ).delete()

            if debug:
                mensagem_debug(f"\033[91mEliminados {deleted_entries[conta.conta_phc]} movimentos\033[0m da conta \033[94m{conta.nome_conta}\033[0m para o mês de \033[94m{mes}/{ano}\033[0m")

            for m in movimentos_filtrados:
                try:
                    entrada = PHCEntry(**m)  # Validação e limpeza com Pydantic
                    movimento = PHCMovimento(
                        data=entrada.data,
                        diario=entrada.diario,
                        lancamento=entrada.numero,
                        documento=entrada.documento,
                        descricao=entrada.descricao,
                        debito=entrada.debito,
                        credito=entrada.credito,
                        centro_custo=entrada.centro_custo,
                        conta_phc=entrada.conta,
                        nome_conta_phc=entrada.nome_conta,
                        valor=entrada.valor,
                        abs_valor=entrada.abs_valor,
                        id_interna=entrada.id_interna,
                        observacoes=entrada.observacoes,
                        ano_mes=ano_mes,
                        id_conta_bancaria=conta.id
                    )
                    session.add(movimento)
                    new_entries[conta.conta_phc] = new_entries.get(conta.conta_phc, 0) + 1
                except Exception as e:
                    mensagem_error(f"Erro ao importar movimento: {e}")
                    continue

            if debug:
                mensagem_debug(f"\033[92mImportados {new_entries[conta.conta_phc]} movimentos\033[0m da conta \033[94m{conta.nome_conta}\033[0m para o mês de \033[94m{mes}/{ano}\033[0m")

        session.commit()
        session.close()
        mensagem_sucess(f"Movimentos do PHC importados com sucesso para o mês de \033[94m{mes:02d}/{ano}\033[0m")

    return {'Movimentos apagados': deleted_entries, 'Movimentos importados': new_entries}
