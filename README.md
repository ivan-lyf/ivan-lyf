<!-- Header -->
<h1 align="center">Hey, I'm Ivan 👋</h1>
<h3 align="center">Computer Engineering @ UBC • Software & Embedded Systems</h3>

<p align="center">
  <a href="https://ivanluo.xyz">Website</a> •
  <a href="https://www.linkedin.com/in/ivan-yingfan-luo/">LinkedIn</a> •
  <a href="mailto:yingfanluo@gmail.com">Email</a>
</p>

---

### 💼 Experience

#### Apera AI — Software Engineer Intern *(Aug 2026 – Present)*
- Built cell localization for shipped robotic work cells, restoring arm-to-cell calibration after transport to **0.01 mm / 0.1°** accuracy
- Containerized the cell's web HMI (Docker, Bash) so PR test deployments bring up the bin-picking app and HMI together
- Fixed calibration progress reporting in the HMI by weighting progress by per-task step counts

#### Ruboss Technology (Leanpub) — Software Engineer Intern *(May – Aug 2026)*
- Shipped [Leanpub's first native iOS app](https://apps.apple.com/ca/app/leanpub/id913517110) in **7 weeks** as one of two engineers: 105 screens, SwiftUI over GraphQL, **1,000+ downloads**
- Built real-time collaborative editing across web and iOS with CRDTs (Yjs) over Rails ActionCable, porting Yjs's binary sync protocol to Swift
- Built an AI catalog assistant for leanpub.com, powered by a tool-calling LLM pipeline over the live catalog

#### UBC Rocket — Embedded Software Engineer *(Sept 2025 – Present)*
- Built the ground control station in C++ / Qt, rendering 100+ Hz telemetry with live 3D attitude and a satellite-view map
- Designed non-blocking STM32 firmware (SPI) delivering a jitter-free **1 kHz** IMU pipeline
- Built a bidirectional radio link with COBS framing and Protobuf, plus the PID flight-control law and a CTest regression harness

---

### 📌 Featured Projects

#### 📈 [Live Market Data FPGA Processor](https://github.com/ivan-lyf/live_fpga_market_data_processor)
A real-time trade tape on a DE10-Lite FPGA.  
**Tech:** SystemVerilog, Python, UART
- Python bridge streams live Coinbase trades as binary frames over UART to a SystemVerilog parser FSM
- Resynchronizing parser with length + XOR checksum validation, sequence-gap detection, and byte timeouts, verified in testbenches before hardware bring-up

#### 🪐 [GravitySandbox 3D](https://github.com/ivan-lyf/gravity_simulation/tree/rewrite)
Interactive N-body gravity simulator in the browser, rewritten from a 2D Qt/C++ prototype.  
**Tech:** TypeScript, React, three.js, Vitest
- Leapfrog KDK integrator with Plummer softening and momentum-conserving merges, in astronomical units (G = 4π²)
- Allocation-free 60 Hz frame loop that never re-renders React; Vitest suite covers 160-year orbit stability and energy drift

#### 🖥️ [ivanluo.xyz](https://ivanluo.xyz) ([source](https://github.com/ivan-lyf/ivan_leon_website))
A personal site rendered onto a 3D Macintosh you can orbit and zoom into.  
**Tech:** JavaScript, three.js
- Profile-driven desktop engine with windows, apps, and a read-only terminal over a virtual filesystem

#### 🏔️ [Whistler Blackcomb Forecast](https://github.com/ivan-lyf/whistler_weather_forecast)
Mountain-specific forecast app that corrects generic weather models using Whistler's local forecast errors.  
**Tech:** Python, FastAPI, PostgreSQL, LightGBM, Next.js, Docker
- Trained LightGBM correction models on archived GFS forecasts vs. ECCC / Open-Meteo observations going back to 2022
- Forecasts alpine snowfall, wind, freezing level, and precip type across base / mid / alpine bands, with SMS alerts via Twilio

#### 💣 [CS2 Nade Guide](https://github.com/ivan-lyf/cs_nade)
Native iPhone app for saving and sharing CS2 grenade lineups and tactics.  
**Tech:** SwiftUI, SwiftData + CloudKit, Supabase
- Local-first library synced through CloudKit, with a thin backend only for sign-in and shared tactics

---

### 🛠 Tech Stack

**Languages:** `C` • `C++` • `Python` • `TypeScript` • `JavaScript` • `Swift` • `Ruby` • `SystemVerilog` • `ARM Assembly`  
**Frameworks:** `React` • `Next.js` • `Remix` • `Node.js` • `SwiftUI` • `Rails` • `GraphQL` • `Qt` • `Protobuf`  
**Tools:** `Git` • `Docker` • `Claude Code` • `Xcode` • `Linux` • `CTest`

---

### 📫 Get in touch

- 🌐 Website: [ivanluo.xyz](https://ivanluo.xyz)
- 💼 LinkedIn: [Ivan Luo](https://www.linkedin.com/in/ivan-yingfan-luo/)
- ✉️ Email: yingfanluo@gmail.com

Always down to chat about cool projects, internships, or collabs.
