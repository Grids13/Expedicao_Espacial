let baseUrl = "http://127.0.0.1:7000"

$(document).ready(() => {
    renderTable()
})

$("#btnRegisterMission").on("click", () => {
    const missionName = document.getElementById('missionName').value;
    const missionLaunchDate = document.getElementById('missionLaunchDate').value;
    const missionDestination = document.getElementById('missionDestination').value;
    const missionStatus = document.getElementById('missionStatus').value;
    const missionCrew = document.getElementById('missionCrew').value;
    const missionPayload = document.getElementById('missionPayload').value;
    const missionDuration = document.getElementById('missionDuration').value;
    const missionCost = document.getElementById('missionCost').value;
    const missionStatusDescription = document.getElementById('missionStatusDescription').value;

    const newMissionData = {
        nome: missionName,
        data_lancamento: missionLaunchDate,
        destino: missionDestination,
        estado: missionStatus,
        tripulacao: missionCrew,
        carga_util: missionPayload,
        duracao: missionDuration,
        custo: missionCost,
        status: missionStatusDescription
    };

    registerMission(newMissionData)
})

$("#btnEditMission").on("click", async () => {
    const missionId = document.getElementById('editMissionId').value;
    const missionName = document.getElementById('editMissionName').value;
    const missionLaunchDate = document.getElementById('editMissionLaunchDate').value;
    const missionDestination = document.getElementById('editMissionDestination').value;
    const missionStatus = document.getElementById('editMissionStatus').value;
    const missionCrew = document.getElementById('editMissionCrew').value;
    const missionPayload = document.getElementById('editMissionPayload').value;
    const missionDuration = document.getElementById('editMissionDuration').value;
    const missionCost = document.getElementById('editMissionCost').value;
    const missionStatusDescription = document.getElementById('editMissionStatusDescription').value;

    const updatedMissionData = {
        id: missionId,
        nome: missionName,
        data_lancamento: missionLaunchDate,
        destino: missionDestination,
        estado: missionStatus,
        tripulacao: missionCrew,
        carga_util: missionPayload,
        duracao: missionDuration,
        custo: missionCost,
        status: missionStatusDescription
    };

    let updated = await updateMission(updatedMissionData)
    
    if (updated) {
        alert("Missão atualizada com sucesso!")
        $("#btnCloseEditModal").trigger('click')
        renderTable()
    } else {
        alert("Ocorreu um error ao atualizar a missão!")
    }
})

$("#btnPesquisar").on("click", async () => {
    let initialDate = $("#initialDate").val()
    let finalDate = $("#finalDate").val()

    if (!initialDate || !finalDate) {
        alert("Periodo de tempo inválido")
        return
    } 

    $("#tBodyMissions").html("")
    let missions = await searchByDate(initialDate, finalDate)
    console.log(missions)
    if (missions?.length == 0 || !missions || missions.Message) {
        $("#info").html("<span class='d-flex justify-content-center p-4'>Missão não encontrada</span>")
        return
    } 

    missions?.map(mission => { addMissionInTable(mission) })
})

$("#initialDate").on("change", () => {
    let initialDate = new Date($("#initialDate").val())

    if (!initialDate) {
        $("#finalDate").attr("disabled", "true");
        return
    } else {
        $("#finalDate").removeAttr("disabled");
    }    

    $("#finalDate").attr("min", $("#initialDate").val())
    if ($("#finalDate").val() < $("#initialDate").val()) {
        $("#finalDate").val($("#initialDate").val());
    }
})

$("#finalDate").on("blur", () => {
    if ($("#finalDate").val() < $("#finalDate").attr("min")) {
        $("#finalDate").val($("#initialDate").val());
    }
})

async function renderTable() {
    $("#tBodyMissions").html("")
    let missions = await getMissions()
    if (missions?.length == 0 || !missions) {
        $("#info").html("<span class='d-flex justify-content-center p-4'>Sem Missões Atualmente</span>")
        return
    } 
    missions.map(mission => { addMissionInTable(mission) })
}

async function getMissions(){
    let missions = null
    let url = `${baseUrl}/all`
    await fetch(url)
        .then(result => {
            if (result.status == 200) {
                missions = result.json()
            } else {
                alert("Ocorreu um error ao buscar as missões!")
            }        
        })
        .catch(err => {
            console.log("Ocorreu um error", err)
            alert("Ocorreu um error ao buscar as missões!")
        })
    
    return missions
}

async function getMissionsById(missionId){
    let mission = null
    let url = `${baseUrl}/id/${missionId}`
    await fetch(url)
        .then(result => mission = result.json())
        .catch(err => {
            console.log("Ocorreu um error ao buscar missão por id", err)
        })
    
    return mission
}

async function registerMission(data) {
    let url = `${baseUrl}/create`
    await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(result => { 
            if (result.status) {
                $("#btnCloseRegisterModal").trigger('click')
                $("#formRegister").trigger('reset');
                renderTable()
                alert("Missão registrada com sucesso!")
            } else {
                alert("Ocorreu um error ao registrar a missão!")
            }
        })
        .catch(err => {
            console.log("Ocorreu um error", err)
            alert("Ocorreu um error ao registrar a missão!")
        })
}

async function updateMission(data) {
    let url = `${baseUrl}/update`
    let updated = null
    await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(result => {
            result.json().then(r => console.log(r))
            if (result.status == 200){
                updated = true
            }  else {
                updated = false
            }
        })
        .catch(err => {
            console.log("Ocorreu um error", err)
            updated = false
        })

    return updated
}

async function deleteMission(data = {id: null}) {
    if (!data?.id) return false
    let deleted = null
    let url = `${baseUrl}/delete`
    await fetch(url, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(result =>  {
            result.status == 200 ? deleted = true : deleted = false
        })
        .catch(err => {
            console.log("Ocorreu um error", err)
            deleted = false
    })
    return deleted
}

async function searchByDate(initialDate, finalDate) {
    if (!initialDate || !finalDate) return null
    let missions = null
    let url = `${baseUrl}/all?data_inicial=${initialDate}&data_final=${finalDate}`
    await fetch(url)
        .then(result => missions = result.json())
        .catch(err => {
            console.log("Ocorreu um error", err)
            alert("Ocorreu um error ao buscar as missões!")
        })
    
    return missions
}

function addMissionInTable(mission) {
    let row = `<tr> 
        <td class='align-middle'>${mission.id}</td>
        <td class='align-middle'>${mission.nome}</td>
        <td class='align-middle'>${mission.data_lancamento}</td>
        <td class='align-middle'>${mission.destino}</td>
        <td class='align-middle'>${mission.estado}</td>
        <td class='align-middle'>
            <button class="btn btn-warning" onclick="openModalEdit(${mission.id})"> <i class="bi bi-pencil"></i> </button>
            <button class="btn btn-danger" onclick="btnDeleteMission(${mission.id})"> <i class="bi bi-x-circle"></i> </button>
        </td>
    </tr>`

    document.getElementById("tBodyMissions").innerHTML += row
}

async function openModalEdit(missionId) {
    let [mission] = await getMissionsById(missionId)

    if (!mission) {
        alert("Não foi possivel abrir modal para editar essa missão!")
        return
    }

    $('#editMissionId').val(mission.id);
    $('#editMissionName').val(mission.nome);
    $('#editMissionLaunchDate').val(mission.data_lancamento);
    $('#editMissionDestination').val(mission.destino);
    $('#editMissionStatus').val(mission.estado);
    $('#editMissionCrew').val(mission.tripulacao);
    $('#editMissionPayload').val(mission.carga_util);
    $('#editMissionDuration').val(mission.duracao);
    $('#editMissionCost').val(mission.custo);
    $('#editMissionStatusDescription').val(mission.status);

    $('#editModal').modal('show');
}

async function btnDeleteMission(id) {

    if (!confirm('Você tem certeza que deseja deletar essa missão?')) {
        return
    }

    let deleted = await deleteMission({id})
    if (deleted) {
        alert("Missão deletada com sucesso")
        renderTable()
    } else {
        alert("Ocorreu um error ao deletar a missão!")
    }
}