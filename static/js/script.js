document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los elementos <select> en la página
    var selectReport = document.getElementById('selectReport');

    selectReport.addEventListener('change', function() {
        if (selectReport.value == 'client_report'){
            console.log("Entro aqui marico")
            createFileInputs('Lapeira & Tru', 'SecurePlus')
        }else if (selectReport.value == 'broker_report'){
            console.log("Este entro aki huevon")
            createFileInputs("Broker Report")
        }else if (selectReport.value == 'oneill_report'){
            createFileInputs("O´NEILL Report")
        }else if (selectReport.value == 'comparative_report'){
            createFileInputs()
        }
    });
});

function createFileInputs(text1, text2) {
    const container = document.getElementById("inputsFiles");
    container.innerHTML = ''
    if (text1 === undefined) {
        container.innerHTML = ''
        document.getElementById("btnSubmit").textContent = 'Generate'
        return;
    }else{
        document.getElementById("btnSubmit").textContent = 'Submit'
    }
    
    const outerDiv = document.createElement("div");
    outerDiv.className = "mb-3";

    const outerDiv2 = document.createElement("div");
    outerDiv2.className = "mb-3";

    const label1 = document.createElement("label");
    label1.className = "form-label";
    label1.textContent = text1;
    const input1 = document.createElement("input");
    input1.name = "file1";
    input1.className = "form-control";
    input1.type = "file";
    if (text1 == 'Broker Report' || text1 == 'O´NEILL Report') {
        input1.accept = ".xlsx";
    }else{
        input1.accept = ".csv";
    }
    
    
    
    const label2 = document.createElement("label");
    label2.className = "form-label";
    label2.textContent = "SecurePlus";
    
    const input2 = document.createElement("input");
    input2.name = "file2";
    input2.className = "form-control";
    input2.type = "file";
    input2.accept = ".csv";
    
    outerDiv.appendChild(label1);
    outerDiv.appendChild(input1);
    outerDiv2.appendChild(label2);
    outerDiv2.appendChild(input2);
    
    container.appendChild(outerDiv);
    
    if (text2 !== undefined) {
        container.appendChild(outerDiv2);
    }
}