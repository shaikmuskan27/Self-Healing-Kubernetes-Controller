document.addEventListener('DOMContentLoaded', () => {
    
    // --- Code Tabs Logic ---
    const tabBtns = document.querySelectorAll('.code-tab-btn');
    const tabContents = document.querySelectorAll('.code-tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active state from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.add('hidden'));

            // Add active state to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.remove('hidden');
        });
    });

    // --- Live Simulator Logic ---
    const triggerBtn = document.getElementById('btn-trigger');
    const logsContainer = document.getElementById('sim-logs');
    const slackUI = document.getElementById('sim-slack');
    const githubUI = document.getElementById('sim-github');

    const logSequence = [
        { msg: "[K8s API] Event received: Pod web-api-production state changed to Failed", delay: 500, color: "text-gray-400" },
        { msg: "[Controller] 🚨 Detected failing pod: web-api-production", delay: 1200, color: "text-red-400 font-bold" },
        { msg: "[Controller] Fetching last 50 lines of container logs...", delay: 2000, color: "text-gray-400" },
        { msg: "[Diagnostic] Parsed logs. Signature match: java.lang.OutOfMemoryError", delay: 2800, color: "text-yellow-400" },
        { msg: "[Remediation] Generating GitOps patch: Increase limits by 256Mi", delay: 3500, color: "text-blue-400" },
        { msg: "[GitOps] Branch created. Pull Request opened #42", delay: 4200, color: "text-green-400" },
        { msg: "[Notification] Slack payload delivered successfully.", delay: 4800, color: "text-gray-400" }
    ];

    triggerBtn.addEventListener('click', () => {
        // Reset state
        triggerBtn.disabled = true;
        triggerBtn.classList.add('opacity-50', 'cursor-not-allowed');
        triggerBtn.innerText = "SIMULATION RUNNING...";
        logsContainer.innerHTML = '';
        slackUI.classList.remove('translate-x-0', 'opacity-100');
        slackUI.classList.add('translate-x-12', 'opacity-0');
        githubUI.classList.remove('translate-x-0', 'opacity-100');
        githubUI.classList.add('translate-x-12', 'opacity-0');

        let totalDelay = 0;

        logSequence.forEach((step, index) => {
            setTimeout(() => {
                const logEl = document.createElement('div');
                logEl.className = `font-mono text-sm ${step.color} animate-fade-in-up`;
                logEl.innerText = `> ${step.msg}`;
                logsContainer.appendChild(logEl);

                // Trigger UIs at specific steps
                if (index === 5) { // Github step
                    githubUI.classList.remove('translate-x-12', 'opacity-0');
                    githubUI.classList.add('translate-x-0', 'opacity-100');
                }
                if (index === 6) { // Slack step
                    slackUI.classList.remove('translate-x-12', 'opacity-0');
                    slackUI.classList.add('translate-x-0', 'opacity-100');
                    
                    // Reset button after completion
                    setTimeout(() => {
                        triggerBtn.disabled = false;
                        triggerBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                        triggerBtn.innerHTML = `
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                            RUN AGAIN
                        `;
                    }, 2000);
                }
            }, step.delay);
        });
    });
});
