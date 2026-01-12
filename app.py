"""
Sistema de Controle de Manutenção de Veículos
Aplicação Streamlit para gerenciar veículos e suas manutenções.
"""
import streamlit as st
from datetime import datetime, date
import database as db

# Configuração da página
st.set_page_config(
    page_title="Controle de Manutenção",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Sistema de Controle de Manutenção de Veículos")

# Menu lateral
menu = st.sidebar.selectbox(
    "Menu",
    ["Veículos", "Tipos de Manutenção", "Registrar Manutenção", "Próximas Manutenções"]
)

# ===================== VEÍCULOS =====================
if menu == "Veículos":
    st.header("Gerenciar Veículos")

    # Formulário para adicionar/editar veículo
    with st.expander("➕ Adicionar Novo Veículo", expanded=False):
        with st.form("form_novo_veiculo"):
            col1, col2 = st.columns(2)
            with col1:
                marca = st.text_input("Marca", placeholder="Ex: Fiat")
                modelo = st.text_input("Modelo", placeholder="Ex: Uno")
            with col2:
                ano = st.number_input("Ano", min_value=1900, max_value=datetime.now().year + 1, value=datetime.now().year)
                km = st.number_input("Quilometragem", min_value=0.0, value=0.0, step=100.0)

            if st.form_submit_button("Salvar Veículo"):
                if marca and modelo:
                    db.adicionar_veiculo(marca, modelo, ano, km)
                    st.success(f"Veículo {marca} {modelo} adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha marca e modelo!")

    # Lista de veículos
    st.subheader("Veículos Cadastrados")
    veiculos = db.listar_veiculos()

    if not veiculos:
        st.info("Nenhum veículo cadastrado ainda.")
    else:
        for veiculo in veiculos:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"**{veiculo['marca']} {veiculo['modelo']}** ({veiculo['ano']})")
                    st.caption(f"Quilometragem: {veiculo['km']:,.0f} km")
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{veiculo['id']}"):
                        st.session_state[f"editing_{veiculo['id']}"] = True
                with col3:
                    if st.button("🗑️ Excluir", key=f"del_{veiculo['id']}"):
                        st.session_state[f"confirm_del_{veiculo['id']}"] = True
                with col4:
                    pass

                # Modal de confirmação de exclusão
                if st.session_state.get(f"confirm_del_{veiculo['id']}", False):
                    st.warning(f"Confirma exclusão de {veiculo['marca']} {veiculo['modelo']}?")
                    col_sim, col_nao = st.columns(2)
                    with col_sim:
                        if st.button("Sim, excluir", key=f"confirm_yes_{veiculo['id']}"):
                            db.excluir_veiculo(veiculo['id'])
                            st.session_state[f"confirm_del_{veiculo['id']}"] = False
                            st.rerun()
                    with col_nao:
                        if st.button("Cancelar", key=f"confirm_no_{veiculo['id']}"):
                            st.session_state[f"confirm_del_{veiculo['id']}"] = False
                            st.rerun()

                # Formulário de edição
                if st.session_state.get(f"editing_{veiculo['id']}", False):
                    with st.form(f"form_edit_{veiculo['id']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_marca = st.text_input("Marca", value=veiculo['marca'])
                            new_modelo = st.text_input("Modelo", value=veiculo['modelo'])
                        with col2:
                            new_ano = st.number_input("Ano", min_value=1900, max_value=datetime.now().year + 1, value=veiculo['ano'])
                            new_km = st.number_input("Quilometragem", min_value=0.0, value=float(veiculo['km']), step=100.0)

                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("Salvar"):
                                db.atualizar_veiculo(veiculo['id'], new_marca, new_modelo, new_ano, new_km)
                                st.session_state[f"editing_{veiculo['id']}"] = False
                                st.success("Veículo atualizado!")
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("Cancelar"):
                                st.session_state[f"editing_{veiculo['id']}"] = False
                                st.rerun()

                st.divider()

# ===================== TIPOS DE MANUTENÇÃO =====================
elif menu == "Tipos de Manutenção":
    st.header("Tipos de Manutenção")

    with st.expander("➕ Adicionar Tipo de Manutenção", expanded=False):
        with st.form("form_novo_tipo"):
            nome = st.text_input("Nome da Manutenção", placeholder="Ex: Troca de óleo")

            st.write("**Intervalo (preencha pelo menos um):**")
            col1, col2 = st.columns(2)
            with col1:
                intervalo_km = st.number_input("A cada (km)", min_value=0.0, value=0.0, step=1000.0)
            with col2:
                intervalo_dias = st.number_input("A cada (dias)", min_value=0, value=0, step=30)

            if st.form_submit_button("Salvar Tipo"):
                if nome and (intervalo_km > 0 or intervalo_dias > 0):
                    db.adicionar_tipo_manutencao(
                        nome,
                        intervalo_km if intervalo_km > 0 else None,
                        intervalo_dias if intervalo_dias > 0 else None
                    )
                    st.success(f"Tipo '{nome}' adicionado!")
                    st.rerun()
                else:
                    st.error("Preencha o nome e pelo menos um intervalo!")

    st.subheader("Tipos Cadastrados")
    tipos = db.listar_tipos_manutencao()

    if not tipos:
        st.info("Nenhum tipo de manutenção cadastrado.")
    else:
        for tipo in tipos:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{tipo['nome']}**")
                    intervalo_str = []
                    if tipo.get('intervalo_km'):
                        intervalo_str.append(f"{tipo['intervalo_km']:,.0f} km")
                    if tipo.get('intervalo_dias'):
                        intervalo_str.append(f"{tipo['intervalo_dias']} dias")
                    st.caption(f"Intervalo: {' ou '.join(intervalo_str)}")
                with col2:
                    if st.button("✏️ Editar", key=f"edit_tipo_{tipo['id']}"):
                        st.session_state[f"editing_tipo_{tipo['id']}"] = True
                with col3:
                    if st.button("🗑️ Excluir", key=f"del_tipo_{tipo['id']}"):
                        db.excluir_tipo_manutencao(tipo['id'])
                        st.rerun()

                # Formulário de edição
                if st.session_state.get(f"editing_tipo_{tipo['id']}", False):
                    with st.form(f"form_edit_tipo_{tipo['id']}"):
                        new_nome = st.text_input("Nome", value=tipo['nome'])
                        col1, col2 = st.columns(2)
                        with col1:
                            new_km = st.number_input("Intervalo (km)", min_value=0.0, value=float(tipo.get('intervalo_km') or 0), step=1000.0)
                        with col2:
                            new_dias = st.number_input("Intervalo (dias)", min_value=0, value=int(tipo.get('intervalo_dias') or 0), step=30)

                        if st.form_submit_button("Salvar"):
                            db.atualizar_tipo_manutencao(
                                tipo['id'], new_nome,
                                new_km if new_km > 0 else None,
                                new_dias if new_dias > 0 else None
                            )
                            st.session_state[f"editing_tipo_{tipo['id']}"] = False
                            st.rerun()

                st.divider()

# ===================== REGISTRAR MANUTENÇÃO =====================
elif menu == "Registrar Manutenção":
    st.header("Registrar Manutenção Realizada")

    veiculos = db.listar_veiculos()
    tipos = db.listar_tipos_manutencao()

    if not veiculos:
        st.warning("Cadastre um veículo primeiro!")
    elif not tipos:
        st.warning("Cadastre um tipo de manutenção primeiro!")
    else:
        with st.form("form_registro"):
            # Seleção de veículo
            veiculo_options = {f"{v['marca']} {v['modelo']} ({v['ano']})": v['id'] for v in veiculos}
            veiculo_sel = st.selectbox("Veículo", options=list(veiculo_options.keys()))
            veiculo_id = veiculo_options[veiculo_sel]

            # Seleção de tipo de manutenção
            tipo_options = {t['nome']: t['id'] for t in tipos}
            tipo_sel = st.selectbox("Tipo de Manutenção", options=list(tipo_options.keys()))
            tipo_id = tipo_options[tipo_sel]

            col1, col2 = st.columns(2)
            with col1:
                veiculo = db.obter_veiculo(veiculo_id)
                km_realizada = st.number_input("KM na Manutenção", min_value=0.0, value=float(veiculo['km']), step=100.0)
            with col2:
                data_realizada = st.date_input("Data da Manutenção", value=date.today())

            observacao = st.text_area("Observações", placeholder="Ex: Óleo Mobil 5W30, filtro Mann")

            if st.form_submit_button("Registrar Manutenção"):
                db.adicionar_registro_manutencao(
                    veiculo_id,
                    tipo_id,
                    km_realizada,
                    data_realizada.isoformat(),
                    observacao
                )
                st.success("Manutenção registrada com sucesso!")
                st.rerun()

    # Histórico de manutenções
    st.subheader("Histórico de Manutenções")
    registros = db.listar_registros_manutencao()

    if not registros:
        st.info("Nenhuma manutenção registrada ainda.")
    else:
        for reg in sorted(registros, key=lambda x: x['data_realizada'], reverse=True):
            veiculo = db.obter_veiculo(reg['veiculo_id'])
            tipo = db.obter_tipo_manutencao(reg['tipo_manutencao_id'])

            if veiculo and tipo:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{tipo['nome']}** - {veiculo['marca']} {veiculo['modelo']}")
                        st.caption(f"Data: {reg['data_realizada']} | KM: {reg['km_realizada']:,.0f}")
                        if reg.get('observacao'):
                            st.caption(f"Obs: {reg['observacao']}")
                    with col2:
                        if st.button("🗑️", key=f"del_reg_{reg['id']}"):
                            db.excluir_registro_manutencao(reg['id'])
                            st.rerun()
                    st.divider()

# ===================== PRÓXIMAS MANUTENÇÕES =====================
elif menu == "Próximas Manutenções":
    st.header("Próximas Manutenções")

    veiculos = db.listar_veiculos()
    tipos = db.listar_tipos_manutencao()

    if not veiculos:
        st.warning("Cadastre um veículo primeiro!")
    elif not tipos:
        st.warning("Cadastre um tipo de manutenção primeiro!")
    else:
        # Seleção de veículo
        veiculo_options = {f"{v['marca']} {v['modelo']} ({v['ano']}) - {v['km']:,.0f} km": v['id'] for v in veiculos}
        veiculo_sel = st.selectbox("Selecione o Veículo", options=list(veiculo_options.keys()))
        veiculo_id = veiculo_options[veiculo_sel]
        veiculo = db.obter_veiculo(veiculo_id)

        st.divider()

        # Mostra status de cada tipo de manutenção
        for tipo in tipos:
            resultado = db.calcular_proxima_manutencao(veiculo_id, tipo['id'])

            if resultado:
                with st.container():
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**{resultado['tipo_nome']}**")

                        if resultado['status'] == 'pendente':
                            st.warning("⚠️ Manutenção nunca realizada")
                        elif resultado['status'] == 'vencida':
                            st.error("🚨 Manutenção vencida!")
                            if resultado.get('km_faltante') is not None:
                                st.write(f"Atrasada em {abs(resultado['km_faltante']):,.0f} km")
                            if resultado.get('dias_faltantes') is not None:
                                st.write(f"Atrasada em {abs(resultado['dias_faltantes'])} dias")
                        else:
                            st.success("✅ Em dia")
                            if resultado.get('km_faltante') is not None:
                                st.write(f"Próxima em {resultado['km_faltante']:,.0f} km (aos {resultado['km_proxima']:,.0f} km)")
                            if resultado.get('dias_faltantes') is not None:
                                st.write(f"Próxima em {resultado['dias_faltantes']} dias ({resultado['data_proxima']})")

                    with col2:
                        if st.button("Registrar", key=f"reg_{tipo['id']}"):
                            st.session_state['goto_registrar'] = True
                            st.rerun()

                    st.divider()

# Rodapé
st.sidebar.divider()
st.sidebar.caption("Sistema de Controle de Manutenção v1.0")
