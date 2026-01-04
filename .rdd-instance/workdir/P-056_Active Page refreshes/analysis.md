```markdown
# Analysis — Active Page refreshes (P-056)

## Copilot Review

Summary:

- The requested change is feasible and low-risk if implemented with targeted, client-side updates. The questionnaire indicates the user selected:
  - Scope: "All status indicators and mode buttons across the Active Prompt page" (Q1 = B)
  - Interval: fixed 2 seconds (Q2 = A)
  - Mechanism: client-side polling using `setInterval` and targeted DOM updates (Q3 = A)
  - Interaction handling: partial suppression while focused or when modals are open (Q4 = C)

Feasibility:

- Implementing a 2s client-side poll that requests only the minimal data (status values and mode-button states) is straightforward and compatible with the existing REST-like API approach used by the Web UI.
- No backend changes are strictly required if endpoints already exist to return the status/mode values; otherwise a small read-only API or an endpoint that returns a compact JSON with the target values is needed.

Risks and challenges:

- Performance: polling every 2s across many clients may increase server load. Mitigation: limit the payload to only changed fields, allow configurable interval, and add caching or conditional GET (ETag/If-Modified-Since) where possible.
- UI jitter: replacing DOM nodes or values while the user interacts may cause visible jumps or focus loss. Mitigation: perform granular updates (text/value only), avoid re-creating DOM elements, and suppress updates for focused elements or open modals per the questionnaire selection.
- Race conditions: user actions (clicks, toggles) may be in-flight while poll responses arrive. Mitigation: apply optimistic UI for user actions and ignore poll updates for in-progress interactions or use timestamps to only apply newer states.

Impact on existing functionality:

- Minimal if updates are targeted; the rest of the page and features remain unchanged. If polling is implemented naively (full re-render), there is a risk to autosave flows and other interactive widgets.

Completeness of prompt description:

- The prompt states the desired behavior and interval but is ambiguous about exact element scope and interaction rules; the included questionnaire resolves these ambiguities and the chosen answers are used in the recommendations below.


## Best Practices (sources & summaries)

- MDN: `setInterval`, DOM update patterns
  - https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setInterval
  - Summary: Use `setInterval` for periodic actions; prefer targeted DOM updates and minimize work inside the interval callback to avoid jank.

- MDN: Server-Sent Events and WebSockets (alternatives to polling)
  - WebSockets: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
  - Server-Sent Events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
  - Summary: Push technologies are more efficient for frequent updates and many clients; they require backend support and connection management.

- UX guidance on avoiding interruptions (selection & focus preservation)
  - Nielsen Norman Group (general guidance on interrupting users): https://www.nngroup.com/articles/interrupting-users/
  - Summary: Avoid unexpected changes while users are actively interacting with UI elements; defer or pause updates when focus is detected.

- Guided examples and discussions for partial updates and polling strategies
  - Article: lightweight polling with conditional updates (example): https://web.dev/long-lived-connection-best-practices/
  - Summary: Favor small JSON payloads, conditional requests, and exponential/backoff or adaptive intervals where appropriate.


## Samples from GitHub / Common approaches

- Client-side polling (simple approach): Many lightweight dashboards use `setInterval` and fetch a compact JSON of changed values, then update specific DOM text nodes. This pattern is common in small admin dashboards and monitoring pages.

- Push-based approaches: Larger apps and collaboration tools use WebSockets or SSE to deliver frequent updates (e.g., chat apps, realtime dashboards). These implementations typically live in repos that integrate `socket.io`, `EventSource`, or backend frameworks supporting WebSocket endpoints.

Note: Specific repository references were not queried live; the above characterizes broadly-observed patterns across open-source dashboards and realtime apps.


## Proposals (alternatives, suggested requirement modifications, trade-offs)

1) Minimal-safe approach (Recommended initial implementation)

- Implement client-side polling with `setInterval` every 2000 ms to fetch a compact endpoint (e.g., `/api/active-prompt/status`) returning only the values to update (status badges and mode buttons across the page).
- Apply only granular updates to existing DOM nodes (text content, CSS classes, disabled/enabled state) rather than re-rendering entire sections.
- Implement partial suppression: detect focused elements and open modals; if a related element is focused, skip updates for that element until it loses focus. Always apply updates that do not affect focused elements.
- Add a small debounce for frequent local user actions to avoid overwriting immediately after user input.
- Configuration: expose a setting (UI + persisted config) to change the refresh interval (default 2000 ms) or disable automatic refresh per-user or per-deployment.

Trade-offs:
- Pros: Fast delivery, simple to implement, compatible with current server design.
- Cons: Higher aggregate server requests with many clients; less efficient than push.

2) Push-based approach (Future improvement)

- Implement SSE or WebSockets for the Active Prompt page to stream only changed values.
- Pros: Scales better for many frequent updates and avoids wasted requests.
- Cons: Requires backend changes and connection management; more complex testing and fallback handling.


## Prompt Modification (refined prompt)

Refined prompt to be used instead of the original:

> On the Active Prompt page, implement an automatic refresh of all status indicators and mode buttons across the page. The default refresh interval should be 2 seconds (configurable via user settings). Use client-side polling initially and perform targeted DOM updates only for changed fields — do not re-create DOM nodes. Pause updates for focused controls or when modals are open to avoid interrupting user interaction. Provide a per-user setting to disable or change the refresh interval. If scaling or performance concerns arise, migrate to a push-based approach (SSE/WebSocket) in a follow-up change.


---

### Notes & Actions taken

- Questionnaire: Applied user selections (Q1=B, Q2=A, Q3=A, Q4=C) when producing proposals and recommendations.
- Technical design: `.rdd-instance/specifications/technical-design.json` is empty; no constraints were found there.

```
