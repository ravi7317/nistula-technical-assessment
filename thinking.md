# Part 3 — Thinking Question Responses

## Question A — The Immediate Response

**Message:**
"Hi [Guest Name], I am so sorry to hear about the hot water issue. I understand how urgent this is with guests arriving for breakfast. I have already contacted our on-call maintenance team and the property caretaker to treat this as a priority. While it is 3 AM, we are working to get a technician to you immediately. I will provide an update on their arrival time as soon as possible. Regarding your refund request, our management team will review this first thing in the morning to ensure we make it right for you."

**Reasoning:**
I chose this wording to validate the guest's frustration while setting realistic expectations. It confirms specific actions (alerting maintenance) and handles the refund request deferentially without making unauthorized promises, maintaining a hospitality-first tone at an unsociable hour.

---

## Question B — The System Design

Beyond sending the message, the platform executes a multi-channel escalation workflow:

1.  **Emergency Trigger:** The system classifies the message as a 'Critical Infrastructure Failure'.
2.  **Immediate Notifications:** 
    *   **Automated Call:** A "Critical Alert" call is placed to the Villa B1 Caretaker and Operations Manager.
    *   **Mitigation Checklist:** The system sends a checklist to the caretaker’s app to check immediate fixes (e.g., geyser reset) or arrange access to an alternate bathroom.
    *   **Internal Alert:** A high-priority message is pushed to the `#ops-emergencies` Slack channel.
3.  **Logging & Audit:** The incident is logged in the PMS as an "Emergency Ticket" for SLA tracking and post-incident analysis.
4.  **No-Response Escalation:** If unacknowledged within 30 minutes, the system escalates to the General Manager and sends a "still working on it" follow-up to the guest.
5.  **Automation Suppression:** The villa status turns RED, automatically suppressing scheduled "happy" messages (like review requests) until resolution.

---

## Question C — The Learning

This pattern indicates a systemic failure. The platform should take these preventative actions:

1.  **Pattern Detection:** Automatically flag recurring "Hot Water" complaints (e.g., 3+ in 60 days) and generate a **Property Health Report**.
2.  **Maintenance Trigger:** Block the next calendar gap for a mandatory water system overhaul by a senior plumber (not just the regular caretaker).
3.  **Pre-emptive Verification:** Add a mandatory "Hot Water Check" to the caretaker’s digital check-in list, requiring a timestamped photo of a thermometer reading before every guest arrival.
4.  **Hardware Upgrade:** If frequency exceeds a threshold, the system triggers a CAPEX request for a backup geyser, citing refund costs and brand damage as financial justification.

