DEMO_PAGE_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Last-Mile Aid Delivery Monitoring Backend</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
        }

        .container {
            width: 100%;
            max-width: none;
            margin: 0;
            padding: 28px 42px 60px 42px;
        }

        .hero {
            background: linear-gradient(135deg, #1d4ed8, #059669);
            padding: 42px;
            border-radius: 22px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.35);
            position: relative;
            overflow: hidden;
            min-height: 240px;
        }

        .hero-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 28px;
            position: relative;
            z-index: 2;
        }

        .hero-text {
            max-width: 950px;
        }

        .circle {
            width: 190px;
            height: 190px;
            border-radius: 50%;
            background: rgba(255,255,255,0.18);
            position: absolute;
            right: -45px;
            top: -45px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.8; }
            50% { transform: scale(1.2); opacity: 0.3; }
            100% { transform: scale(0.9); opacity: 0.8; }
        }

        h1 {
            margin: 0;
            font-size: 42px;
            line-height: 1.15;
        }

        .subtitle {
            max-width: 980px;
            margin-top: 14px;
            line-height: 1.6;
            color: #d1fae5;
            font-size: 17px;
        }

        .status {
            display: inline-block;
            margin-top: 18px;
            padding: 9px 15px;
            background: rgba(255,255,255,0.16);
            border-radius: 999px;
            font-size: 15px;
        }

        .dot {
            display: inline-block;
            width: 11px;
            height: 11px;
            background: #22c55e;
            border-radius: 50%;
            margin-right: 8px;
            box-shadow: 0 0 12px #22c55e;
        }

        .big-seed-button {
            background: #facc15;
            color: #111827;
            font-weight: bold;
            font-size: 18px;
            padding: 18px 28px;
            border-radius: 16px;
            border: none;
            cursor: pointer;
            box-shadow: 0 14px 30px rgba(250, 204, 21, 0.35);
            min-width: 230px;
        }

        .big-seed-button:hover {
            background: #eab308;
        }

        .hero-actions {
            margin-top: 26px;
            position: relative;
            z-index: 2;
        }

        .button, button {
            background: #2563eb;
            color: white;
            border: none;
            padding: 11px 15px;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 5px 5px 5px 0;
            font-size: 14px;
        }

        .button:hover, button:hover {
            background: #1d4ed8;
        }

        .button.secondary {
            background: #0f172a;
            border: 1px solid rgba(255,255,255,0.18);
        }

        .button.secondary:hover {
            background: #1e293b;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 24px;
            margin-top: 24px;
        }

        .card {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 18px;
            padding: 26px;
            min-height: 250px;
            box-shadow: 0 12px 28px rgba(0,0,0,0.18);
        }

        .wide-card {
            grid-column: 1 / -1;
        }

        .card h2 {
            margin-top: 0;
            font-size: 25px;
        }

        .card p {
            color: #e5e7eb;
            line-height: 1.45;
        }

        label {
            font-size: 14px;
            color: #cbd5e1;
            display: block;
            margin-top: 10px;
        }

        input, textarea {
            width: 100%;
            padding: 12px;
            margin: 7px 0 12px;
            border-radius: 9px;
            border: 1px solid #334155;
            background: #020617;
            color: #e5e7eb;
            font-size: 14px;
        }

        textarea {
            min-height: 80px;
        }

        pre {
            background: #020617;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 14px;
            overflow-x: auto;
            min-height: 120px;
            color: #a7f3d0;
            font-size: 13px;
            line-height: 1.45;
            white-space: pre-wrap;
        }

        .note {
            color: #facc15;
            font-size: 14px;
            line-height: 1.5;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 14px;
            margin-top: 18px;
        }

        .metric {
            background: #020617;
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 16px;
        }

        .metric-label {
            color: #93c5fd;
            font-size: 13px;
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #f8fafc;
        }

        .health-panel {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 14px;
            margin-top: 18px;
        }

        .health-box {
            background: #020617;
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 16px;
        }

        .health-label {
            color: #93c5fd;
            font-size: 13px;
            margin-bottom: 8px;
        }

        .health-value {
            color: #a7f3d0;
            font-size: 19px;
            font-weight: bold;
            word-break: break-word;
        }

        .footer {
            margin-top: 34px;
            padding: 18px;
            color: #94a3b8;
            text-align: center;
            font-size: 14px;
        }

        @media (max-width: 800px) {
            .container {
                padding: 18px;
            }

            .hero-top {
                flex-direction: column;
            }

            h1 {
                font-size: 32px;
            }

            .big-seed-button {
                width: 100%;
            }
        }
    </style>
</head>

<body>
<div class="container">

    <section class="hero">
        <div class="circle"></div>

        <div class="hero-top">
            <div class="hero-text">
                <h1>Last-Mile Aid Delivery Monitoring Backend</h1>
                <p class="subtitle">
                    Live FastAPI demo for humanitarian delivery monitoring. The backend supports warehouse stock checks,
                    delivery requests, issue reporting, delayed delivery monitoring, and operational summary metrics.
                </p>

                <div class="status">
                    <span class="dot"></span>Backend API running
                </div>
            </div>

            <div>
                <button class="big-seed-button" onclick="loadDemoData()">Load Demo Data</button>
            </div>
        </div>

        <div class="hero-actions">
            <a class="button" href="/docs" target="_blank">Open Swagger Docs</a>
	    <button onclick="loadHealthPanelAndScroll()">Health Status UI</button>
            <button onclick="loadSummaryDashboardAndScroll()">Operational Summary UI</button>
            <a class="button secondary" href="/health" target="_blank">Raw Health JSON</a>
            <a class="button secondary" href="/summary/operational" target="_blank">Raw Summary JSON</a>
        </div>
    </section>

    <section class="grid">

        <div class="card">
            <h2>Backend Checks</h2>
            <p>Use these buttons to call live API endpoints.</p>

            <button onclick="callApi('/health', 'healthResult')">Check Health</button>
            <button onclick="callApi('/db-health', 'healthResult')">Check DB</button>
            <button onclick="callApi('/data-health', 'healthResult')">Check Seed Data</button>

            <pre id="healthResult">Click "Load Demo Data" first, then check seed data.</pre>
        </div>

        <div class="card">
            <h2>Operational Summary</h2>
            <p>Fetch delivery status counts, open issues, overdue deliveries, and low stock records.</p>

            <button onclick="callApi('/summary/operational', 'summaryResult')">Load Summary JSON</button>
            <button onclick="loadSummaryDashboard()">Show Summary UI</button>

            <pre id="summaryResult">Summary JSON will appear here.</pre>
        </div>

        <div class="card">
            <h2>Warehouse Stock</h2>

            <label>Warehouse ID</label>
            <input id="warehouseId" type="number" value="1">

            <button onclick="loadStock()">Check Stock</button>

            <pre id="stockResult">Warehouse stock will appear here.</pre>
        </div>

    </section>

    <section class="grid">

        <div class="card wide-card" id="healthSection">
            <h2>Health Status Interface</h2>
            <p>This is the human-friendly view of the backend health endpoint.</p>

            <button onclick="loadHealthPanel()">Refresh Health Status</button>

            <div id="healthPanel" class="health-panel">
                <div class="health-box">
                    <div class="health-label">Status</div>
                    <div class="health-value">Not loaded</div>
                </div>
                <div class="health-box">
                    <div class="health-label">Service</div>
                    <div class="health-value">Not loaded</div>
                </div>
                <div class="health-box">
                    <div class="health-label">Version</div>
                    <div class="health-value">Not loaded</div>
                </div>
            </div>
        </div>

        <div class="card wide-card" id="summarySection">
            <h2>Operational Summary Interface</h2>
            <p>This is the human-friendly dashboard view of the operational summary JSON.</p>

            <button onclick="loadSummaryDashboard()">Refresh Operational Dashboard</button>

            <div id="summaryDashboard" class="metric-grid">
                <div class="metric">
                    <div class="metric-label">Total Deliveries</div>
                    <div class="metric-value">0</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Pending</div>
                    <div class="metric-value">0</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Open Issues</div>
                    <div class="metric-value">0</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Low Stock Records</div>
                    <div class="metric-value">0</div>
                </div>
            </div>
        </div>

    </section>

    <section class="grid">

        <div class="card">
            <h2>Create Delivery Request</h2>

            <p class="note">
                This sends JSON to POST /deliveries/. It demonstrates backend validation for stock, dates, and references.
                Use demo IDs 1 after loading demo data.
            </p>

            <label>Request Code</label>
            <input id="requestCode" value="REQ-DEMO-001">

            <label>Warehouse ID</label>
            <input id="deliveryWarehouseId" type="number" value="1">

            <label>Field Location ID</label>
            <input id="fieldLocationId" type="number" value="1">

            <label>Partner ID</label>
            <input id="partnerId" type="number" value="1">

            <label>Item ID</label>
            <input id="itemId" type="number" value="1">

            <label>Quantity Requested</label>
            <input id="quantityRequested" type="number" value="10">

            <label>Request Date</label>
            <input id="requestDate" type="date" value="2026-06-09">

            <label>Required Delivery Date</label>
            <input id="requiredDeliveryDate" type="date" value="2026-06-12">

            <label>Notes</label>
            <textarea id="deliveryNotes">Demo delivery request from the web interface.</textarea>

            <button onclick="createDelivery()">Submit Delivery</button>

            <pre id="deliveryResult">Delivery response will appear here.</pre>
        </div>

        <div class="card">
            <h2>Create Issue Report</h2>

            <p class="note">
                This sends JSON to POST /issues/. Create a delivery first, then use the returned delivery ID here.
            </p>

            <label>Delivery Request ID</label>
            <input id="issueDeliveryId" type="number" value="1">

            <label>Severity</label>
            <input id="severity" value="high">

            <label>Issue Type</label>
            <input id="issueType" value="Access constraint">

            <label>Description</label>
            <textarea id="issueDescription">Road access to the field location is temporarily blocked.</textarea>

            <button onclick="createIssue()">Submit Issue</button>

            <pre id="issueResult">Issue response will appear here.</pre>
        </div>

    </section>

    <div class="footer">
        Portfolio demo only. Main repository: github.com/yasirsiddiq01/last-mile-aid-delivery-backend
    </div>

</div>

<script>
function showResult(outputId, title, details) {
    const output = document.getElementById(outputId);
    output.textContent = title + "\n\n" + details;
}

async function callApi(endpoint, outputId) {
    showResult(outputId, "LOADING", "Calling " + endpoint + "...");

    try {
        const response = await fetch(endpoint);
        const data = await response.json();

        showResult(
            outputId,
            response.ok ? "SUCCESS" : "FAILED",
            "Endpoint: " + endpoint +
            "\nHTTP status: " + response.status +
            "\n\n" + JSON.stringify(data, null, 2)
        );
    } catch (error) {
        showResult(
            outputId,
            "CONNECTION ERROR",
            "Could not call " + endpoint + "\n\n" + String(error)
        );
    }
}

async function loadDemoData() {
    showResult("healthResult", "LOADING DEMO DATA", "Calling POST /demo/seed...");

    try {
        const response = await fetch("/demo/seed", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: "{}"
        });

        const data = await response.json();

        showResult(
            "healthResult",
            response.ok ? "DEMO DATA READY" : "DEMO DATA FAILED",
            "HTTP status: " + response.status +
            "\n\n" + JSON.stringify(data, null, 2) +
            "\n\nUse these IDs for testing:" +
            "\nWarehouse ID: 1" +
            "\nField Location ID: 1" +
            "\nPartner ID: 1" +
            "\nItem ID: 1"
        );

        await loadHealthPanel();
        await loadSummaryDashboard();
        await callApi("/data-health", "healthResult");

    } catch (error) {
        showResult(
            "healthResult",
            "CONNECTION ERROR",
            "Could not call POST /demo/seed.\n\n" + String(error)
        );
    }
}
async function loadHealthPanelAndScroll() {
    await loadHealthPanel();

    document.getElementById("healthSection").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

async function loadSummaryDashboardAndScroll() {
    await loadSummaryDashboard();

    document.getElementById("summarySection").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

async function loadHealthPanel() {
    try {
        const response = await fetch("/health");
        const data = await response.json();

        const panel = document.getElementById("healthPanel");

        if (response.ok) {
            panel.innerHTML = `
                <div class="health-box">
                    <div class="health-label">Status</div>
                    <div class="health-value">${data.status || "unknown"}</div>
                </div>
                <div class="health-box">
                    <div class="health-label">Service</div>
                    <div class="health-value">${data.service || "unknown"}</div>
                </div>
                <div class="health-box">
                    <div class="health-label">Version</div>
                    <div class="health-value">${data.version || "unknown"}</div>
                </div>
            `;
        } else {
            panel.innerHTML = `
                <div class="health-box">
                    <div class="health-label">Health Check Failed</div>
                    <div class="health-value">HTTP ${response.status}</div>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById("healthPanel").innerHTML = `
            <div class="health-box">
                <div class="health-label">Connection Error</div>
                <div class="health-value">${String(error)}</div>
            </div>
        `;
    }
}

async function loadSummaryDashboard() {
    try {
        const response = await fetch("/summary/operational");
        const data = await response.json();

        const dashboard = document.getElementById("summaryDashboard");

        if (response.ok) {
            dashboard.innerHTML = `
                <div class="metric">
                    <div class="metric-label">Total Deliveries</div>
                    <div class="metric-value">${data.total_deliveries}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Pending</div>
                    <div class="metric-value">${data.pending}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Dispatched</div>
                    <div class="metric-value">${data.dispatched}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">In Transit</div>
                    <div class="metric-value">${data.in_transit}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Delivered</div>
                    <div class="metric-value">${data.delivered}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Delayed</div>
                    <div class="metric-value">${data.delayed}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Cancelled</div>
                    <div class="metric-value">${data.cancelled}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Failed</div>
                    <div class="metric-value">${data.failed}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Overdue Deliveries</div>
                    <div class="metric-value">${data.overdue_deliveries}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Open Issue Reports</div>
                    <div class="metric-value">${data.open_issue_reports}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Low Stock Records</div>
                    <div class="metric-value">${data.low_stock_records}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Low Stock Threshold</div>
                    <div class="metric-value">${data.low_stock_threshold}</div>
                </div>
            `;

            showResult(
                "summaryResult",
                "SUCCESS",
                "Endpoint: /summary/operational\nHTTP status: " + response.status +
                "\n\n" + JSON.stringify(data, null, 2)
            );
        } else {
            dashboard.innerHTML = `
                <div class="metric">
                    <div class="metric-label">Summary Failed</div>
                    <div class="metric-value">HTTP ${response.status}</div>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById("summaryDashboard").innerHTML = `
            <div class="metric">
                <div class="metric-label">Connection Error</div>
                <div class="metric-value">${String(error)}</div>
            </div>
        `;
    }
}

async function loadStock() {
    const id = document.getElementById("warehouseId").value;
    await callApi("/warehouses/" + id + "/stock", "stockResult");
}

async function createDelivery() {
    const payload = {
        request_code: document.getElementById("requestCode").value,
        warehouse_id: Number(document.getElementById("deliveryWarehouseId").value),
        field_location_id: Number(document.getElementById("fieldLocationId").value),
        partner_id: Number(document.getElementById("partnerId").value),
        item_id: Number(document.getElementById("itemId").value),
        quantity_requested: Number(document.getElementById("quantityRequested").value),
        request_date: document.getElementById("requestDate").value,
        required_delivery_date: document.getElementById("requiredDeliveryDate").value,
        notes: document.getElementById("deliveryNotes").value
    };

    await sendPost("/deliveries/", payload, "deliveryResult", "delivery");
}

async function createIssue() {
    const payload = {
        delivery_request_id: Number(document.getElementById("issueDeliveryId").value),
        severity: document.getElementById("severity").value,
        issue_type: document.getElementById("issueType").value,
        description: document.getElementById("issueDescription").value
    };

    await sendPost("/issues/", payload, "issueResult", "issue");
}

async function sendPost(endpoint, payload, outputId, recordType) {
    showResult(
        outputId,
        "SUBMITTING",
        "Sending JSON to " + endpoint + "\n\n" + JSON.stringify(payload, null, 2)
    );

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            let savedIdText = "";

            if (data.id) {
                savedIdText = "\nSaved record ID: " + data.id;
            }

            if (recordType === "delivery" && data.id) {
                document.getElementById("issueDeliveryId").value = data.id;
                document.getElementById("requestCode").value = "REQ-DEMO-" + Date.now();
            }

            showResult(
                outputId,
                "SUBMISSION SUCCESSFUL",
                "The " + recordType + " was saved in the backend." +
                "\nHTTP status: " + response.status +
                savedIdText +
                "\n\nBackend response:\n" +
                JSON.stringify(data, null, 2)
            );

            await loadSummaryDashboard();
            await callApi("/data-health", "healthResult");

        } else {
            showResult(
                outputId,
                "SUBMISSION FAILED",
                "The " + recordType + " was not saved." +
                "\nHTTP status: " + response.status +
                "\n\nBackend reason:\n" +
                JSON.stringify(data, null, 2)
            );
        }

    } catch (error) {
        showResult(
            outputId,
            "CONNECTION ERROR",
            "The request could not reach the backend.\n\n" + String(error)
        );
    }
}

window.onload = async function() {
    document.getElementById("requestCode").value = "REQ-DEMO-" + Date.now();
    await loadHealthPanel();
    await loadSummaryDashboard();
};
</script>

</body>
</html>
"""