# Phase 0: Raspberry Pi environment audit

Date: 2026-11-25
Machine: `pi5home` (aarch64), user `bliss`, no root used
Scope: read-only inspection. No packages installed, no config, service, or route changed.

Labels: FACT = directly observed command output. OBSERVATION = seen once, not reproduced. UNKNOWN = not determined.

## Hardware and OS

- FACT: Debian GNU/Linux 13 (trixie). CLAUDE.md section 4.1 says Bookworm. This must be corrected in CLAUDE.md (not changed here).
- FACT: kernel `6.18.29+rpt-rpi-2712`, architecture `aarch64`.
- FACT: 4 CPU cores, Cortex-A76.
- FACT: RAM 7.9 GiB total, about 6.6 GiB available at audit time. Swap 2.0 GiB, zram0, 0 B used.
- FACT: root filesystem on `/dev/mmcblk0p2`, 58 GB total, 15 GB used, 42 GB free (26%).
- FACT: CPU temperature 51.6 °C at audit time.

## Installed software

| Component | Result |
|---|---|
| Python | 3.13.5 (`/usr/bin/python3`) |
| Git | 2.47.3 |
| Node.js | present (`/usr/bin/node`), version not checked |
| OpenCode | v2.4.1 (`~/.opencode/bin/opencode`) |
| VNC | `wayvnc.service` (running, port 5900), plus `wayvnc-control.service`. Wayland VNC server, not TigerVNC/x11vnc. |
| Firefox | NOT FOUND (`firefox`, `firefox-esr` absent) |
| Docker | NOT FOUND |
| Playwright (Python) | NOT INSTALLED (`ModuleNotFoundError`) |

## Git repository

- FACT: `/home/bliss/web_lab` is a git repo, branch history contains one commit (`1014afb initial`), working tree clean before this audit.
- FACT: `origin` = `https://github.com/bayunderground/web_lab.git` (fetch and push). This matches the URL provided by the user. No change was made.
- FACT: no `.gitignore` exists yet. It must be created before the first commit (AGENTS.md section 4).

## Network

- FACT: `eth0` UP, `192.168.0.118/24`, default gateway `192.168.0.1` (DHCP). `wlan0` DOWN.
- FACT: a second interface `happ-xray` (172.19.0.1/30) carries the default route with metric 1, which takes precedence over `eth0` (metric 100). This is the VPN tunnel. Owner: the Happ client (outside Web Lab).
- FACT: IPv4 routing table `main` only. No custom policy-routing tables beyond the defaults (`ip rule`: local, main, default).
- FACT: DNS resolver is `127.0.0.1` (local stub on port 53). `getent` resolves `www.avito.ru` to 176.114.120.24, 176.114.122.24, 176.114.124.24.
- FACT: `vpn-gateway-watch.service` and `vpn-gateway-forward.service` are running. They are local project-external services that manage forwarding according to Happ state. Their unit files were read; their scripts (`/usr/local/lib/vpn-gateway/`) were not read.
- FACT: `/etc/wireguard` is not readable by user `bliss` (permission denied). `/etc/openvpn` exists (client, server, update-resolv-conf).
- OBSERVATION: public exit IP as seen by `ifconfig.me` is 34.160.111.145 (via the default route at time of test).
- UNKNOWN: whether the `happ-xray` tunnel is the one that makes Avito reachable (see below). Not tested.

## Listening services (relevant)

- SSH on 22 (IPv4 and IPv6).
- VNC on 5900 (`wayvnc`).
- DNS stub on 127.0.0.1:53 and 192.168.0.118:53.
- ngrok TCP endpoint for SSH (`ngrok-ssh.service`), local API on 127.0.0.1:4040.
- opencode listening on 127.0.0.1:49374.
- Other local ports (8888, 10808-10811) owned by processes not identified in this audit.

Note: ngrok exposes local SSH through a public tunnel. This was not configured by Web Lab and was not changed. It should be reviewed against CLAUDE.md section 12.2 (VNC and remote control must not be public). UNKNOWN: its configuration and whether it is intended.

## Avito reachability

- OBSERVATION: `curl -I https://www.avito.ru/` (default curl user agent, single request, no retry) returned HTTP 403 in 0.16 s from 176.114.120.24.
- INFERENCE: the server rejects this request. The cause is not known. It may be bot protection keyed on the client, the IP/route, or the request type (HEAD).
- Not done, deliberately: no retries, no browser-like headers, no alternate routes. AGENTS.md section 7 requires stopping and reporting when access is denied.
- UNKNOWN: whether a GET from a browser on this Pi, or from the Ubuntu PC, is accepted. Needs a decision from the user before any further request.

## Limitations

- Ubuntu PC audit not done (requires access to that machine, outside this session).
- Node.js version, wayvnc configuration, and the VPN scripts were not inspected.
- Avito behaviour is based on one HEAD request only.

## Re-test after VPN was disabled (2026-11-25, later)

- FACT: user disabled the VPN. Default route now `192.168.0.1 dev eth0`. The `happ-xray` interface is gone. `vpn-gateway-*` services still report `active`.
- OBSERVATION: `curl -I https://www.avito.ru/` (same method as before) returned **HTTP 429**, `server: QRATOR`, with challenge cookies. Before, with VPN on, it returned 403.
- INFERENCE: the response changed from 403 to 429 after the route changed. This matches QRATOR bot/rate protection. My earlier requests may also have contributed. The data cannot separate these causes.
- Action: stopped. No retries. AGENTS.md section 7 requires stopping and reporting on denied or limited access.

## Domains-to-CIDR data (read-only, `~/domains-to-cidr`)

- FACT: `networks.txt` already contains `176.114.120.0/24`, `176.114.122.0/24`, `176.114.124.0/24`. These cover the Avito IPs seen by DNS.
- FACT: `failed-domains.txt` lists 19 hosts that did not resolve, including `*.img.avito.st` CDN hosts, `www.cdn.uxfeedback.ru`, and `www.tube.buzzoola.com`. Their networks are not in `networks.txt`.
- OBSERVATION: `networks.txt` entries are /24, but `README.md` and the latest commit describe /20 mapping. Which tool version produced the file is UNKNOWN. Not changed.
- Not done: no edit to `networks.txt`, no run of `run.sh`. Those are manual steps for the user.

## Proposed installation plan (not executed, needs approval)

1. Firefox ESR from Debian repos (`apt`), to check ARM64 availability and version.
2. Playwright Python in a project-local virtualenv (`venv` outside Git).
3. Decide whether Docker is needed at all (CLAUDE.md section 4.4 says avoid unnecessary container layers). Not installed; no decision yet.

Every install step needs explicit approval (AGENTS.md section 3).
