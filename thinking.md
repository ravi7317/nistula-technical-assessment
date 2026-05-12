# Part 3 — Thinking Question Responses

## Question A — The Immediate Response

**Message:**
"Hi [Guest Name], I am so sorry to hear about the hot water issue. I understand how urgent this is with your guests arriving soon. I have already contacted our on-call maintenance team and the property caretaker. I’ve marked this as an urgent issue and our team is being notified right away. While it is 3 AM, we are treating this as a priority. I will provide you with an update as soon as I have a confirmation on the technician's arrival time. Regarding your refund request, our management team will review this first thing in the morning to ensure we make it right."

**Reasoning:**
I chose this wording to validate the guest's frustration immediately while setting realistic expectations. It acknowledges the emergency (3 AM, guests arriving soon), confirms specific actions (alerting maintenance/caretaker), and deferentially handles the refund request without making unauthorized promises, maintaining professional boundaries and a hospitality-first tone.

---

## Question B — The System Design

Beyond sending the message, the platform should execute a multi-channel escalation workflow:

1.  **Emergency Trigger:** The system classifies the message as a 'Critical Complaint' + 'Infrastructure Failure'.
2.  **Immediate Notifications & Mitigation:** 
    *   **SMS/Automated Call:** An automated "Critical Alert" call is placed to the Villa B1 Caretaker and the North Goa Operations Manager.
    *   **Manual Check Trigger:** The system sends a specific checklist to the caretaker’s mobile app to check for immediate mitigations, such as restarting the water heater or arranging access to an alternate bathroom/property if available.
    *   **Slack/Teams Alert:** A high-priority message is pushed to the `#ops-emergencies` channel.
3.  **Logging & Audit Trail:** The incident is logged in the Property Management System (PMS) with a timestamped "Emergency Ticket." All escalation events, acknowledgement times, and resolution updates are stored for SLA tracking and post-incident analysis.
4.  **No-Response Escalation:** If no "Acknowledgement" is received within 30 minutes:
    *   The system escalates to the General Manager.
    *   The system sends a follow-up message to the guest: "We are still working on reaching our technician. We haven't forgotten you and are trying an alternative contact."
5.  **Automation Suppression:** The Villa B1 status on the internal dashboard turns RED, automatically suppressing any scheduled "happy" messages (like breakfast reminders or review requests) until the incident is resolved.

---

## Question C — The Learning

This pattern indicates a systemic failure rather than an isolated incident. The platform should take the following actions:

1.  **Pattern Detection:** The platform should automatically detect recurring complaint patterns (e.g., "Hot Water" appearing in `complaint` query types for `villa-b1` three times in 60 days). It should then generate a **Property Health Report**.
2.  **Preventative Maintenance (PM) Trigger:** The system should block the next "Available" gap in the calendar for a mandatory "Water System Overhaul" and assign a senior plumber (not the regular caretaker) to inspect the solar/electric heaters and pressure pumps.
3.  **Pre-emptive Guest Communication:** For future guests at Villa B1, the system should add a specific "Hot Water Check" to the caretaker's digital check-in list, requiring a photo or temperature reading of running hot water before the guest arrives.
4.  **Hardware Upgrade:** If the frequency exceeds a threshold, the system should trigger a CAPEX request to the owner for a backup geyser system, citing the cost of potential refunds and brand damage as financial justification.
