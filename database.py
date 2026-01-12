"""
Módulo de persistência de dados usando JSON.
"""
import json
import os
from datetime import datetime
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
VEICULOS_FILE = os.path.join(DATA_DIR, "veiculos.json")
MANUTENCOES_FILE = os.path.join(DATA_DIR, "manutencoes.json")
REGISTROS_FILE = os.path.join(DATA_DIR, "registros_manutencao.json")


def _garantir_diretorio():
    """Garante que o diretório de dados existe."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _carregar_json(arquivo: str) -> list:
    """Carrega dados de um arquivo JSON."""
    _garantir_diretorio()
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _salvar_json(arquivo: str, dados: list):
    """Salva dados em um arquivo JSON."""
    _garantir_diretorio()
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def _proximo_id(lista: list) -> int:
    """Retorna o próximo ID disponível."""
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


# ===================== VEÍCULOS =====================

def listar_veiculos() -> list:
    """Lista todos os veículos."""
    return _carregar_json(VEICULOS_FILE)


def obter_veiculo(veiculo_id: int) -> Optional[dict]:
    """Obtém um veículo pelo ID."""
    veiculos = listar_veiculos()
    for v in veiculos:
        if v["id"] == veiculo_id:
            return v
    return None


def adicionar_veiculo(marca: str, modelo: str, ano: int, km: float) -> dict:
    """Adiciona um novo veículo."""
    veiculos = listar_veiculos()
    novo = {
        "id": _proximo_id(veiculos),
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "km": km,
        "criado_em": datetime.now().isoformat()
    }
    veiculos.append(novo)
    _salvar_json(VEICULOS_FILE, veiculos)
    return novo


def atualizar_veiculo(veiculo_id: int, marca: str, modelo: str, ano: int, km: float) -> Optional[dict]:
    """Atualiza um veículo existente."""
    veiculos = listar_veiculos()
    for v in veiculos:
        if v["id"] == veiculo_id:
            v["marca"] = marca
            v["modelo"] = modelo
            v["ano"] = ano
            v["km"] = km
            v["atualizado_em"] = datetime.now().isoformat()
            _salvar_json(VEICULOS_FILE, veiculos)
            return v
    return None


def excluir_veiculo(veiculo_id: int) -> bool:
    """Exclui um veículo e seus registros de manutenção."""
    veiculos = listar_veiculos()
    veiculos_filtrados = [v for v in veiculos if v["id"] != veiculo_id]
    if len(veiculos_filtrados) < len(veiculos):
        _salvar_json(VEICULOS_FILE, veiculos_filtrados)
        # Remove registros de manutenção do veículo
        registros = listar_registros_manutencao()
        registros_filtrados = [r for r in registros if r["veiculo_id"] != veiculo_id]
        _salvar_json(REGISTROS_FILE, registros_filtrados)
        return True
    return False


# ===================== TIPOS DE MANUTENÇÃO =====================

def listar_tipos_manutencao() -> list:
    """Lista todos os tipos de manutenção."""
    return _carregar_json(MANUTENCOES_FILE)


def obter_tipo_manutencao(manutencao_id: int) -> Optional[dict]:
    """Obtém um tipo de manutenção pelo ID."""
    manutencoes = listar_tipos_manutencao()
    for m in manutencoes:
        if m["id"] == manutencao_id:
            return m
    return None


def adicionar_tipo_manutencao(nome: str, intervalo_km: Optional[float], intervalo_dias: Optional[int]) -> dict:
    """Adiciona um novo tipo de manutenção."""
    manutencoes = listar_tipos_manutencao()
    novo = {
        "id": _proximo_id(manutencoes),
        "nome": nome,
        "intervalo_km": intervalo_km,
        "intervalo_dias": intervalo_dias,
        "criado_em": datetime.now().isoformat()
    }
    manutencoes.append(novo)
    _salvar_json(MANUTENCOES_FILE, manutencoes)
    return novo


def atualizar_tipo_manutencao(manutencao_id: int, nome: str, intervalo_km: Optional[float], intervalo_dias: Optional[int]) -> Optional[dict]:
    """Atualiza um tipo de manutenção existente."""
    manutencoes = listar_tipos_manutencao()
    for m in manutencoes:
        if m["id"] == manutencao_id:
            m["nome"] = nome
            m["intervalo_km"] = intervalo_km
            m["intervalo_dias"] = intervalo_dias
            m["atualizado_em"] = datetime.now().isoformat()
            _salvar_json(MANUTENCOES_FILE, manutencoes)
            return m
    return None


def excluir_tipo_manutencao(manutencao_id: int) -> bool:
    """Exclui um tipo de manutenção."""
    manutencoes = listar_tipos_manutencao()
    manutencoes_filtradas = [m for m in manutencoes if m["id"] != manutencao_id]
    if len(manutencoes_filtradas) < len(manutencoes):
        _salvar_json(MANUTENCOES_FILE, manutencoes_filtradas)
        return True
    return False


# ===================== REGISTROS DE MANUTENÇÃO =====================

def listar_registros_manutencao(veiculo_id: Optional[int] = None) -> list:
    """Lista registros de manutenção, opcionalmente filtrados por veículo."""
    registros = _carregar_json(REGISTROS_FILE)
    if veiculo_id:
        return [r for r in registros if r["veiculo_id"] == veiculo_id]
    return registros


def adicionar_registro_manutencao(veiculo_id: int, tipo_manutencao_id: int, km_realizada: float, data_realizada: str, observacao: str = "") -> dict:
    """Adiciona um registro de manutenção realizada."""
    registros = listar_registros_manutencao()
    novo = {
        "id": _proximo_id(registros),
        "veiculo_id": veiculo_id,
        "tipo_manutencao_id": tipo_manutencao_id,
        "km_realizada": km_realizada,
        "data_realizada": data_realizada,
        "observacao": observacao,
        "criado_em": datetime.now().isoformat()
    }
    registros.append(novo)
    _salvar_json(REGISTROS_FILE, registros)
    return novo


def excluir_registro_manutencao(registro_id: int) -> bool:
    """Exclui um registro de manutenção."""
    registros = listar_registros_manutencao()
    registros_filtrados = [r for r in registros if r["id"] != registro_id]
    if len(registros_filtrados) < len(registros):
        _salvar_json(REGISTROS_FILE, registros_filtrados)
        return True
    return False


def calcular_proxima_manutencao(veiculo_id: int, tipo_manutencao_id: int) -> Optional[dict]:
    """
    Calcula quando será a próxima manutenção.
    Retorna dict com 'km_faltante' e/ou 'dias_faltantes'.
    """
    veiculo = obter_veiculo(veiculo_id)
    tipo = obter_tipo_manutencao(tipo_manutencao_id)

    if not veiculo or not tipo:
        return None

    # Busca último registro dessa manutenção para o veículo
    registros = listar_registros_manutencao(veiculo_id)
    registros_tipo = [r for r in registros if r["tipo_manutencao_id"] == tipo_manutencao_id]

    resultado = {
        "tipo_nome": tipo["nome"],
        "km_faltante": None,
        "dias_faltantes": None,
        "status": "ok"
    }

    if not registros_tipo:
        # Nunca fez essa manutenção
        resultado["status"] = "pendente"
        resultado["mensagem"] = "Manutenção nunca realizada"
        return resultado

    # Ordena por data e pega o mais recente
    registros_tipo.sort(key=lambda x: x["data_realizada"], reverse=True)
    ultimo = registros_tipo[0]

    # Calcula por KM
    if tipo["intervalo_km"]:
        km_proxima = ultimo["km_realizada"] + tipo["intervalo_km"]
        km_faltante = km_proxima - veiculo["km"]
        resultado["km_faltante"] = km_faltante
        resultado["km_proxima"] = km_proxima
        if km_faltante <= 0:
            resultado["status"] = "vencida"

    # Calcula por dias
    if tipo["intervalo_dias"]:
        from datetime import datetime, timedelta
        data_ultima = datetime.fromisoformat(ultimo["data_realizada"])
        data_proxima = data_ultima + timedelta(days=tipo["intervalo_dias"])
        dias_faltantes = (data_proxima - datetime.now()).days
        resultado["dias_faltantes"] = dias_faltantes
        resultado["data_proxima"] = data_proxima.strftime("%d/%m/%Y")
        if dias_faltantes <= 0:
            resultado["status"] = "vencida"

    return resultado
