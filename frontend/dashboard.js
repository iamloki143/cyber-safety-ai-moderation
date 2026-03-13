<!DOCTYPE html>
<html>

<head>

<title>Cyber Safety Moderation Dashboard</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
    font-family: Arial;
    background:#0f172a;
    color:white;
    padding:30px;
}

h1{
    text-align:center;
}

.stats{
    display:flex;
    gap:20px;
    margin-bottom:30px;
}

.card{
    background:#1e293b;
    padding:20px;
    border-radius:10px;
    flex:1;
    text-align:center;
}

.card h2{
    margin:0;
    font-size:35px;
}

table{
    width:100%;
    border-collapse:collapse;
    background:#1e293b;
    margin-top:20px;
}

th,td{
    padding:10px;
    border-bottom:1px solid #334155;
    text-align:center;
}

th{
    background:#334155;
}

canvas{
    margin-top:30px;
}

</style>

</head>


<body>

<h1>Cyber Safety Moderation Dashboard</h1>


<div class="stats">

<div class="card">
<h2 id="total">0</h2>
<p>Total Messages</p>
</div>

<div class="card">
<h2 id="blocked">0</h2>
<p>Blocked Messages</p>
</div>

<div class="card">
<h2 id="images">0</h2>
<p>Image Violations</p>
</div>

</div>


<h2>Moderation Analytics</h2>
<canvas id="moderationChart"></canvas>

<canvas id="moderationChart" width="400" height="200"></canvas>


<h2>Moderation Logs</h2>

<table id="logs">

<thead>

<tr>
<th>User</th>
<th>Content</th>
<th>Category</th>
<th>Status</th>
<th>Confidence</th>
</tr>

</thead>

<tbody></tbody>

</table>



<script>

async function loadLogs(){

    const response = await fetch("/logs");
    const logs = await response.json();

    console.log(logs);

    const table = document.querySelector("#logs tbody");
    table.innerHTML = "";

    let total = logs.length;
    let blocked = 0;
    let images = 0;
    let toxic = 0;
    let neutral = 0;

    logs.forEach(log => {

        if(log.status === "blocked"){
            blocked++;
        }

        if(log.type === "image"){
            images++;
        }

        if(log.category === "Bullying"){
            toxic++;
        }

        if(log.category === "Neutral"){
            neutral++;
        }

        const row = document.createElement("tr");

        row.innerHTML = `
        <td>${log.user_id || "-"}</td>
        <td>${log.content}</td>
        <td>${log.category}</td>
        <td>${log.status}</td>
        <td>${Number(log.confidence).toFixed(2)}</td>
        `;

        table.appendChild(row);

    });

    document.getElementById("total").innerText = total;
    document.getElementById("blocked").innerText = blocked;
    document.getElementById("images").innerText = images;

    createChart(toxic, neutral, images);

}



function createChart(toxic, neutral, images){

    const ctx = document.getElementById("moderationChart");

    new Chart(ctx, {

        type: "bar",

        data: {

            labels: [
                "Toxic Messages",
                "Neutral Messages",
                "Image Violations"
            ],

            datasets: [{
                label: "Moderation Statistics",

                data: [toxic, neutral, images],

                backgroundColor: [
                    "#ef4444",
                    "#22c55e",
                    "#f59e0b"
                ]

            }]

        },

        options: {

            responsive:true,

            plugins:{
                legend:{
                    labels:{color:"white"}
                }
            },

            scales:{
                y:{ticks:{color:"white"}},
                x:{ticks:{color:"white"}}
            }

        }

    });

}


loadLogs();

</script>


</body>

</html>