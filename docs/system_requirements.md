# VolVoice System Requirements

## 1. UX Scenarios captured from the existing plan
- **S1. Quick entry and room creation** – a player launches the desktop client, enters a nickname, and creates a new voice room.
- **S2. Invite collaborators** – the room creator shares either a link or short access code with friends so they can join the room.
- **S3. Join existing room** – an invited player starts the client, enters their nickname and the received room link or code to join the ongoing conversation.
- **S4. In-room voice session** – all connected players converse through persistent audio until they leave the room.

## 2. Functional system requirements derived from scenarios
| ID | Scenario | Requirement |
|----|----------|-------------|
| SR-1 | S1 | The desktop application SHALL allow launching without prior account registration and prompt for a unique nickname before entering the service. |
| SR-2 | S1 | The system SHALL provide controls to create a new voice room in fewer than three clicks from the initial screen. |
| SR-3 | S1 | Upon room creation, the system SHALL generate a unique room identifier and access link valid for at least 24 hours. |
| SR-4 | S2 | The system SHALL display the room link and alphanumeric access code immediately after creation and keep them accessible from the room lobby UI. |
| SR-5 | S2 | The system SHALL support copying the link/code to the clipboard through a single UI action. |
| SR-6 | S3 | The client SHALL allow users to paste a room link or manually enter the access code from the home screen. |
| SR-7 | S3 | The backend SHALL validate room codes within 1 second and provide clear feedback if the room is invalid or full. |
| SR-8 | S3 | Upon successful validation, the user SHALL be connected to the room without restarting the application. |
| SR-9 | S4 | The system SHALL establish bidirectional VoIP streams between all participants upon joining a room. |
| SR-10 | S4 | Users SHALL have UI controls to mute/unmute their microphone and adjust output volume during a session. |
| SR-11 | S4 | The system SHALL show presence indicators for all connected users (nickname list with speaking status). |
| SR-12 | S4 | Rooms SHALL persist until the last participant leaves or an owner explicitly ends the session. |

## 3. Target platforms and hardware support
- **Operating systems:** Windows 10 and Windows 11 (64-bit editions) with the latest cumulative updates.
- **Supported audio devices:** USB headsets, 3.5 mm analog headsets via standard PC audio jacks, built-in laptop microphones/speakers, and Bluetooth audio devices that expose a Windows audio profile.
- **Minimum PC specifications:** Dual-core 2.0 GHz 64-bit CPU, 4 GB RAM, 500 MB free disk space for installation and caching, broadband internet connection (5 Mbps down / 2 Mbps up) with latency below 80 ms to the VolVoice signaling servers.

## 4. Non-functional requirements
- **Audio latency:** End-to-end mouth-to-ear latency SHALL not exceed 200 ms for participants meeting the minimum network requirements; average latency target is 120 ms.
- **Room scalability:** The service SHALL support a minimum of 16 concurrent participants per room at MVP launch and scale to 64 participants in subsequent releases without degradation of audio quality.
- **Reliability:** The service SHALL maintain 99.5% uptime for signaling and media services measured monthly.
- **Security and data handling:**
  - All signaling traffic SHALL be encrypted via TLS 1.2 or higher; media streams SHALL use DTLS-SRTP.
  - Access codes SHALL expire within 24 hours after room creation or immediately once manually revoked by the owner.
  - The system SHALL not retain voice recordings by default; transient audio buffers must be discarded after delivery.
  - Minimal user profile data (nickname) SHALL be stored in volatile session state only and cleared once the session ends.

## 5. Acceptance criteria
### MVP
- A Windows 10/11 64-bit desktop client installs and launches on hardware meeting the minimum specifications.
- Users can create rooms, share link/code, and have at least three participants join the same room with stable audio for a 30-minute session.
- Audio latency observed in controlled testing stays at or below the 200 ms requirement for users within the target network profile.
- Security checklist confirming TLS/DTLS-SRTP enforcement, ephemeral room codes, and lack of stored audio passes internal review.

### Post-MVP releases
- Room capacity validated to 64 participants with automated load tests while keeping latency under 250 ms.
- Support for persistent friend lists and scheduled rooms introduced without breaking MVP flows.
- Achieve 99.9% monthly uptime by implementing redundancy and monitoring alerts.
- Deliver compliance documentation for data handling and security suitable for enterprise adoption.
