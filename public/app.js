const form = document.querySelector("#change-form");
const changeInput = document.querySelector("#change-input");
const writebackInput = document.querySelector("#writeback-input");
const result = document.querySelector("#result");
const runLabel = document.querySelector("#run-label");
const scenarioList = document.querySelector("#scenario-list");
const submitButton = form.querySelector("button[type='submit']");
const submitLabel = submitButton.querySelector("span");

let lastAssessment = null;

const escapeHtml = (value) =>
  String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

async function loadScenarios() {
  try {
    const response = await fetch("/api/scenarios");
    if (!response.ok) throw new Error("Could not load scenarios.");
    const data = await response.json();
    scenarioList.innerHTML = data.scenarios
      .map(
        (scenario, index) => `
          <button class="scenario-button" type="button" data-change="${escapeHtml(scenario.change)}">
            <span><b>0${index + 1}</b>${escapeHtml(scenario.label)}</span>
            <small>${escapeHtml(scenario.expected)}</small>
          </button>
        `,
      )
      .join("");
    scenarioList.querySelectorAll("button").forEach((button) => {
      button.addEventListener("click", () => {
        changeInput.value = button.dataset.change;
        changeInput.focus();
      });
    });
  } catch (error) {
    scenarioList.innerHTML = `<p class="help">${escapeHtml(error.message)}</p>`;
  }
}

function renderLoading() {
  submitButton.disabled = true;
  submitLabel.textContent = "Compiling evidence";
  runLabel.textContent = "Querying DataHub MCP";
  result.innerHTML = `
    <div class="loading-state" aria-label="Compilation in progress">
      <div class="loading-heading"><span></span><span></span></div>
      <div class="loading-metrics"><span></span><span></span><span></span><span></span></div>
      <div class="loading-panel"><span></span><span></span><span></span><span></span></div>
    </div>
  `;
}

function renderError(message) {
  runLabel.textContent = "Compile failed";
  result.innerHTML = `
    <div class="error-state" role="alert">
      <p class="empty-kicker">Input rejected</p>
      <h3>Migration plan could not compile</h3>
      <p>${escapeHtml(message)}</p>
    </div>
  `;
}

function renderAssessment(data) {
  lastAssessment = data;
  const metrics = data.counterfactual.metrics;
  const failures = data.counterfactual.predicted_failures.length
    ? data.counterfactual.predicted_failures
        .map(
          (failure) => `
            <li class="failure-item">
              <div class="failure-heading">
                <strong>${escapeHtml(failure.asset)}</strong>
                <span class="severity ${escapeHtml(failure.severity)}">${escapeHtml(failure.severity)}</span>
              </div>
              <p>${escapeHtml(failure.failure_mode)}</p>
              <div class="lineage-path" aria-label="Lineage path">
                ${failure.lineage_path.map((node) => `<code>${escapeHtml(node)}</code>`).join("<i>→</i>")}
              </div>
              <small>Owner / ${escapeHtml(failure.owner)}</small>
            </li>
          `,
        )
        .join("")
    : `<li class="failure-item"><strong>No predicted failures</strong><p>No active consumer edge depends on this field.</p></li>`;

  const policies = data.policy_proof
    .map(
      (item) => `
        <li class="policy-item">
          <code>${escapeHtml(item.id)}</code>
          <div><strong>${escapeHtml(item.title)}</strong><p>${escapeHtml(item.evidence)}</p></div>
          <span class="policy-status ${escapeHtml(item.status.toLowerCase())}">${escapeHtml(item.status)}</span>
        </li>
      `,
    )
    .join("");

  const execution = data.execution_plan
    .map(
      (node) => `
        <li class="dag-node">
          <div class="node-id">${escapeHtml(node.id)}</div>
          <div class="node-body">
            <div class="node-title"><strong>${escapeHtml(node.action)}</strong><span>${escapeHtml(node.state)}</span></div>
            <p>${escapeHtml(node.evidence)}</p>
            <small>Actor / ${escapeHtml(node.actor)}</small>
          </div>
          <code>${node.depends_on.length ? `after ${escapeHtml(node.depends_on.join(", "))}` : "root gate"}</code>
        </li>
      `,
    )
    .join("");

  const trace = data.tool_trace
    .map(
      (call, index) => `
        <li class="trace-item">
          <span>0${index + 1}</span>
          <div><code>${escapeHtml(call.tool)}</code><p>${escapeHtml(call.summary)}</p></div>
          <pre>${escapeHtml(JSON.stringify(call.arguments, null, 2))}</pre>
        </li>
      `,
    )
    .join("");

  const artifacts = data.artifact_manifest
    .map(
      (artifact) => `
        <li><span class="file-icon" aria-hidden="true">↳</span><div><code>${escapeHtml(artifact.path)}</code><small>${escapeHtml(artifact.purpose)}</small></div><b>READY</b></li>
      `,
    )
    .join("");

  const writeback = data.writeback.success
    ? data.writeback.message
    : data.writeback.message || "Writeback skipped.";

  runLabel.textContent = data.change_capsule.capsule_id;
  result.innerHTML = `
    <section class="gate-summary">
      <div class="gate-copy">
        <p>${escapeHtml(data.decision)} / ${escapeHtml(data.release_gate.blockers.length)} policy blockers</p>
        <h3>Release gate ${escapeHtml(data.release_gate.status)}</h3>
        <strong class="gate-impact">${escapeHtml(metrics.broken_edges)} broken edges across ${escapeHtml(metrics.max_lineage_hops)} hops</strong>
        <span class="gate-rationale">${escapeHtml(data.headline)}</span>
        <code>${escapeHtml(data.source.name)}.${escapeHtml(data.request.column)}</code>
      </div>
      <div class="risk-score"><strong>${escapeHtml(data.risk_score)}</strong><span>risk / 10</span></div>
    </section>

    <section class="metric-grid" aria-label="Counterfactual metrics">
      ${metric("Broken edges", metrics.broken_edges, "projected")}
      ${metric("Critical assets", metrics.critical_consumers, "tagged")}
      ${metric("Owner coverage", `${metrics.ownership_coverage}%`, `${metrics.owned_assets}/${metrics.assets_inspected} routed`)}
      ${metric("Max depth", metrics.max_lineage_hops, "lineage hops")}
    </section>

    <div class="tab-bar" role="tablist" aria-label="Compiled evidence views">
      <button id="tab-counterfactual" role="tab" aria-selected="true" aria-controls="panel-counterfactual" data-tab="counterfactual">Counterfactual</button>
      <button id="tab-policy" role="tab" aria-selected="false" aria-controls="panel-policy" data-tab="policy" tabindex="-1">Policy proof <span>${escapeHtml(data.release_gate.blockers.length)}</span></button>
      <button id="tab-plan" role="tab" aria-selected="false" aria-controls="panel-plan" data-tab="plan" tabindex="-1">Execution DAG</button>
      <button id="tab-trace" role="tab" aria-selected="false" aria-controls="panel-trace" data-tab="trace" tabindex="-1">MCP trace <span>${escapeHtml(data.tool_trace.length)}</span></button>
    </div>

    <section id="panel-counterfactual" class="tab-panel" role="tabpanel" aria-labelledby="tab-counterfactual" data-panel="counterfactual">
      <div class="state-diff">
        <div><span>BEFORE</span><strong>${escapeHtml(data.counterfactual.before.field)}</strong><small>${escapeHtml(data.counterfactual.before.type)} / ${escapeHtml(data.counterfactual.before.consumer_edges)} edges</small></div>
        <i>→</i>
        <div class="projected"><span>PROJECTED</span><strong>${escapeHtml(data.counterfactual.after.field)}</strong><small>${escapeHtml(data.counterfactual.after.status)} / ${escapeHtml(data.counterfactual.after.broken_edges)} broken</small></div>
        <code>${escapeHtml(data.counterfactual.engine)}</code>
      </div>
      <div class="panel-heading"><h4>Predicted failure paths</h4><span>${escapeHtml(data.counterfactual.mode)}</span></div>
      <ul class="failure-list">${failures}</ul>
    </section>

    <section id="panel-policy" class="tab-panel" role="tabpanel" aria-labelledby="tab-policy" data-panel="policy" hidden>
      <div class="panel-heading"><h4>Bounded policy proof</h4><span>Stable rule IDs</span></div>
      <ul class="policy-list">${policies}</ul>
      <div class="release-condition"><strong>Gate opens when</strong><p>${escapeHtml(data.release_gate.release_condition)}</p></div>
    </section>

    <section id="panel-plan" class="tab-panel" role="tabpanel" aria-labelledby="tab-plan" data-panel="plan" hidden>
      <div class="panel-heading"><h4>Zero-downtime execution DAG</h4><span>${escapeHtml(data.execution_plan.length)} nodes / owner routed</span></div>
      <ol class="dag-list">${execution}</ol>
    </section>

    <section id="panel-trace" class="tab-panel" role="tabpanel" aria-labelledby="tab-trace" data-panel="trace" hidden>
      <div class="panel-heading"><h4>DataHub MCP provenance</h4><span>Exact calls and arguments</span></div>
      <ol class="trace-list">${trace}</ol>
      <div class="writeback"><strong>DataHub writeback</strong><span>${escapeHtml(writeback)}</span></div>
    </section>

    <section class="artifact-section" aria-labelledby="artifact-title">
      <div class="artifact-heading">
        <div><p class="empty-kicker">Compilation output</p><h4 id="artifact-title">Merge-ready evidence pack</h4></div>
        <div class="artifact-actions">
          <button id="copy-review" class="secondary-button" type="button">Copy PR decision</button>
          <a id="download-pack" class="download-button" href="/api/evidence-pack/${encodeURIComponent(data.run_id)}?change=${encodeURIComponent(data.request.raw)}" download>Download PR pack (.zip) <span>↓</span></a>
        </div>
      </div>
      <ul class="artifact-list">${artifacts}</ul>
      <div class="capsule-line"><span>Hash-sealed capsule</span><code>${escapeHtml(data.change_capsule.capsule_id)}</code><code>sha256:${escapeHtml(data.change_capsule.evidence_sha256.slice(0, 16))}...</code></div>
    </section>
  `;
  bindResultInteractions();
}

function metric(label, value, detail) {
  return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong><small>${escapeHtml(detail)}</small></div>`;
}

function bindResultInteractions() {
  const tabs = [...result.querySelectorAll("[role='tab']")];
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => activateTab(tab.dataset.tab));
    tab.addEventListener("keydown", (event) => {
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      event.preventDefault();
      const current = tabs.indexOf(tab);
      const offset = event.key === 'ArrowRight' ? 1 : -1;
      tabs[(current + offset + tabs.length) % tabs.length].click();
      tabs[(current + offset + tabs.length) % tabs.length].focus();
    });
  });
  result.querySelector("#copy-review").addEventListener("click", copyReviewDecision);
}

function activateTab(name) {
  result.querySelectorAll("[role='tab']").forEach((tab) => {
    const active = tab.dataset.tab === name;
    tab.setAttribute("aria-selected", String(active));
    tab.tabIndex = active ? 0 : -1;
  });
  result.querySelectorAll("[role='tabpanel']").forEach((panel) => {
    panel.hidden = panel.dataset.panel !== name;
  });
}

async function copyReviewDecision() {
  const button = result.querySelector("#copy-review");
  const review = [
    `Ripplecheck ${lastAssessment.change_capsule.capsule_id}`,
    `${lastAssessment.decision}: ${lastAssessment.headline}`,
    `Gate: ${lastAssessment.release_gate.status}`,
    `Blockers: ${lastAssessment.release_gate.blockers.join(", ") || "none"}`,
    `Release condition: ${lastAssessment.release_gate.release_condition}`,
  ].join("\n");
  try {
    await navigator.clipboard.writeText(review);
    button.textContent = "Copied to clipboard";
    window.setTimeout(() => { button.textContent = "Copy PR decision"; }, 1800);
  } catch {
    button.textContent = "Copy unavailable";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  renderLoading();
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        change: changeInput.value,
        writeback: writebackInput.checked,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Compilation failed.");
    renderAssessment(data);
  } catch (error) {
    renderError(error.message);
  } finally {
    submitButton.disabled = false;
    submitLabel.textContent = "Compile migration plan";
  }
});

loadScenarios();
